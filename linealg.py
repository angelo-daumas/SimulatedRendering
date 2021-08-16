import numpy as np
from numpy.typing import NDArray
from typing import Tuple, Union, Any, Optional, Sequence, NamedTuple
from enum import IntEnum

Matrix = NDArray[np.float64]
ArrayPoint = NDArray[np.float64]
Vector = NDArray[np.float64]
PointLike = Union[ArrayPoint, Tuple[float,float]]

class LineSegment(NamedTuple):
    start: PointLike
    end: PointLike

    class Side(IntEnum):
        """
        An enum for use if LineSegment.orient().

        LEFT: Point is to the left of the LineSegment.
        RIGHT: Point is to the right of the LineSegment.
        COLLINEAR: Point is in the same line as the LineSegment.
        """
        LEFT = -1
        COLLINEAR = 0
        RIGHT = 1

    def vector(self) -> Vector:
        return np.subtract(self.start, self.end)

    def orient(self, point:PointLike) -> Side:
        vector = np.subtract(point, self.start)
        return LineSegment.Side(np.sign(np.cross(self.vector(), vector)))  # type: ignore

    def bounds(self) -> Tuple[float,float,float,float]:
        xs, ys = zip(*self)
        return min(xs), min(ys), max(xs), max(ys)

class AffineTransform:
    """
    A class that represents a 2D affine transformation.

    Args:
        matrix (3x3 Matrix): The matrix that represents the transformation mathematically.
    
    Attributes:
        matrix (3x3 Matrix): The matrix that represents the transformation mathematically.
    """
    matrix:Matrix

    def __init__(self, matrix:Matrix) -> None:
        self.matrix = matrix
        pass

    def apply(self, point:PointLike) -> ArrayPoint:
        """Applies the transformation to a 2D point, and returns the resulting 2D point."""
        return (self.matrix * [*point, 1.])[0:2]


def normalize(vector:Sequence[Any], dtype:Optional[type]=None) -> ArrayPoint:
    """Normalizes a vector, returning a unit vector."""
    return np.array(vector, dtype=dtype)/(np.linalg.norm(vector)) #type: ignore

def lineRayIntersectionPoint(rayOrigin:PointLike, rayDirection:PointLike, segment:LineSegment) -> Union[ArrayPoint, bool]:
    # Convert to numpy arrays
    rayOrigin = np.array(rayOrigin, dtype=np.float64) # type: ignore
    rayDirection = normalize(rayDirection, dtype=np.float64) # type: ignore
    point1 = np.array(segment.start, dtype=np.float64) # type: ignore
    point2 = np.array(segment.end, dtype=np.float64) # type: ignore

    # Ray-Line Segment Intersection Test in 2D
    # http://bit.ly/1CoxdrG
    v1 = rayOrigin - point1
    v2 = point2 - point1
    v3 = np.array([-rayDirection[1], rayDirection[0]])  #type: ignore
    
    if np.cross(v2, rayDirection-rayOrigin) == 0.: #type: ignore
        return True

    t1 =  np.cross(v2, v1)/ np.dot(v2, v3) #type: ignore
    t2 = np.dot(v1, v3) / np.dot(v2, v3) #type: ignore

    if t1 >= 0.0 and t2 >= 0.0 and t2 <= 1.0:
        return rayOrigin + t1 * rayDirection #type: ignore
    return False
