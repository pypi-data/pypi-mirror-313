from typing import Final, Literal, TypeAlias, overload

import numpy as np
import optype.numpy as onp
from scipy.sparse import csr_matrix, sparray, spmatrix

_GraphLike: TypeAlias = onp.ToFloat2D | sparray | spmatrix

DTYPE: Final[type[np.float64]] = ...
ITYPE: Final[type[np.int32]] = ...

def connected_components(
    csgraph: _GraphLike,
    directed: bool = True,
    connection: Literal["weak", "strong"] = "weak",
    return_labels: bool = True,
) -> tuple[int, onp.Array1D[np.int32]]: ...
def breadth_first_tree(csgraph: _GraphLike, i_start: int, directed: bool = True) -> csr_matrix: ...
def depth_first_tree(csgraph: _GraphLike, i_start: int, directed: bool = True) -> csr_matrix: ...

#
@overload
def breadth_first_order(
    csgraph: _GraphLike,
    i_start: int,
    directed: bool = True,
    return_predecessors: Literal[True, 1] = True,
) -> tuple[onp.Array1D[np.int32], onp.Array1D[np.int32]]: ...
@overload
def breadth_first_order(
    csgraph: _GraphLike,
    i_start: int,
    directed: bool,
    return_predecessors: Literal[False, 0],
) -> onp.Array1D[np.int32]: ...
@overload
def breadth_first_order(
    csgraph: _GraphLike,
    i_start: int,
    directed: bool = True,
    *,
    return_predecessors: Literal[False, 0],
) -> onp.Array1D[np.int32]: ...
@overload
def depth_first_order(
    csgraph: _GraphLike,
    i_start: int,
    directed: bool = True,
    return_predecessors: Literal[True] = True,
) -> tuple[onp.Array1D[np.int32], onp.Array1D[np.int32]]: ...
@overload
def depth_first_order(
    csgraph: _GraphLike,
    i_start: int,
    directed: bool,
    return_predecessors: Literal[False, 0],
) -> onp.Array1D[np.int32]: ...
@overload
def depth_first_order(
    csgraph: _GraphLike,
    i_start: int,
    directed: bool = True,
    *,
    return_predecessors: Literal[False, 0],
) -> onp.Array1D[np.int32]: ...
