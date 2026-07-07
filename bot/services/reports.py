from db import supabase

def add_report(tg_id:str, first_photo: str,second_photo: str):
    response = (
        supabase
        .table("reports")
        .upsert(
            {
                "tg_id": tg_id,
                "first_photo":first_photo,
                "second_photo":second_photo,
                "status":"PENDING"
            },
         )
        .execute()
    )

    return response.data

def get_pending_reports():
    response = (
        supabase
        .table("reports")
        .select(
            "*"
        )
        .eq("status", "PENDING")
        .execute()
    )
    return response.data
def get_pending_reports_count():
    response = (
        supabase
        .table("reports")
        .select("*", count="exact", head=True)
        .eq("status", "PENDING")
        .execute()
    )
    return response.count
