from dataclasses import asdict
from typing import Optional

from firebase_admin.db import Reference
from lms_hub.models.profile import Profile


def reconstruct_user_from_db(user_data: dict) -> Profile:
    return Profile(
        google_user_id=user_data["google_user_id"],
        user_id=user_data["user_id"],
        name=user_data["name"],
        email=user_data["email"],
        accounts={}
    )

class Database:
    def __init__(self, ref: Reference):
        self.root: Reference = ref

    def add_user(self, user: Profile):
        users_ref = self.root.child("users")
        user.user_id = users_ref.push().key
        users_ref.child(user.user_id).set(asdict(user))

    def delete_user(self, user_id: str):
        self.root.child(f"users/{user_id}").delete()

    def lookup_user_by_username(self, email: str) -> Optional[Profile]:
        users = self.root.child("users").get()
        if not users:
            return None

        for _, user in users.items():
            if user["email"] == email:
                return reconstruct_user_from_db(user)
        return None

    def lookup_user_by_email(self, email: str) -> Optional[Profile]:
        users = self.root.child("users").get()
        if not users:
            return None

        for _, user in users.items():
            if user["email"] == email:
                return reconstruct_user_from_db(user)
        return None

    def lookup_user_by_id(self, user_id: str) -> Optional[Profile]:
        loaded_user = self.root.child(f"users/{user_id}").get()
        if loaded_user:
            return reconstruct_user_from_db(loaded_user)
        return None
