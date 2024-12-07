import math
import inspect
import itertools
import resource
import subprocess
from tqdm import tqdm
from functools import wraps
from itertools import islice

import numpy as np
import torch
import torch.optim as optim
from torch import nn, Tensor
import multiprocessing as mp

from netam.sequences import iter_codons, apply_aa_mask_to_nt_sequence

BIG = 1e9
SMALL_PROB = 1e-6
BASES = ["A", "C", "G", "T"]
BASES_AND_N_TO_INDEX = {"A": 0, "C": 1, "G": 2, "T": 3, "N": 4}
AA_STR_SORTED = "ACDEFGHIKLMNPQRSTVWY"
AA_STR_SORTED_AMBIG = AA_STR_SORTED + "X"
MAX_AMBIG_AA_IDX = len(AA_STR_SORTED_AMBIG) - 1

# I needed some sequence to use to normalize the rate of mutation in the SHM model.
# So, I chose perhaps the most famous antibody sequence, VRC01:
# https://www.ncbi.nlm.nih.gov/nuccore/GU980702.1
VRC01_NT_SEQ = (
    "CAGGTGCAGCTGGTGCAGTCTGGGGGTCAGATGAAGAAGCCTGGCGAGTCGATGAGAATT"
    "TCTTGTCGGGCTTCTGGATATGAATTTATTGATTGTACGCTAAATTGGATTCGTCTGGCC"
    "CCCGGAAAAAGGCCTGAGTGGATGGGATGGCTGAAGCCTCGGGGGGGGGCCGTCAACTAC"
    "GCACGTCCACTTCAGGGCAGAGTGACCATGACTCGAGACGTTTATTCCGACACAGCCTTT"
    "TTGGAGCTGCGCTCGTTGACAGTAGACGACACGGCCGTCTACTTTTGTACTAGGGGAAAA"
    "AACTGTGATTACAATTGGGACTTCGAACACTGGGGCCGGGGCACCCCGGTCATCGTCTCA"
    "TCA"
)


def force_spawn():
    """Force the spawn start method for multiprocessing.

    This is necessary to avoid conflicts with the internal OpenMP-based thread pool in
    PyTorch.
    """
    mp.set_start_method("spawn", force=True)


def generate_kmers(kmer_length):
    # Our strategy for kmers is to have a single representation for any kmer that isn't in ACGT.
    # This is the first one, which is simply "N", and so this placeholder value is 0.
    all_kmers = ["N"] + [
        "".join(p) for p in itertools.product(BASES, repeat=kmer_length)
    ]
    assert len(all_kmers) < torch.iinfo(torch.int32).max
    return all_kmers


def kmer_to_index_of(all_kmers):
    return {kmer: idx for idx, kmer in enumerate(all_kmers)}


def aa_idx_tensor_of_str_ambig(aa_str):
    """Return the indices of the amino acids in a string, allowing the ambiguous
    character."""
    try:
        return torch.tensor(
            [AA_STR_SORTED_AMBIG.index(aa) for aa in aa_str], dtype=torch.int
        )
    except ValueError:
        print(f"Found an invalid amino acid in the string: {aa_str}")
        raise


def generic_mask_tensor_of(ambig_symb, seq_str, length=None):
    """Return a mask tensor indicating non-empty and non-ambiguous sites.

    Sites beyond the length of the sequence are masked.
    """
    if length is None:
        length = len(seq_str)
    mask = torch.zeros(length, dtype=torch.bool)
    if len(seq_str) < length:
        seq_str += ambig_symb * (length - len(seq_str))
    else:
        seq_str = seq_str[:length]
    mask[[c != ambig_symb for c in seq_str]] = 1
    return mask


