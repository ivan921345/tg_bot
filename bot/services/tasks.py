from db import supabase
from datetime import datetime, timezone

def add_task(code_word: str,norm: int):
    response = (
        supabase
        .table("tasks")
        .upsert(
            {
                "code_word": code_word,
                "norm": norm,
            },
         )
        .execute()
    )

    return response.data

def get_last_task():
    response = (
        supabase
        .table("tasks")
        .select("*")
        .order("created_at", desc=True)
        .limit(1)
        .execute()
    )
    if response.count!=0:
        return response.data[0]
    else:
        return None
