from enum import Enum

class ComplainTypes_Enum(str,Enum):
    Traffic_Voilation="Traffic Violation",
    Road_Damage="Road Damage",
    Public_Transport="Public Transport",
    Parking_Issue="Parking Issue",
    Noise_Pollution="Noise Pollution",


ROAD_TYPES = [
    "Road Damage",
    "Noise Pollution"
]

TRANSPORT_TYPES = [
    "Traffic Violation",
    "Public Transport",
    "Parking Issue"
]
