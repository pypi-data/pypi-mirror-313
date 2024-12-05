# pyright: reportInconsistentConstructor=false

from collections.abc import Sequence
from typing import ClassVar, Literal
from typing_extensions import Self, override

import numpy as np
import numpy.typing as npt
import optype.numpy as onp
from scipy._typing import Untyped, UntypedArray, UntypedTuple

__all__ = ["LinearOperator", "aslinearoperator"]

# TODO: make these all generic
class LinearOperator:
    __array_ufunc__: ClassVar[None]

    shape: tuple[int] | tuple[int, int]
    ndim: Literal[1, 2]
    dtype: np.dtype[np.generic]

    def __new__(cls, *args: Untyped, **kwargs: Untyped) -> Self: ...
    def __init__(self, /, dtype: npt.DTypeLike, shape: onp.ToInt | Sequence[onp.ToInt]) -> None: ...
    def matvec(self, /, x: npt.ArrayLike) -> UntypedArray: ...
    def rmatvec(self, /, x: npt.ArrayLike) -> UntypedArray: ...
    def matmat(self, /, X: npt.ArrayLike) -> UntypedArray: ...
    def rmatmat(self, /, X: npt.ArrayLike) -> UntypedArray: ...
    def __call__(self, /, x: npt.ArrayLike | LinearOperator) -> _ProductLinearOperator | _ScaledLinearOperator | UntypedArray: ...
    def __mul__(self, x: LinearOperator | npt.ArrayLike, /) -> _ProductLinearOperator | _ScaledLinearOperator | UntypedArray: ...
    def __truediv__(self, other: onp.ToScalar, /) -> _ScaledLinearOperator: ...
    def dot(self, /, x: LinearOperator | npt.ArrayLike) -> _ProductLinearOperator | _ScaledLinearOperator | UntypedArray: ...
    def __matmul__(
        self,
        other: LinearOperator | onp.CanArray[tuple[int, ...], np.dtype[np.generic]],
        /,
    ) -> _ScaledLinearOperator | UntypedArray: ...
    def __rmatmul__(
        self,
        other: LinearOperator | onp.CanArray[tuple[int, ...], np.dtype[np.generic]],
        /,
    ) -> _ScaledLinearOperator | UntypedArray: ...
    def __rmul__(self, x: LinearOperator | npt.ArrayLike, /) -> Untyped: ...
    def __pow__(self, p: onp.ToScalar, /) -> _PowerLinearOperator: ...
    def __add__(self, x: LinearOperator, /) -> _SumLinearOperator: ...
    def __neg__(self, /) -> _ScaledLinearOperator: ...
    def __sub__(self, x: LinearOperator, /) -> _SumLinearOperator: ...
    def adjoint(self, /) -> _AdjointLinearOperator: ...
    @property
    def H(self, /) -> _AdjointLinearOperator: ...
    def transpose(self, /) -> _TransposedLinearOperator: ...
    @property
    def T(self, /) -> _TransposedLinearOperator: ...

class _CustomLinearOperator(LinearOperator):
    args: UntypedTuple
    def __init__(
        self,
        /,
        shape: Untyped,
        matvec: Untyped,
        rmatvec: Untyped | None = None,
        matmat: Untyped | None = None,
        dtype: Untyped | None = None,
        rmatmat: Untyped | None = None,
    ) -> None: ...

class _AdjointLinearOperator(LinearOperator):
    A: LinearOperator
    args: tuple[LinearOperator]
    def __init__(self, /, A: LinearOperator) -> None: ...

class _TransposedLinearOperator(LinearOperator):
    A: LinearOperator
    args: tuple[LinearOperator]
    def __init__(self, /, A: LinearOperator) -> None: ...

class _SumLinearOperator(LinearOperator):
    args: tuple[LinearOperator, LinearOperator]
    def __init__(self, /, A: LinearOperator, B: LinearOperator) -> None: ...

class _ProductLinearOperator(LinearOperator):
    args: tuple[LinearOperator, LinearOperator]
    def __init__(self, /, A: LinearOperator, B: LinearOperator) -> None: ...

class _ScaledLinearOperator(LinearOperator):
    args: tuple[LinearOperator, onp.ToScalar]
    def __init__(self, /, A: LinearOperator, alpha: onp.ToScalar) -> None: ...

class _PowerLinearOperator(LinearOperator):
    args: tuple[LinearOperator, onp.ToInt]
    def __init__(self, /, A: LinearOperator, p: onp.ToInt) -> None: ...

class MatrixLinearOperator(LinearOperator):
    A: LinearOperator
    args: tuple[LinearOperator]
    def __init__(self, /, A: LinearOperator) -> None: ...

class _AdjointMatrixOperator(MatrixLinearOperator):
    A: LinearOperator
    args: tuple[LinearOperator]
    shape: tuple[int, int]  # pyright: ignore[reportIncompatibleVariableOverride]
    @property
    @override
    def dtype(self, /) -> np.dtype[np.generic]: ...  # type: ignore[override] # pyright: ignore[reportIncompatibleVariableOverride]
    def __init__(self, /, adjoint: LinearOperator) -> None: ...

class IdentityOperator(LinearOperator):
    def __init__(self, /, shape: Untyped, dtype: Untyped | None = None) -> None: ...

def aslinearoperator(A: Untyped) -> Untyped: ...