def codon_mask_tensor_of(nt_parent, *other_nt_seqs, aa_length=None):
    """Return a mask tensor indicating codons which contain at least one N.

    Codons beyond the length of the sequence are masked. If other_nt_seqs are provided,
    the "and" mask will be computed for all sequences
    """
    if aa_length is None:
        aa_length = len(nt_parent) // 3
    sequences = (nt_parent,) + other_nt_seqs
    mask = [
        all("N" not in codon for codon in codons)
        for codons in zip(*(iter_codons(sequence) for sequence in sequences))
    ]
    if len(mask) < aa_length:
        mask += [False] * (aa_length - len(mask))
    else:
        mask = mask[:aa_length]
    assert len(mask) == aa_length
    return torch.tensor(mask, dtype=torch.bool)


def assert_pcp_valid(parent, child, aa_mask=None):
    """Check that the parent-child pairs are valid.

    * The parent and child sequences must be the same length
    * There must be unmasked codons
    * The parent and child sequences must not match after masking codons containing
      ambiguities.

    Args:
        parent: The parent sequence.
        child: The child sequence.
        aa_mask: The mask tensor for the amino acid sequence. If None, it will be
            computed from the parent and child sequences.
    """
    if aa_mask is None:
        aa_mask = codon_mask_tensor_of(parent, child)
    if len(parent) != len(child):
        raise ValueError("Parent and child sequences are not the same length.")
    if not aa_mask.any():
        raise ValueError("Parent-child pair is masked in all codons.")
    if apply_aa_mask_to_nt_sequence(parent, aa_mask) == apply_aa_mask_to_nt_sequence(
        child, aa_mask
    ):
        raise ValueError(
            "Parent-child pair matches after masking codons containing ambiguities"
        )


def nt_mask_tensor_of(*args, **kwargs):
    return generic_mask_tensor_of("N", *args, **kwargs)


def aa_mask_tensor_of(*args, **kwargs):
    return generic_mask_tensor_of("X", *args, **kwargs)


def informative_site_count(seq_str):
    return sum(c != "N" for c in seq_str)


def clamp_probability(x: Tensor) -> Tensor:
    return torch.clamp(x, min=SMALL_PROB, max=(1.0 - SMALL_PROB))


def clamp_log_probability(x: Tensor) -> Tensor:
    return torch.clamp(x, max=np.log(1.0 - SMALL_PROB))


def print_parameter_count(model):
    total = 0
    for name, module in model.named_modules():
        if len(list(module.children())) == 0:  # Only count parameters in leaf modules
            num_params = sum(p.numel() for p in module.parameters())
            print(f"{name}: {num_params} parameters")
            total += num_params
    print("-----")
    print(f"total: {total} parameters")


def parameter_count_of_model(model):
    return sum(p.numel() for p in model.parameters() if p.requires_grad)


def stack_heterogeneous(tensors, pad_value=0.0):
    """Stack an iterable of 1D or 2D torch.Tensor objects of different lengths along the
    first dimension into a single tensor.

        black --check netam tests
    Args:
        tensors (iterable): An iterable of 1D or 2D torch.Tensor objects with variable lengths in the first dimension.
        pad_value (number): The value used for padding shorter tensors. Default is 0.

    Returns:
        torch.Tensor: A stacked tensor with all input tensors padded to the length of the longest tensor in the first dimension.
    """
    if tensors is None or len(tensors) == 0:
        return torch.Tensor()  # Return an empty tensor if no tensors are provided

    dim = tensors[0].dim()
    if dim not in [1, 2]:
        raise ValueError("This function only supports 1D or 2D tensors.")

    max_length = max(tensor.size(0) for tensor in tensors)

    if dim == 1:
        # If 1D, simply pad the end of the tensor.
        padded_tensors = [
            torch.nn.functional.pad(
                tensor, (0, max_length - tensor.size(0)), value=pad_value
            )
            for tensor in tensors
        ]
    else:
        # If 2D, pad the end of the first dimension (rows); the argument to pad
        # is a tuple of (padding_left, padding_right, padding_top,
        # padding_bottom)
        padded_tensors = [
            torch.nn.functional.pad(
                tensor, (0, 0, 0, max_length - tensor.size(0)), value=pad_value
            )
            for tensor in tensors
        ]

    return torch.stack(padded_tensors)


