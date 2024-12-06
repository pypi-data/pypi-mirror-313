"""
pybind geom2d module
"""
from __future__ import annotations
import netgen.libngpy._meshing
import os
import typing
__all__ = ['CSG2d', 'Circle', 'EdgeInfo', 'PointInfo', 'Rectangle', 'Solid2d', 'Spline', 'SplineGeometry']
class CSG2d:
    def Add(self, arg0: Solid2d) -> None:
        ...
    def GenerateMesh(self, mp: netgen.libngpy._meshing.MeshingParameters | None = None, **kwargs) -> netgen.libngpy._meshing.Mesh:
        """
        Meshing Parameters
        -------------------
        
        maxh: float = 1e10
          Global upper bound for mesh size.
        
        grading: float = 0.3
          Mesh grading how fast the local mesh size can change.
        
        meshsizefilename: str = None
          Load meshsize from file. Can set local mesh size for points
          and along edges. File must have the format:
        
            nr_points
            x1, y1, z1, meshsize
            x2, y2, z2, meshsize
            ...
            xn, yn, zn, meshsize
        
            nr_edges
            x11, y11, z11, x12, y12, z12, meshsize
            ...
            xn1, yn1, zn1, xn2, yn2, zn2, meshsize
        
        segmentsperedge: float = 1.
          Minimal number of segments per edge.
        
        quad_dominated: bool = False
          Quad-dominated surface meshing.
        
        blockfill: bool = True
          Do fast blockfilling.
        
        filldist: float = 0.1
          Block fill up to distance
        
        delaunay: bool = True
          Use delaunay meshing.
        
        delaunay2d : bool = True
          Use delaunay meshing for 2d geometries.
        
        Optimization Parameters
        -----------------------
        
        optimize3d: str = "cmdmustm"
          3d optimization strategy:
            m .. move nodes
            M .. move nodes, cheap functional
            s .. swap faces
            c .. combine elements
            d .. divide elements
            p .. plot, no pause
            P .. plot, Pause
            h .. Histogramm, no pause
            H .. Histogramm, pause
        
        optsteps3d: int = 3
          Number of 3d optimization steps.
        
        optimize2d: str = "smcmSmcmSmcm"
          2d optimization strategy:
            s .. swap, opt 6 lines/node
            S .. swap, optimal elements
            m .. move nodes
            p .. plot, no pause
            P .. plot, pause
            c .. combine
        
        optsteps2d: int = 3
          Number of 2d optimization steps.
        
        elsizeweight: float = 0.2
          Weight of element size w.r.t. element shape in optimization.
        """
    def GenerateSplineGeometry(self) -> SplineGeometry:
        ...
    def __init__(self) -> None:
        ...
class EdgeInfo:
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, control_point: netgen.libngpy._meshing.Point2d) -> None:
        ...
    @typing.overload
    def __init__(self, maxh: float) -> None:
        ...
    @typing.overload
    def __init__(self, bc: str) -> None:
        ...
    @typing.overload
    def __init__(self, control_point: netgen.libngpy._meshing.Point2d | None = None, maxh: float = 1e+99, bc: str = '') -> None:
        ...
class PointInfo:
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, maxh: float) -> None:
        ...
    @typing.overload
    def __init__(self, name: str) -> None:
        ...
    @typing.overload
    def __init__(self, maxh: float, name: str) -> None:
        ...
class Solid2d:
    def BC(self, arg0: str) -> Solid2d:
        ...
    def Copy(self) -> Solid2d:
        ...
    def Layer(self, arg0: int) -> Solid2d:
        ...
    def Mat(self, arg0: str) -> Solid2d:
        ...
    def Maxh(self, arg0: float) -> Solid2d:
        ...
    def Move(self, arg0: netgen.libngpy._meshing.Vec2d) -> Solid2d:
        ...
    def Rotate(self, angle: float, center: netgen.libngpy._meshing.Point2d = ...) -> Solid2d:
        ...
    @typing.overload
    def Scale(self, arg0: float) -> Solid2d:
        ...
    @typing.overload
    def Scale(self, arg0: netgen.libngpy._meshing.Vec2d) -> Solid2d:
        ...
    def __add__(self, arg0: Solid2d) -> Solid2d:
        ...
    def __iadd__(self, arg0: Solid2d) -> Solid2d:
        ...
    def __imul__(self, arg0: Solid2d) -> Solid2d:
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, points: Array[netgen.libngpy._meshing.Point2d | ... | ...], mat: str = '', bc: str = '') -> None:
        ...
    def __isub__(self, arg0: Solid2d) -> Solid2d:
        ...
    def __mul__(self, arg0: Solid2d) -> Solid2d:
        ...
    def __sub__(self, arg0: Solid2d) -> Solid2d:
        ...
