from .deck import Deck
from .camera import Camera
from .beacon import Beacon

def custom_serializer(self):
    if isinstance(self, ViewerData):
        # return {"name": self.name, "height": self.height, "decks": [custom_serializer(deck) for deck in self.deck] }
        return {
            "name": self.name, 
            "height": self.height, 
            "deck": custom_serializer(self.deck),
            "camera": custom_serializer(self.camera) if self.camera is not None else None
        }
        # return {"name": self.name, "height": self.height }
    elif isinstance(self, Deck):
        return {
            "id": self.id, 
            "external_id": self.external_id, 
            "name": self.name, 
            "image_id": self.image_id,
            "beacons": [custom_serializer(beacon) for beacon in self.beacons]
        }
    elif isinstance(self, Beacon):
        return {
            "id": self.id, 
            "externalId": self.external_id,
            "name": self.name, 
            "macAddress": self.macAddress,
            "zone": self.zone,
            "radius": self.radius,
            "widthSegment": self.widthSegment,
            "heightSegment": self.heightSegment,
            "color": self.color,
            "signalRadius": self.signalRadius,
            "fadeSpeed": self.fadeSpeed,
            "expandSpeed": self.expandSpeed,
            "maxScale": self.maxScale,
            "deviceLocation": self.deviceLocation        
        }
    elif isinstance(self, Camera):
        return {
            "position": {
                "x": self.position.x,
                "y": self.position.y,
                "z": self.position.z
             }, 
            "lookAt": {
                "x": self.lookAt.x,
                "y": self.lookAt.y,
                "z": self.lookAt.z,
            }      
        }
    raise TypeError(f"Type {type(self)} is not serializable")

class ViewerData:
    def __init__(self, name, height, deck:Deck=None, camera:Camera=None):
        self.name = name
        self.height = height
        self.deck = deck
        self.camera = camera
        
    def to_json(self):
        return custom_serializer(self)

        