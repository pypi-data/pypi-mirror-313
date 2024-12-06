"""
pybind csg module
"""
from __future__ import annotations
import netgen.libngpy._meshing
import typing
__all__ = ['And', 'CSGeometry', 'Cone', 'Cylinder', 'Ellipsoid', 'EllipticCone', 'Extrusion', 'Or', 'OrthoBrick', 'Plane', 'Polyhedron', 'Revolution', 'Save', 'Solid', 'Sphere', 'SplineCurve2d', 'SplineCurve3d', 'SplineSurface', 'Torus', 'ZRefinement']
class CSGeometry(netgen.libngpy._meshing.NetgenGeometry):
    def Add(self, solid: Solid, bcmod: list = [], maxh: float = 1e+99, col: tuple = (), transparent: bool = False, layer: int = 1) -> int:
        ...
    def AddPoint(self, arg0: netgen.libngpy._meshing.Point3d, arg1: int | str) -> CSGeometry:
        ...
    def AddSplineSurface(self, SplineSurface: SplineSurface) -> None:
        ...
    def AddSurface(self, surface: Solid, solid: Solid) -> None:
        ...
    @typing.overload
    def CloseSurfaces(self, solid1: Solid, solid2: Solid, slices: list) -> None:
        ...
    @typing.overload
    def CloseSurfaces(self, solid1: Solid, solid2: Solid, reflevels: int = 2, domain: Solid = None) -> None:
        ...
    def Draw(self) -> None:
        ...
    def GenerateMesh(self, mp: netgen.libngpy._meshing.MeshingParameters = None, **kwargs) -> netgen.libngpy._meshing.Mesh:
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
    def GetSolids(self) -> list:
        ...
    def GetTransparent(self, tlonr: int) -> bool:
        ...
    def GetVisible(self, tlonr: int) -> bool:
        ...
    def NameEdge(self, arg0: Solid, arg1: Solid, arg2: str) -> None:
        ...
    def PeriodicSurfaces(self, solid1: Solid, solid2: Solid, trafo: netgen.libngpy._meshing.Trafo = ...) -> None:
        ...
    def Save(self, arg0: str) -> None:
        ...
    def SetBoundingBox(self, pmin: netgen.libngpy._meshing.Point3d, pmax: netgen.libngpy._meshing.Point3d) -> None:
        ...
    def SetTransparent(self, tlonr: int, transparent: bool) -> None:
        ...
    def SetVisible(self, tlonr: int, visible: bool) -> None:
        ...
    def SingularEdge(self, arg0: Solid, arg1: Solid, arg2: float) -> None:
        ...
    def SingularFace(self, solid: Solid, surfaces: Solid = None, factor: float = 0.25) -> None:
        ...
    def SingularPoint(self, arg0: Solid, arg1: Solid, arg2: Solid, arg3: float) -> None:
        ...
    def __getstate__(self) -> tuple:
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, filename: str) -> None:
        ...
    def __setstate__(self, arg0: tuple) -> None:
        ...
    def _visualizationData(self) -> dict:
        ...
    @property
    def ntlo(self) -> int:
        ...
class Solid:
    def __add__(self, arg0: Solid) -> Solid:
        ...
    def __mul__(self, arg0: Solid) -> Solid:
        ...
    def __str__(self) -> str:
        ...
    def __sub__(self, arg0: Solid) -> Solid:
        ...
    @typing.overload
    def bc(self, arg0: int) -> Solid:
        ...
    @typing.overload
    def bc(self, arg0: str) -> Solid:
        ...
    def col(self, arg0: list) -> Solid:
        ...
    @typing.overload
    def mat(self, arg0: str) -> Solid:
        ...
    @typing.overload
    def mat(self) -> str:
        ...
    def maxh(self, arg0: float) -> Solid:
        ...
    def transp(self) -> Solid:
        ...
class SplineCurve2d:
    def AddPoint(self, arg0: float, arg1: float) -> int:
        ...
    @typing.overload
    def AddSegment(self, p1: int, p2: int, bcname: str = 'default', maxh: float = 1e+99) -> None:
        ...
    @typing.overload
    def AddSegment(self, p1: int, p2: int, p3: int, bcname: str = 'default', maxh: float = 1e+99) -> None:
        ...
    def __init__(self) -> None:
        ...