class Spline:
    """
    Spline of a SplineGeometry object
    """
    leftdom: int
    rightdom: int
    def EndPoint(self) -> netgen.libngpy._meshing.Point2d:
        ...
    def GetNormal(self, arg0: float) -> netgen.libngpy._meshing.Vec2d:
        ...
    def StartPoint(self) -> netgen.libngpy._meshing.Point2d:
        ...
    @property
    def bc(self) -> int:
        ...
class SplineGeometry(netgen.libngpy._meshing.NetgenGeometry):
    """
    a 2d boundary representation geometry model by lines and splines
    """
    def AddCurve(self, func: typing.Any, leftdomain: int = 1, rightdomain: int = 0, bc: typing.Any = ..., maxh: float = 1e+99) -> None:
        """
        Curve is given as parametrization on the interval [0,1]
        """
    def Append(self, point_indices: list, leftdomain: int = 1, rightdomain: int = 0, bc: int | str | None = None, copy: int | None = None, maxh: float = 1e+99, hpref: float = 0, hprefleft: float = 0, hprefright: float = 0) -> int:
        ...
    def AppendPoint(self, x: float, y: float, maxh: float = 1e+99, hpref: float = 0, name: str = '') -> int:
        ...
    def AppendSegment(self, point_indices: list, leftdomain: int = 1, rightdomain: int = 0) -> None:
        ...
    def Draw(self) -> None:
        ...
    def GenerateMesh(self, mp: netgen.libngpy._meshing.MeshingParameters | None = None, **kwargs) -> netgen.libngpy._meshing.Mesh:
        """
        Meshing Parameters
        -------------------
        
        maxh: float = 1e10
          Global upper bound for mesh size.
        
        grading: float = 0.3
          Mesh grading how fast the local mesh size can change.
        
        meshsizefilename: str = None
          Load meshsize from file. Can set local mesh size for points
          and along edges. File must have the format:
        
            nr_points
            x1, y1, z1, meshsize
            x2, y2, z2, meshsize
            ...
            xn, yn, zn, meshsize
        
            nr_edges
            x11, y11, z11, x12, y12, z12, meshsize
            ...
            xn1, yn1, zn1, xn2, yn2, zn2, meshsize
        
        segmentsperedge: float = 1.
          Minimal number of segments per edge.
        
        quad_dominated: bool = False
          Quad-dominated surface meshing.
        
        blockfill: bool = True
          Do fast blockfilling.
        
        filldist: float = 0.1
          Block fill up to distance
        
        delaunay: bool = True
          Use delaunay meshing.
        
        delaunay2d : bool = True
          Use delaunay meshing for 2d geometries.
        
        Optimization Parameters
        -----------------------
        
        optimize3d: str = "cmdmustm"
          3d optimization strategy:
            m .. move nodes
            M .. move nodes, cheap functional
            s .. swap faces
            c .. combine elements
            d .. divide elements
            p .. plot, no pause
            P .. plot, Pause
            h .. Histogramm, no pause
            H .. Histogramm, pause
        
        optsteps3d: int = 3
          Number of 3d optimization steps.
        
        optimize2d: str = "smcmSmcmSmcm"
          2d optimization strategy:
            s .. swap, opt 6 lines/node
            S .. swap, optimal elements
            m .. move nodes
            p .. plot, no pause
            P .. plot, pause
            c .. combine
        
        optsteps2d: int = 3
          Number of 2d optimization steps.
        
        elsizeweight: float = 0.2
          Weight of element size w.r.t. element shape in optimization.
        """
    def GetBCName(self, arg0: int) -> str:
        ...
    def GetNDomains(self) -> int:
        ...
    def GetNPoints(self) -> int:
        ...
    def GetNSplines(self) -> int:
        ...
    def GetPoint(self, arg0: int) -> netgen.libngpy._meshing.Point2d:
        ...
    def GetSpline(self, arg0: int) -> Spline:
        ...
    def Load(self, arg0: os.PathLike) -> None:
        ...
    def PlotData(self) -> tuple:
        ...
    def PointData(self) -> tuple:
        ...
    def Print(self) -> None:
        ...
    def SegmentData(self) -> tuple:
        ...
    def SetDomainLayer(self, arg0: int, arg1: int) -> None:
        ...
    def SetDomainMaxH(self, arg0: int, arg1: float) -> None:
        ...
    def SetMaterial(self, arg0: int, arg1: str) -> None:
        ...
    def _SetDomainTensorMeshing(self, arg0: int, arg1: bool) -> None:
        ...
    def __getstate__(self) -> tuple:
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: str) -> None:
        ...
    def __setstate__(self, arg0: tuple) -> None:
        ...
    def _visualizationData(self) -> dict:
        ...
def Circle(center: netgen.libngpy._meshing.Point2d, radius: float, mat: str = '', bc: str = '') -> Solid2d:
    ...
def Rectangle(pmin: netgen.libngpy._meshing.Point2d, pmax: netgen.libngpy._meshing.Point2d, mat: str = '', bc: str = '', bottom: str | None = None, right: str | None = None, top: str | None = None, left: str | None = None) -> Solid2d:
    ...
