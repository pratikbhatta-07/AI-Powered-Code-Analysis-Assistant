from src.db.db import get_connection


def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cache (
            code_hash TEXT PRIMARY KEY,
            response  TEXT
        )
    """)
    conn.commit()
    conn.close()
