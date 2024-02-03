from utils.types import Position, Rotation


class Camera:
    def __init__(self, pos: Position = dict(x=0, y=0, z=0), rot: Rotation = dict(x=1, y=0, z=0)) -> None:
        self.pos: Position = pos
        self.rot: Rotation = rot

    def __str__(self) -> str:
        return f"Pos: {self.pos}, \nRot: {self.rot}"