def optimizer_of_name(optimizer_name, model_parameters, **kwargs):
    """Build a torch.optim optimizer from a string name and model parameters.

    Use a SGD optimizer with momentum if the optimizer_name is "SGDMomentum".
    """
    if optimizer_name == "SGDMomentum":
        optimizer_name = "SGD"
        kwargs["momentum"] = 0.9
    try:
        optimizer_class = getattr(optim, optimizer_name)
        return optimizer_class(model_parameters, **kwargs)
    except AttributeError:
        raise ValueError(
            f"Optimizer '{optimizer_name}' is not recognized in torch.optim"
        )


def find_least_used_cuda_gpu():
    """Find the least used CUDA GPU on the system using nvidia-smi.

    If they are all idle, return None.
    """
    result = subprocess.run(
        ["nvidia-smi", "--query-gpu=utilization.gpu", "--format=csv,nounits,noheader"],
        stdout=subprocess.PIPE,
        text=True,
    )
    if result.returncode != 0:
        print(f"Error running nvidia-smi.")
        return None
    utilization = [int(x) for x in result.stdout.strip().split("\n")]
    if max(utilization) == 0:
        return None  # All GPUs are idle.
    # else:
    return utilization.index(min(utilization))


def pick_device(gpu_preference=None):
    """Pick a device for PyTorch to use.

    If gpu_preference is a string, use the device with that name. This is considered a
    strong preference from a user who knows what they are doing.

    If gpu_preference is an integer, this is a weak preference for a numbered GPU.  If
    CUDA is available, use the least used GPU, and if all are idle use the gpu_index
    modulo the number of GPUs. If gpu_index is None, then use a random GPU.
    """

    # Strong preference for a specific device.
    if gpu_preference is not None and isinstance(gpu_preference, str):
        return torch.device(gpu_preference)

    # else weak preference for a numbered GPU.

    # check that CUDA is usable
    def check_CUDA():
        try:
            torch._C._cuda_init()
            return True
        except:
            return False

    if torch.backends.cudnn.is_available() and check_CUDA():
        which_gpu = find_least_used_cuda_gpu()
        if which_gpu is None:
            if gpu_preference is None:
                which_gpu = np.random.randint(torch.cuda.device_count())
            else:
                which_gpu = gpu_preference % torch.cuda.device_count()
        print(f"Using CUDA GPU {which_gpu}")
        return torch.device(f"cuda:{which_gpu}")
    elif torch.backends.mps.is_available():
        print("Using Metal Performance Shaders")
        return torch.device("mps")
    else:
        print("Using CPU")
        return torch.device("cpu")


def print_tensor_devices(scope="local"):
    """Print the devices of all PyTorch tensors in the given scope.

    Args:
        scope (str): 'local' for local scope, 'global' for global scope.
    """
    if scope == "local":
        frame = inspect.currentframe()
        variables = frame.f_back.f_locals
    elif scope == "global":
        variables = globals()
    else:
        raise ValueError("Scope must be 'local' or 'global'.")

    for var_name, var_value in variables.items():
        if isinstance(var_value, torch.Tensor):
            print(f"{var_name}: {var_value.device}")


def get_memory_usage_mb():
    # Returns the peak memory usage in MB
    usage = resource.getrusage(resource.RUSAGE_SELF)
    return usage.ru_maxrss / 1024  # Convert from KB to MB


def tensor_to_np_if_needed(x):
    if isinstance(x, torch.Tensor):
        return x.cpu().numpy()
    else:
        assert isinstance(x, np.ndarray)
        return x


