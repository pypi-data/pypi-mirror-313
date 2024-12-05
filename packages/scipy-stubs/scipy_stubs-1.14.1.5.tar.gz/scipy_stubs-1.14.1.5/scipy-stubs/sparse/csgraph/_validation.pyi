from typing import Any, Final, TypeAlias

import numpy as np
import numpy.typing as npt
import optype.numpy as onp
from scipy.sparse import sparray, spmatrix

_GraphLike: TypeAlias = onp.ToFloat2D | sparray | spmatrix

DTYPE: Final[type[np.float64]] = ...

def validate_graph(
    csgraph: _GraphLike,
    directed: bool,
    dtype: npt.DTypeLike = ...,
    csr_output: bool = True,
    dense_output: bool = True,
    copy_if_dense: bool = False,
    copy_if_sparse: bool = False,
    null_value_in: float = 0,
    null_value_out: float = ...,
    infinity_null: bool = True,
    nan_null: bool = True,
) -> onp.Array2D[np.floating[Any]]: ...
