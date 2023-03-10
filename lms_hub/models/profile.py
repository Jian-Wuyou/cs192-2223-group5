from dataclasses import dataclass

from lms_hub.models.credentials import LearningEnvCredentials

@dataclass
class Profile:
    google_user_id: str
    name: str
    email: str
    accounts: dict[str, LearningEnvCredentials]
    user_id: str = ""
    username: str = ""

    def __post_init__(self):
        self.is_authenticated = True
        self.is_active = True
        self.is_anonymous = False

    def get_id(self) -> str:
        return self.user_id

def from_google_jwt(jwt_info: dict[str, str | int | bool]) -> Profile:
    return Profile(
        google_user_id=jwt_info["sub"],
        name=jwt_info["name"],
        email=jwt_info["email"],
        accounts={}
    )
