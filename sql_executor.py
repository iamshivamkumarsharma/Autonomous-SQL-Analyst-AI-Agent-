from sqlalchemy import text
from db.engine import engine

def run_sql_safe(query):
    if not query.lower().startswith("select"):
        return {"success": False, "error": "Only SELECT allowed"}

    try:
        with engine.connect() as conn:
            rows = conn.execute(text(query)).fetchall()
        return {"success": True, "data": rows}
    except Exception as e:
        return {"success": False, "error": str(e)}
