import numpy as np
from numpy.typing import NDArray
from typing import Tuple, Union, NamedTuple
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
        self.matrix = np.array(matrix)  # type: ignore
        pass

    def apply(self, point:PointLike) -> PointLike:
        """Applies the transformation to a 2D point, and returns the resulting 2D point."""
        return tuple((self.matrix @ [*point, 1.])[0:2])  # type: ignore
