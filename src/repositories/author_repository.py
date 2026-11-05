from database.database import get_connection
from models.author import Author

def _map(row) -> Author:
    return Author(*row)

def get_all() -> list[Author]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT author_id, first_name, second_name FROM Authors")
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]

def get_by_id(author_id: int) -> Author | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT author_id, first_name, second_name FROM Authors WHERE author_id = ?", (author_id,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None

def create(first_name: str, second_name: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO Authors (first_name, second_name) VALUES (?, ?)", (first_name, second_name))
    conn.commit()
    conn.close()

def delete(author_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM Authors WHERE author_id = ?", (author_id,))
    conn.commit()
    conn.close()