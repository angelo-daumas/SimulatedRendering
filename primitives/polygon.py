import numpy as np
from .primitives import Primitive, BoundingBox
from typing import Set, Sequence, Dict, Any
from linealg import PointLike, lineRayIntersectionPoint

class Polygon(Primitive):
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


    def edges(self):
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
    
    @classmethod
    def from_dict(cls, params:Dict[str,Any]):
        return cls(params["vertices"])