# Reference: https://pytorch.org/tutorials/beginner/transformer_tutorial.html
class PositionalEncoding(nn.Module):
    def __init__(self, d_model: int, dropout: float = 0.1, max_len: int = 5000):
        super().__init__()
        self.dropout = nn.Dropout(p=dropout)

        # assert that d_model is even
        assert d_model % 2 == 0, "d_model must be even for PositionalEncoding"

        position = torch.arange(max_len).unsqueeze(1)
        div_term = torch.exp(
            torch.arange(0, d_model, 2) * (-math.log(10000.0) / d_model)
        )
        pe = torch.zeros(max_len, 1, d_model)
        pe[:, 0, 0::2] = torch.sin(position * div_term)
        pe[:, 0, 1::2] = torch.cos(position * div_term)
        self.register_buffer("pe", pe)

    def forward(self, x: Tensor) -> Tensor:
        """
        Arguments:
            x: Tensor, shape ``[seq_len, batch_size, embedding_dim]``
        """
        x = x + self.pe[: x.size(0)]
        return self.dropout(x)


def linear_bump_lr(epoch, warmup_epochs, total_epochs, max_lr, min_lr):
    """Linearly increase the learning rate from min_lr to max_lr over warmup_epochs,
    then linearly decrease the learning rate from max_lr to min_lr.

    See https://github.com/matsengrp/netam/pull/41 for more details.

    Example:
    .. code-block:: python
        pd.Series([linear_bump_lr(epoch, warmup_epochs=20, total_epochs=200, max_lr=0.01, min_lr=1e-5) for epoch in range(200)]).plot()
    """
    if epoch < warmup_epochs:
        lr = min_lr + ((max_lr - min_lr) / warmup_epochs) * epoch
    else:
        lr = max_lr - ((max_lr - min_lr) / (total_epochs - warmup_epochs)) * (
            epoch - warmup_epochs
        )
    return lr


def encode_sequences(sequences, encoder):
    encoded_parents, wt_base_modifiers = zip(
        *[encoder.encode_sequence(sequence) for sequence in sequences]
    )
    masks = [nt_mask_tensor_of(sequence, encoder.site_count) for sequence in sequences]
    return (
        torch.stack(encoded_parents),
        torch.stack(masks),
        torch.stack(wt_base_modifiers),
    )


# from https://docs.python.org/3.11/library/itertools.html#itertools-recipes
# avoiding walrus:
def chunked(iterable, n):
    "Chunk data into lists of length n. The last chunk may be shorter."
    it = iter(iterable)
    while True:
        chunk = list(islice(it, n))
        if not chunk:
            return
        yield chunk


def chunk_method(default_chunk_size=2048, progress_bar_name=None):
    """Decorator to chunk the input to a method.

    Expects that all positional arguments are iterables of the same length,
    and that outputs are tuples of tensors whose first dimension
    corresponds to the first dimension of the input iterables.

    If method returns just one item, it must not be a tuple.

    Chunking is done along the first dimension of all inputs.

    Args:
        default_chunk_size: The default chunk size. The decorated method can
            also automatically accept a `default_chunk_size` keyword argument.
        progress_bar_name: The name of the progress bar. If None, no progress bar is shown.
    """

    def decorator(method):
        @wraps(method)
        def wrapper(self, *args, **kwargs):
            if "chunk_size" in kwargs:
                chunk_size = kwargs.pop("chunk_size")
            else:
                chunk_size = default_chunk_size
            results = []
            if progress_bar_name is None:
                progargs = {"disable": True}
            else:
                progargs = {"desc": progress_bar_name}
            bar = tqdm(total=len(args[0]), delay=2.0, **progargs)
            for chunked_args in zip(*(chunked(arg, chunk_size) for arg in args)):
                bar.update(len(chunked_args[0]))
                results.append(method(self, *chunked_args, **kwargs))
            if isinstance(results[0], tuple):
                return tuple(torch.cat(tensors) for tensors in zip(*results))
            else:
                return torch.cat(results)

        return wrapper

    return decorator
