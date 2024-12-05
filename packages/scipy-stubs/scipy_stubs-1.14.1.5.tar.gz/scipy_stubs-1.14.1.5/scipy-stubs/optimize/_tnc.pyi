from collections.abc import Callable, Sequence
from typing import Any, Final, Literal, TypeAlias

import numpy as np
import numpy.typing as npt
import optype.numpy as onp

__all__ = ["fmin_tnc"]

_ReturnCode: TypeAlias = Literal[-1, 0, 1, 2, 3, 4, 5, 6, 7]

MSG_NONE: Final = 0
MSG_ITER: Final = 1
MSG_INFO: Final = 2
MSG_VERS: Final = 4
MSG_EXIT: Final = 8
MSG_ALL: Final = 15
MSGS: Final[dict[Literal[0, 1, 2, 4, 8, 15], str]]

INFEASIBLE: Final = -1
LOCALMINIMUM: Final = 0
FCONVERGED: Final = 1
XCONVERGED: Final = 2
MAXFUN: Final = 3
LSFAIL: Final = 4
CONSTANT: Final = 5
NOPROGRESS: Final = 6
USERABORT: Final = 7
RCSTRINGS: Final[dict[_ReturnCode, str]]

def fmin_tnc(
    func: Callable[..., float | np.floating[Any]] | Callable[..., tuple[float | np.floating[Any], float | np.floating[Any]]],
    x0: npt.ArrayLike,
    fprime: Callable[..., float | np.floating[Any]] | None = None,
    args: tuple[object, ...] = (),
    approx_grad: int = 0,
    bounds: Sequence[tuple[float | None, float | None]] | None = None,
    epsilon: float = 1e-08,
    scale: npt.ArrayLike | None = None,
    offset: npt.ArrayLike | None = None,
    messages: int = ...,
    maxCGit: int = -1,
    maxfun: int | None = None,
    eta: float = -1,
    stepmx: float = 0,
    accuracy: float = 0,
    fmin: float = 0,
    ftol: float = -1,
    xtol: float = -1,
    pgtol: float = -1,
    rescale: float = -1,
    disp: bool | None = None,
    callback: Callable[[onp.ArrayND[np.floating[Any]]], None] | None = None,
) -> tuple[onp.ArrayND[np.floating[Any]], int, _ReturnCode]: ...
