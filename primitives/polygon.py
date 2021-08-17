from .primitives import Primitive, BoundingBox
from typing import Sequence, Dict, Any
from linealg import PointLike, LineSegment, AffineTransform

class Polygon(Primitive):
    """
    A Primitive that represents a polygon. Uses the Winding Number method to check whether a point is contained within it.
    
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
        # Winding Number method
        Y = point[1]
        winding = 0

        for edge in self.edges():
            orient = edge.orient(point)

            if orient == edge.Side.COLLINEAR and BoundingBox(*edge.bounds()).contains(point):
                return True

            if edge.start[1] <= Y:
                if edge.end[1] > Y:
                    if orient == edge.Side.LEFT:
                        winding += 1
            else:
                if edge.end[1] <= Y:
                    if orient == edge.Side.RIGHT:
                        winding -= 1
        
        return bool(winding)

    def transform(self, matrix: AffineTransform):
        self.boundingBox.transform(matrix)
        for i,vert in enumerate(self.vertices):
            self.vertices[i] = matrix.apply(vert)

    @classmethod
    def from_dict(cls, params:Dict[str,Any]):
        return cls(params["vertices"])

class ConvexPolygon(Polygon):
    """This Polygon represents a ConvexPolygon and uses a different method to check whether a point is contained within it."""
    
    def contains(self, point:PointLike) -> bool:
        # Equivalent to cross-product check for the triangle, but generalized to N-sided convex polygons.
        # There is no need for a triangle-specific implementation, as it would look exactly like this one.
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