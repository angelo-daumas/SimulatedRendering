from primitives.primitives import Primitive
from primitives.polygon import ConvexPolygon
import numpy as np
from numpy.typing import NDArray

import json

from typing import Sequence, Any, Dict, List, Type
import primitives

from primitives import Circle, Polygon, ConvexPolygon
class Screen:
    ''' Creates a virtual basic screen

    Args:
        gdata (dict): dictionary containing screen size and scene description
    '''
    _width:int
    _height:int
    _scene:Sequence[primitives.Primitive]
    _image:NDArray[np.uint8]

    def __init__(self, gdata:Dict[str, Any]):
        self._width = int(gdata["width"])
        self._height = int(gdata["height"])
        self._scene = self.parse_primitives(gdata["scene"])

        # Create white image with R, G, B channels
        self._image = 255 *  np.ones((self._height, self._width, 3), np.uint8) #type: ignore


    def parse_primitives(self, scene:Sequence[Dict[str, Any]]) -> List[primitives.Primitive]:
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
            preprop_scene.append(shape)

        return preprop_scene
        
    def rasterize(self) -> None:
        ''' Rasterize the primitives along the Screen    
        '''
        for primitive in self._scene:
            for w,h in primitive.boundingBox.pixels():
                if primitive.contains((w+0.5, h+0.5)):  # add 0.5 to get the pixel's  center
                    im_x, im_y = w, self._height - (h + 1)
                    self._image[im_y, im_x] = primitive.color


with open('tests/lion.json') as f:
    data = json.load(f)

# data = {"width": 200, "height": 600, "scene": [Circle((100,300), 10.), ConvexPolygon([(50,50),(100,50),(100,100), (50,75)])]}

screen = Screen(data)
import time
from PIL import Image
start = time.process_time()
screen.rasterize()
end = time.process_time()
print(f"Finished rasterizing. Took {end-start} seconds.")
img = Image.fromarray(screen._image).show()