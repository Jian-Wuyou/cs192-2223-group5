from dataclasses import dataclass, asdict
from json import JSONEncoder

# Supported Learning Management Systems
class Platform:
    UVLE = 'uvle'
    GCLASS = 'auto'

@dataclass
class LearningEnvClass:
    """
    Abstract dataclass for a learning environment class object.
    """

    class_id: str       # Class ID
    platform: str
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