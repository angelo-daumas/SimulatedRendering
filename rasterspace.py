from typing import TypeVar, Generic
import numpy as np

T = TypeVar('T')

class RasterSpace(Generic[T]):
    __slots__ = ('__width', '__height', '__background', '__image')

    def __init__(self, width:int, height:int, background:T):
        self.__width = width
        self.__height = height
        self.__background = background
        self.__image = np.array(background, np.uint8) * np.ones((height, width, len(background)), np.uint8)  #type: ignore

    @property
    def width(self) -> int:
        return self.__width

    @property
    def height(self) -> int:
        return self.__height

    @property
    def background(self) -> T:
        return self.__background

    def __getitem__(self, x:int, y:int) -> T:
        return self.__image[x, y] # type: ignore

    def __setitem__(self, x:int, y:int, v:T) -> None:
        self.__image[x,y] = v  # type: ignore


from PIL import Image
import colorspaces
white = colorspaces.RGB(255, 255, 255)
a = Image.fromarray(RasterSpace[colorspaces.RGB](200, 600, white)._RasterSpace__image) # type: ignore