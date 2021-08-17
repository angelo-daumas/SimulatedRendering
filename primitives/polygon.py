import numpy as np
from .primitives import Primitive, BoundingBox
from typing import Set, Sequence, Dict, Any
from linealg import PointLike, lineRayIntersectionPoint, LineSegment, AffineTransform

class Polygon(Primitive):
    """
    A Primitive that represents a polygon.
    
    Attributes:
        vertices (Sequence[PointLike]): The list of vertices that defines this polygon.
    """

    def __init__(self, points:Sequence[PointLike]):
        self.vertices = list(points)
        xs, ys = (sorted(dim) for dim in zip(*points))
        self.boundingBox = BoundingBox(xs[0], ys[0], xs[-1], ys[-1])


    def edges(self):
        """Returns a generator that yields all the edges of this polygon."""
        num_verts = len(self.vertices)
        for i,vert in enumerate(self.vertices):
            yield LineSegment(vert, self.vertices[(i+1)%num_verts])

    def contains(self, point:PointLike) -> bool:
        intersects:Set[PointLike] = set()  # use a set to detect collisions with multiple edges (i.e for collisions at the vertices of the polygon)
        for edge in self.edges():
            intersect = lineRayIntersectionPoint(point, (1.,1.), edge)
            if type(intersect) is bool:
                if intersect:
                    return True
            else:
                if np.array_equal(intersect, point):  # type: ignore
                    return True
                else:
                    intersects.add(tuple(intersect))  #type: ignore

        return len(intersects)%2 == 1
    
    def transform(self, matrix: AffineTransform):
        self.boundingBox.transform(matrix)
        for i,vert in enumerate(self.vertices):
            self.vertices[i] = matrix.apply(vert)

    @classmethod
    def from_dict(cls, params:Dict[str,Any]):
        return cls(params["vertices"])

class ConvexPolygon(Polygon):
    # There is no need for a triangle-specific implementation, as this is already just as fast.

    def contains(self, point:PointLike) -> bool:
        # Equivalent to cross-product check for the triangle, but generalized to N-sided convex polygons.
        edges = self.edges()
        edge = next(edges)
        orient = edge.orient(point)
        if orient is LineSegment.Side.COLLINEAR:
                return BoundingBox(*edge.bounds()).contains(point)

        for edge in edges:
            o = edge.orient(point)

            if o != orient:
                return o is LineSegment.Side.COLLINEAR and BoundingBox(*edge.bounds()).contains(point)

        return True