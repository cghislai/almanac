from enum import Enum


class EventType(Enum):
    MOON_PHASE = "moon_phase"
    MOON_ZODIAC = "moon_zodiac"


class Body(Enum):
    EARTH = "earth",
    MOON = "moon",
    SUN = "sun"
