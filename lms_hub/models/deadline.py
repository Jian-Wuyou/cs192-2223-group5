from datetime import datetime
from dataclasses import asdict, dataclass
from json import JSONEncoder

from .learning_env_class import Platform

@dataclass
class Deadline:
    """
    Dataclass for a deadline.
    """
    course_name: str            # Course to which the deadline belongs
    course_url: str             # Course link
    name: str                   # Name of the assignment
    url: str                    # URL to the assignment, if any
    timestamp: int              # Deadline date, in Unix timestamp format
    description: str
    platform: Platform          # Platform that the course is on
    moduletype: str = None


class DeadlineEnc(JSONEncoder):
    """
    JSONEncoder for Deadline objects.
    """
    def default(self, o):
        if isinstance(o, Deadline):
            return asdict(o)
        return JSONEncoder.default(self, o)

def sort_deadlines(raw_deadlines: list[Deadline]) -> dict[str, any]:
    # Sort deadlines by date
    deadlines = []
    for deadline in raw_deadlines:
        # Parse date from Unix timestamp
        if deadline.timestamp != 0:
            parsed_date = datetime.utcfromtimestamp(deadline.timestamp)
            parsed_date_str = parsed_date.strftime("%Y-%m-%d")
        else:
            parsed_date_str = "0"

        deadline_dict = asdict(deadline)
        deadline_dict['date'] = parsed_date_str
        deadlines.append(deadline_dict)
    
    # Sort deadlines in ascending order
    deadlines.sort(key=lambda x: x['timestamp'])

    return deadlines