import numpy as np
from numpy.typing import NDArray

import scipy as sp
from matplotlib import patheffects
import matplotlib.pyplot as plt
import json

from typing import Sequence, Any, Dict

def inside(x, y, primitive):
  """
  Check if point (x,y) is inside the primitive
  
  Args:
    x (float): horizontal point position
    y (float): vertical point position
  Returns:
    True if (x,y) is inside the primitive, False case contrary
  """
  
  # You should implement your inside test here for all shapes   
  # for now, it only returns a false test

  return False

class Screen:
    ''' Creates a virtual basic screen

    Args:
        gdata (dict): dictionary containing screen size and scene description
    '''
    _width:int
    _height:int
    _scene:Sequence[Any]
    _image:NDArray[Any]

    def __init__(self, gdata:Dict[Any, Any]):
        self._width = gdata.get("width")  # type: ignore
        self._height = gdata.get("height")  # type: ignore
        self._scene = self.preprocess( gdata.get("scene") ) # type: ignore

        # Create white image with R, G, B channels
        self._image = 255 *  np.ones((self._height, self._width, 3), np.uint8) #type: ignore
        self.create_image()


    def preprocess(self, scene:Sequence[Any]) -> Sequence[Any]:
        ''' 
        '''
        preprop_scene:Sequence[Any] = []

        for primitive in scene:
            preprop_scene.append(primitive)

        return preprop_scene
        
    def rasterize(self) -> None:
        ''' Rasterize the primitives along the Screen    
        '''

        for primitive in self._scene:
            for w,h in primitive.boundingBox.getPixels():
                if primitive.contains((w+0.5, h+0.5)):  # add 0.5 to get the pixel's  center
                    im_x, im_y = w, self._height - (h + 1)
                    self._image[im_y, im_x] = (255, 0, 0)

from primitives import Circle, Polygon
screen = Screen({"width": 200, "height": 600, "scene": [Circle((100,300), 10.), Polygon([(50,50),(100,50),(100,100), (50,75)])]})
from PIL import Image
screen.rasterize()
img = Image.fromarray(screen._image).show()