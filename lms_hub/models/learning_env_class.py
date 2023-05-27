from dataclasses import dataclass, asdict
from json import JSONEncoder
from enum import StrEnum, auto

# Supported Learning Management Systems
class Platform(StrEnum):
    UVLE = auto()
    GCLASS = auto()

@dataclass
class LearningEnvClass:
    """
    Abstract dataclass for a learning environment class object.
    """

    class_id: str       # Class ID
    platform: Platform
    name: str           # Class name
    description: str    # Class description
    url: str            # Class URL (link to external learning environment)

class LearningEnvClassEnc(JSONEncoder):
    """
    JSON encoder for LearningEnvClass
    """

    def default(self, o):
        if isinstance(o, LearningEnvClass):
            return asdict(o)
        return super().default(o)