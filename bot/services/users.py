from db import supabase

from utils.helpers import User

def add_user(tg_id: int, username: str, full_name: str):
    response = (
        supabase.table("users").upsert(
        {
            "tg_id": tg_id,
            "username": username,
            "full_name": full_name,
            "is_admin": False,
        },
        on_conflict="tg_id"
        ).execute()
    )

    return response.data


def get_all_users() -> list[User]:
    response = (
        supabase
        .table("users")
        .select("id, tg_id, is_admin, crosses_count, username, full_name")
        .order("crosses_count")
        .execute()
    )

    return response.data

def get_all_user_ids() -> list[int]:
    response = (
        supabase
        .table("users")
        .select("tg_id")
        .eq("is_admin", False)
        .execute()
    )


    return [row["tg_id"] for row in response.data]

def get_user_crosses_count(tg_id:int) -> int:
    response = (
        supabase
        .table("users")
        .select("crosses_count")
        .eq("is_admin", False)
        .execute()
    )


    if len(response.data)!=0:
        return response.data[0]["crosses_count"]
    else:
        return 0
    

def get_user_by_tg_id( tg_id:int) -> int:
    response = (
        supabase
        .table("users")
        .select("tg_id")
        .eq("tg_id", tg_id)
        .execute()
    )

    if len(response.data)!=0:
        return response.data[0]["tg_id"]
    else:
        return -1


def get_admin_ids() -> list[int]:
    response = (
        supabase
        .table("users")
        .select("tg_id")
        .eq("is_admin", True)
        .execute()
    )

    
    return [row["tg_id"] for row in response.data]
