from typing import TypedDict

class User(TypedDict):
    id: int
    tg_id: int
    is_admin: bool
    crosses_count: int
    username: str | None
    full_name: str | None