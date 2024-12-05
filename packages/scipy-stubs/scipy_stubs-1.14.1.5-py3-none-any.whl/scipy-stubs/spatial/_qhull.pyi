from typing import Any, TypeAlias
from typing_extensions import final

import numpy as np
import numpy.typing as npt
import optype.numpy as onp

__all__ = ["ConvexHull", "Delaunay", "HalfspaceIntersection", "QhullError", "Voronoi", "tsearch"]

_Array_i: TypeAlias = onp.ArrayND[np.intc]
_Array_n: TypeAlias = onp.ArrayND[np.intp]
_Array_f8: TypeAlias = onp.ArrayND[np.float64]

class QhullError(RuntimeError): ...

@final
class _Qhull:
    mode_option: bytes
    options: bytes
    furthest_site: bool
    @property
    def ndim(self, /) -> int: ...
    def __init__(
        self,
        /,
        mode_option: bytes,
        points: _Array_f8,
        options: bytes | None = None,
        required_options: bytes | None = None,
        furthest_site: bool = False,
        incremental: bool = False,
        interior_point: _Array_f8 | None = None,
    ) -> None: ...
    def check_active(self, /) -> None: ...
    def close(self, /) -> None: ...
    def get_points(self, /) -> _Array_f8: ...
    def add_points(self, /, points: npt.ArrayLike, interior_point: npt.ArrayLike | None = None) -> None: ...
    def get_paraboloid_shift_scale(self, /) -> tuple[float, float]: ...
    def volume_area(self, /) -> tuple[float, float]: ...
    def triangulate(self, /) -> None: ...
    def get_simplex_facet_array(self, /) -> tuple[_Array_i, _Array_i, _Array_f8, _Array_i, _Array_i]: ...
    def get_hull_points(self, /) -> _Array_f8: ...
    def get_hull_facets(self, /) -> tuple[list[list[int]], _Array_f8]: ...
    def get_voronoi_diagram(self, /) -> tuple[_Array_f8, _Array_i, list[list[int]], list[list[int]], _Array_n]: ...
    def get_extremes_2d(self, /) -> _Array_i: ...

def _get_barycentric_transforms(points: _Array_f8, simplices: _Array_i, eps: float) -> _Array_f8: ...

class _QhullUser:
    ndim: int
    npoints: int
    min_bound: _Array_f8
    max_bound: _Array_f8

    def __init__(self, /, qhull: _Qhull, incremental: bool = False) -> None: ...
    def __del__(self, /) -> None: ...
    def _update(self, /, qhull: _Qhull) -> None: ...
    def _add_points(
        self,
        /,
        points: npt.ArrayLike,
        restart: bool = False,
        interior_point: npt.ArrayLike | None = None,
    ) -> None: ...
    def close(self, /) -> None: ...

class Delaunay(_QhullUser):
    furthest_site: bool
    paraboloid_scale: float
    paraboloid_shift: float
    simplices: _Array_i
    neighbors: _Array_i
    equations: _Array_f8
    coplanar: _Array_i
    good: _Array_i
    nsimplex: int
    vertices: _Array_i

    def __init__(
        self,
        /,
        points: npt.ArrayLike,
        furthest_site: bool = False,
        incremental: bool = False,
        qhull_options: str | None = None,
    ) -> None: ...
    def add_points(self, /, points: npt.ArrayLike, restart: bool = False) -> None: ...
    @property
    def points(self, /) -> _Array_f8: ...
    @property
    def transform(self, /) -> _Array_f8: ...
    @property
    def vertex_to_simplex(self, /) -> _Array_i: ...
    @property
    def vertex_neighbor_vertices(self, /) -> tuple[_Array_i, _Array_i]: ...
    @property
    def convex_hull(self, /) -> _Array_i: ...
    def find_simplex(self, /, xi: npt.ArrayLike, bruteforce: bool = False, tol: float | None = None) -> _Array_i: ...
    def plane_distance(self, /, xi: npt.ArrayLike) -> _Array_f8: ...
    def lift_points(self, /, x: npt.ArrayLike) -> _Array_f8: ...

def tsearch(tri: Delaunay, xi: npt.ArrayLike) -> _Array_i: ...
def _copy_docstr(dst: object, src: object) -> None: ...

class ConvexHull(_QhullUser):
    simplices: _Array_i
    neighbors: _Array_i
    equations: _Array_f8
    coplanar: _Array_i
    good: onp.ArrayND[np.bool_] | None
    volume: float
    area: float
    nsimplex: int

    def __init__(self, /, points: npt.ArrayLike, incremental: bool = False, qhull_options: str | None = None) -> None: ...
    def add_points(self, /, points: npt.ArrayLike, restart: bool = False) -> None: ...
    @property
    def points(self, /) -> _Array_f8: ...
    @property
    def vertices(self, /) -> _Array_i: ...

class Voronoi(_QhullUser):
    vertices: _Array_f8
    ridge_points: _Array_i
    ridge_vertices: list[list[int]]
    regions: list[list[int]]
    point_region: _Array_n
    furthest_site: bool

    def __init__(
        self,
        /,
        points: npt.ArrayLike,
        furthest_site: bool = False,
        incremental: bool = False,
        qhull_options: str | None = None,
    ) -> None: ...
    def add_points(self, /, points: npt.ArrayLike, restart: bool = False) -> None: ...
    @property
    def points(self, /) -> _Array_f8: ...
    @property
    def ridge_dict(self, /) -> dict[tuple[int, int], list[int]]: ...

class HalfspaceIntersection(_QhullUser):
    interior_point: _Array_f8
    dual_facets: list[list[int]]
    dual_equations: _Array_f8
    dual_points: _Array_f8
    dual_volume: float
    dual_area: float
    intersections: _Array_f8
    ndim: int
    nineq: int

    def __init__(
        self,
        /,
        halfspaces: npt.ArrayLike,
        interior_point: npt.ArrayLike,
        incremental: bool = False,
        qhull_options: str | None = None,
    ) -> None: ...
    def add_halfspaces(self, /, halfspaces: npt.ArrayLike, restart: bool = False) -> None: ...
    @property
    def halfspaces(self, /) -> _Array_f8: ...
    @property
    def dual_vertices(self, /) -> onp.ArrayND[np.integer[Any]]: ...
