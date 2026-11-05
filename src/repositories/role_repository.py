from database.database import get_connection
from models.role import Role

def _map(row) -> Role:
    return Role(*row)

def get_all() -> list[Role]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT role_id, role_name FROM Roles")
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]

def get_by_id(role_id: int) -> Role | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT role_id, role_name FROM Roles WHERE role_id = ?", (role_id,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None