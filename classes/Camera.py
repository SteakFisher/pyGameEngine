from utils.types import Position, Rotation


class Camera:
    def __init__(self, pos: Position = dict(x=0, y=0, z=-3, w=1), rot: Rotation = dict(x=0, y=0, z=180)) -> None:
        self.pos: Position = pos
        self.rot: Rotation = rot

    def __str__(self) -> str:
        return f"Pos: {self.pos}, \nRot: {self.rot}"

    def translate(self, translation: Position) -> None:
        self.pos = translation

    def rotate(self, angle: Rotation) -> None:
        self.rot['x'] += angle['x']
        self.rot['y'] += angle['y']
        self.rot['z'] += angle['z']