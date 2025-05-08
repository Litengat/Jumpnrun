from src.collision import Collision


class Object(Collision):
    x: int
    y: int
    z: int
    width: int
    height: int
    z_render: int

    def render():
        pass