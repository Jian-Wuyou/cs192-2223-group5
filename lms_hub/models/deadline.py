from datetime import datetime
from dataclasses import asdict, dataclass
from typing import List

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
    platform: str               # Platform that the course is on
    moduletype: str = None

def sort_deadlines(raw_deadlines: List[Deadline]) -> List[dict[str, any]]:
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