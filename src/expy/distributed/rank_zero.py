import os
from functools import wraps
from typing import Callable, Optional, ParamSpec, TypeVar, overload


def _get_rank() -> Optional[int]:
    # SLURM_PROCID can be set even if SLURM is not managing the multiprocessing,
    # therefore LOCAL_RANK needs to be checked first
    rank_keys = ("RANK", "LOCAL_RANK", "SLURM_PROCID", "JSM_NAMESPACE_RANK")
    for key in rank_keys:
        rank = os.environ.get(key)
        if rank is not None:
            return int(rank)

    # None to differentiate whether an environment variable was set at all
    return None


T = TypeVar("T")
P = ParamSpec("P")


@overload
def rank_zero_only(fn: Callable[P, T]) -> Callable[P, Optional[T]]:
    """Rank zero only."""


@overload
def rank_zero_only(fn: Callable[P, T], default: T) -> Callable[P, T]:
    """Rank zero only."""


def rank_zero_only(
    fn: Callable[P, T], default: Optional[T] = None
) -> Callable[P, Optional[T]]:
    @wraps(fn)
    def wrapped_fn(*args: P.args, **kwargs: P.kwargs) -> Optional[T]:
        rank = getattr(rank_zero_only, "rank", None)
        if rank is None:
            raise RuntimeError("The `rank_zero_only.rank` needs to be set before use")
        if rank == 0:
            return fn(*args, **kwargs)
        return default

    return wrapped_fn


rank_zero_only.rank = getattr(rank_zero_only, "rank", _get_rank() or 0)
