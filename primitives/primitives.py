from typing import Any, Dict, TypeVar, Type
from linealg import AffineTransform, PointLike
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

    @classmethod
    @abc.abstractmethod
    def from_dict(cls: Type[T], params:Dict[str,Any]) -> T:
        """Returns an object of this class, initialized using the fields of a dict."""
        raise NotImplementedError()
