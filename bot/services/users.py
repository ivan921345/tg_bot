from db import supabase


def add_user(tg_id: int, crosses_count: int, is_admin: bool):
    response = (
        supabase
        .table("users")
        .upsert(
            {
                "tg_id": tg_id,
                "is_admin": is_admin,
                "crosses_count": crosses_count,
            },
            on_conflict="tg_id",
        )
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
