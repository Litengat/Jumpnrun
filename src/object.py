from collision import Collision
from render import Renderer

class Object(Collision, Renderer):
    x: int
    y: int
    z: int
    width: int
    height: int
    z_render: int
    

    def render():
        pass