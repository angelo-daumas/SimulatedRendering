import numpy as np
from .primitives import Primitive, Dict, PointLike, BoundingBox, Any
from linealg import PointLike, ArrayPoint

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

    def contains(self, point:PointLike) -> bool:
        # print(point - self.center, np.linalg.norm(point - self.center))
        return np.linalg.norm(point - self.center) <= self.radius # type: ignore

    @classmethod
    def from_dict(cls, params:Dict[str,Any]):
        return cls(params["center"], params["radius"])