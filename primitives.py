import numpy as np
from typing import Sequence, Any, Optional, Union, Generator, Tuple, Set
from numpy.typing import NDArray

#ArrayPoint = np.ndarray[Any, np.dtype[np.float64]]
ArrayPoint = NDArray[np.float64]
Matrix = NDArray[np.float64]
PointLike = Union[ArrayPoint, Tuple[float,float]]


class BoundingBox:

    def __init__(self, minX:float = 0., minY:float=0., maxX:float=0., maxY:float=0.):
        self.minX = minX
        self.maxX = maxX
        self.minY = minY
        self.maxY = maxY

    def transform(self, matrix:Matrix):
        matrix
        pass

    def getPixels(self):
        for x in range(int(self.minX), 1+int(self.maxX)):
            yield from ((x,y) for y in range(int(self.minY), 1+int(self.maxY)))

class Primitive:


    def contains(self, point:PointLike):
        point
        return False

    @property
    def boundingBox(self):
        return None


class Circle:
    center:ArrayPoint
    radius:float
    boundingBox:BoundingBox

    def __init__(self, center:PointLike, radius:float):
        self.center = np.array(center)  # type: ignore
        self.radius = radius
        self.boundingBox = BoundingBox(minX=center[0]-radius, minY=center[1]-radius,
                                       maxX=center[0]+radius, maxY=center[1]+radius)

    def contains(self, point:PointLike) -> bool:
        # print(point - self.center, np.linalg.norm(point - self.center))
        return np.linalg.norm(point - self.center) <= self.radius # type: ignore

class Polygon:

    def __init__(self, points:Sequence[PointLike]):
        self.vertices = points
        xs, ys = zip(*points)
        self.boundingBox = BoundingBox(min(xs), min(ys), max(xs), max(ys))
        print(self.boundingBox.minX, self.boundingBox.minY, self.boundingBox.maxX, self.boundingBox.maxY)


    def edges(self) -> Generator[Tuple[PointLike, PointLike], None, None]:
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
            
            



def normamlize(vector:Sequence[Any], dtype:Optional[type]=None) -> ArrayPoint:
   return np.array(vector, dtype=dtype)/(np.linalg.norm(vector)) #type: ignore

def lineRayIntersectionPoint(rayOrigin:PointLike, rayDirection:PointLike, point1:PointLike, point2:PointLike) -> Union[ArrayPoint, bool]:
    # Convert to numpy arrays
    rayOrigin = np.array(rayOrigin, dtype=np.float64) # type: ignore
    rayDirection = normamlize(rayDirection, dtype=np.float64) # type: ignore
    point1 = np.array(point1, dtype=np.float64) # type: ignore
    point2 = np.array(point2, dtype=np.float64) # type: ignore

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