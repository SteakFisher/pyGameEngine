from utils.types import Position, Rotation


class Camera:
    def __init__(self, pos: Position = Position(), rot: Rotation = Rotation()):
        self.pos = pos
        self.rot = rot

