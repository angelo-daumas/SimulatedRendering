from typing import Sequence, Any, Dict, List, Type
import numpy as np
from numpy.typing import NDArray
from primitives import Primitive, Circle, Polygon, ConvexPolygon
from linealg import AffineTransform

class RasterSpace:
    ''' Creates a virtual basic screen

    Args:
        gdata (dict): dictionary containing screen size and scene description
    '''
    _width:int
    _height:int
    _scene:Sequence[Primitive]
    image:NDArray[np.uint8]

    def __init__(self, gdata:Dict[str, Any]):
        self._width = int(gdata["width"])
        self._height = int(gdata["height"])
        self._scene = self.parse_primitives(gdata["scene"])

        # Create white image with R, G, B channels
        self.image = 255 *  np.ones((self._height, self._width, 3), np.uint8) #type: ignore


    def parse_primitives(self, scene:Sequence[Dict[str, Any]]) -> List[Primitive]:
        ''' 
        '''
        preprop_scene:List[Any] = []

        for primitive in scene:
            primitive_type:Type[Primitive] = {
                "circle":Circle, 
                "polygon":Polygon, 
                "triangle":ConvexPolygon
                }[primitive["shape"]]
            shape = primitive_type.from_dict(primitive)
            shape.color = primitive["color"]
            if "xform" in primitive:
                shape.transform(AffineTransform(primitive["xform"]))
            preprop_scene.append(shape)

        return preprop_scene
        
    def rasterize(self) -> None:
        ''' Rasterize the primitives along the Screen    
        '''
        for primitive in self._scene:
            for w,h in primitive.boundingBox.pixels():
                if primitive.contains((w+0.5, h+0.5)):  # add 0.5 to get the pixel's  center
                    im_x, im_y = w, self._height - (h + 1)
                    self.image[im_y, im_x] = primitive.color