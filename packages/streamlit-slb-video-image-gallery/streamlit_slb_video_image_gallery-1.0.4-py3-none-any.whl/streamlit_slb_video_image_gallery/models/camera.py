
from .coordinate import Coordinate

class Camera:
    def __init__(self, id, name, position: Coordinate, lookAt: Coordinate):
        self.id = id
        self.name = name
        self.position: Coordinate = position
        self.lookAt: Coordinate = lookAt    