import numpy as np
from typing import Sequence, Generator, Tuple, Set, Any, Dict, TypeVar, Type
from linealg import AffineTransform, PointLike, ArrayPoint, lineRayIntersectionPoint
import abc

T = TypeVar('T')

class BoundingBox:
    """
    A class that represents a 2D bounding box (a rectangle whose sides are parallel to (1,0) and (0,1)).
    
    Attributes:
        minX (float): The minimum X coordinate of the bounding box.
        minY (float): The minimum Y coordinate of the bounding box.
        maxX (float): The maximum X coordinate of the bounding box.
        maxY (float): The maximum Y coordinate of the bounding box.
    """

    def __init__(self, minX:float = 0., minY:float=0., maxX:float=0., maxY:float=0.):
        """Initializes the BoundingBox with each respective attribute."""
        self.minX = minX
        self.maxX = maxX
        self.minY = minY
        self.maxY = maxY

    def transform(self, matrix:AffineTransform):
        """Transforms this bounding box using an affine transformation, then sets it to the bounding rectangle of this transformed shape."""
        verts = [(self.minX, self.minY), (self.minX, self.maxY), (self.maxX, self.maxY), (self.maxX, self.minY)]
        verts = (matrix.apply(v) for v in verts)
        xs, ys = zip(*verts)
        self.minX = min(xs)
        self.maxX = max(xs)
        self.minY = min(ys)
        self.maxY = max(ys)

    def pixels(self):
        """Returns a generator that iterates over all pixels contained withing the bounding box (including pixels at the edges)."""
        for x in range(int(self.minX), 1+int(self.maxX)):
            yield from ((x,y) for y in range(int(self.minY), 1+int(self.maxY)))

class Primitive(abc.ABC):
    """
    An abstract class that represents a primitive shape in 2D space.
    
    Attributes:
        boundingBox (BoundingBox): The bounding rectangle which contains the entire shape.
    """

    boundingBox:BoundingBox 

    @abc.abstractmethod
    def contains(self, point:PointLike) -> bool:
        """Returns whether this shape contains a given point in 2D space."""
        raise NotImplementedError()

    @abc.abstractmethod
    @classmethod
    def from_dict(cls: Type[T], params:Dict[str,Any]) -> T:
        """Returns an object of this class, initialized using the fields of a dict."""
        raise NotImplementedError()

class Circle(Primitive):
    """
    A Primitive that represents a circle.
    
    Attributes:
        center (ArrayPoint): The center of the circle in 2D space.
        radius (float): The radius of the circle.
    """
    center:ArrayPoint
    radius:float

    def __init__(self, center:PointLike, radius:float):
        self.center = np.array(center)  # type: ignore
        self.radius = radius
        self.boundingBox = BoundingBox(minX=center[0]-radius, minY=center[1]-radius,
                                       maxX=center[0]+radius, maxY=center[1]+radius)

    def contains(self, point:PointLike) -> bool:
        # print(point - self.center, np.linalg.norm(point - self.center))
        return np.linalg.norm(point - self.center) <= self.radius # type: ignore

    @classmethod
    def from_dict(cls, params:Dict[str,Any]):
        return cls(params["center"], params["radius"])

class Polygon:
    """
    A Primitive that represents a polygon.
    
    Attributes:
        vertices (Sequence[PointLike]): The list of vertices that defines this polygon.
    """

    def __init__(self, points:Sequence[PointLike]):
        self.vertices = points
        xs, ys = zip(*points)
        self.boundingBox = BoundingBox(min(xs), min(ys), max(xs), max(ys))
        print(self.boundingBox.minX, self.boundingBox.minY, self.boundingBox.maxX, self.boundingBox.maxY)


    def edges(self) -> Generator[Tuple[PointLike, PointLike], None, None]:
        """Returns a generator that yields all the edges of this polygon, as a tuple of two points."""
        num_verts = len(self.vertices)
        for i,vert in enumerate(self.vertices):
            yield vert, self.vertices[(i+1)%num_verts]

    def contains(self, point:PointLike) -> bool:
        intersects:Set[PointLike] = set()  # use a set to detect collisions with multiple edges (i.e for collisions at the vertices of the polygon)
        for edge in self.edges():
            intersect = lineRayIntersectionPoint(point, (1.,1.), edge[0], edge[1])
            if type(intersect) is bool:
                if intersect:
                    return True
            else:
                if np.array_equal(intersect, point):  # type: ignore
                    return True
                else:
                    intersects.add(tuple(intersect))  #type: ignore

        return len(intersects)%2 == 1
            