class SplineCurve3d:
    def AddPoint(self, arg0: float, arg1: float, arg2: float) -> int:
        ...
    @typing.overload
    def AddSegment(self, arg0: int, arg1: int) -> None:
        ...
    @typing.overload
    def AddSegment(self, arg0: int, arg1: int, arg2: int) -> None:
        ...
    def __init__(self) -> None:
        ...
class SplineSurface:
    """
    A surface for co dim 2 integrals on the splines
    """
    def AddPoint(self, x: float, y: float, z: float, hpref: bool = False) -> int:
        ...
    @typing.overload
    def AddSegment(self, pnt1: int, pnt2: int, bcname: str = 'default', maxh: float = -1.0) -> None:
        ...
    @typing.overload
    def AddSegment(self, pnt1: int, pnt2: int, pnt3: int, bcname: str = 'default', maxh: float = -1.0) -> None:
        ...
    def __init__(self, base: SPSolid, cuts: list = []) -> None:
        ...
def And(arg0: Solid, arg1: Solid) -> Solid:
    ...
def Cone(arg0: netgen.libngpy._meshing.Point3d, arg1: netgen.libngpy._meshing.Point3d, arg2: float, arg3: float) -> Solid:
    ...
def Cylinder(arg0: netgen.libngpy._meshing.Point3d, arg1: netgen.libngpy._meshing.Point3d, arg2: float) -> Solid:
    ...
def Ellipsoid(arg0: netgen.libngpy._meshing.Point3d, arg1: netgen.libngpy._meshing.Vec3d, arg2: netgen.libngpy._meshing.Vec3d, arg3: netgen.libngpy._meshing.Vec3d) -> Solid:
    ...
def EllipticCone(a: netgen.libngpy._meshing.Point3d, vl: netgen.libngpy._meshing.Vec3d, vs: netgen.libngpy._meshing.Vec3d, h: float, r: float) -> Solid:
    """
    An elliptic cone, given by the point 'a' at the base of the cone along the main axis,
    the vectors v and w of the long and short axis of the ellipse, respectively,
    the height of the cone, h, and ratio of base long axis length to top long axis length, r
    
    Note: The elliptic cone has to be truncated by planes similar to a cone or an elliptic cylinder.
    When r =1, the truncated elliptic cone becomes an elliptic cylinder.
    When r tends to zero, the truncated elliptic cone tends to a full elliptic cone.
    However, when r = 0, the top part becomes a point(tip) and meshing fails!
    """
def Extrusion(path: SplineCurve3d, profile: SplineCurve2d, d: netgen.libngpy._meshing.Vec3d) -> Solid:
    """
    A body of extrusion is defined by its profile
    (which has to be a closed, clockwiseoriented 2D curve),
     by a path (a 3D curve) and a vector d. It is constructed
     as follows: Take a point p on the path and denote the
     (unit-)tangent of the path in this point by t. If we cut
     the body by the plane given by p and t as normal vector,
     the cut is the profile. The profile is oriented by the
     (local) y-direction `y:=d−(d·t)t` and the (local) x-direction
     `x:=t \times y`.
    The following points have to be noticed:
     * If the path is not closed, then also the body is NOT closed.
       In this case e.g. planes or orthobricks have to be used to
       construct a closed body.
     * The path has to be smooth, i.e. the tangents at the end- resp.
       start-point of two consecutive spline or line patches have to
       have the same directions.
    """
def Or(arg0: Solid, arg1: Solid) -> Solid:
    ...
def OrthoBrick(arg0: netgen.libngpy._meshing.Point3d, arg1: netgen.libngpy._meshing.Point3d) -> Solid:
    ...
def Plane(arg0: netgen.libngpy._meshing.Point3d, arg1: netgen.libngpy._meshing.Vec3d) -> Solid:
    ...
def Polyhedron(arg0: list, arg1: list) -> Solid:
    ...
def Revolution(arg0: netgen.libngpy._meshing.Point3d, arg1: netgen.libngpy._meshing.Point3d, arg2: SplineCurve2d) -> Solid:
    ...
def Save(arg0: netgen.libngpy._meshing.Mesh, arg1: str, arg2: CSGeometry) -> None:
    ...
def Sphere(arg0: netgen.libngpy._meshing.Point3d, arg1: float) -> Solid:
    ...
def Torus(arg0: netgen.libngpy._meshing.Point3d, arg1: netgen.libngpy._meshing.Vec3d, arg2: float, arg3: float) -> Solid:
    ...
def ZRefinement(arg0: netgen.libngpy._meshing.Mesh, arg1: CSGeometry) -> None:
    ...
