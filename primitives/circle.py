from typing import Optional
import numpy as np
from .primitives import Primitive, Dict, PointLike, BoundingBox, Any
from linealg import PointLike, ArrayPoint, AffineTransform

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
        self.center = np.array(center) # type: ignore
        self.radius = radius
        self.boundingBox = BoundingBox(minX=center[0]-radius, minY=center[1]-radius,
                                       maxX=center[0]+radius, maxY=center[1]+radius)
        self._transformation:Optional[AffineTransform] = None

    def contains(self, point:PointLike) -> bool:
        # print(point - self.center, np.linalg.norm(point - self.center))
        if self._transformation is not None:
            point = self._transformation.apply(point)
        return np.linalg.norm(point - self.center) <= self.radius # type: ignore

    @classmethod
    def from_dict(cls, params:Dict[str,Any]):
        return cls(params["center"], params["radius"])

    def transform(self, matrix: AffineTransform):
        self.boundingBox.transform(matrix)
        self._transformation = AffineTransform(np.linalg.inv(matrix.matrix))  # type: ignore
