from src.db.db import get_connection

def get_cached_response(code_hash) :
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT response FROM cache WHERE code_hash = ? ", (code_hash,)
    )
    row = cursor.fetchone()
    conn.close()

    return row[0] if row else None

def save_response(code_hash, response) :
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT OR REPLACE INTO cache (code_hash, response) VALUES (?, ?)", (code_hash, response)
    )

    conn.commit()
    conn.close()