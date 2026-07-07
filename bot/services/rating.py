from db import supabase

def get_top_users():
    response = (
        supabase
        .table("users")
        .select("id, tg_id, is_admin, crosses_count, username, full_name")
        .order("crosses_count", desc=True)
        .limit(10)
        .execute()
    )

    return response.data