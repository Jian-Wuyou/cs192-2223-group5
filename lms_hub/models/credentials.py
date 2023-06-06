from dataclasses import dataclass, field
from abc import ABC, abstractmethod

@dataclass
class LearningEnvCredentials(ABC):
    ...

@dataclass
class GoogleCredentials(LearningEnvCredentials):
    # Associated user ID
    user_id: str = ""

    # Associated e-mail address
    email: str = ""

    # OAuth2 access token
    token: str = ""

    # OAuth2 refresh token
    refresh_token: str = ""

    # OAuth2 token URI
    token_uri: str = ""

    # OAuth2 client ID
    client_id: str = ""

    # OAuth2 scopes
    scopes: List[str] = field(default_factory=list)

    # OpenID token
    id_token: str = ""

    # OAuth2 expiry
    expiry: str = ""

@dataclass
class UVLeCredentials(LearningEnvCredentials):
    username: str
    token: str
    server: str