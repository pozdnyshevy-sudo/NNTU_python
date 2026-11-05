from database.database import get_connection
from models.user import User

def _map(row) -> User:
    return User(*row)

def get_all() -> list[User]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT u.user_id, u.first_name, u.second_name, u.login, u.password, u.role_id, r.role_name
        FROM Users u JOIN Roles r ON u.role_id = r.role_id
    """)
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]

def get_by_id(user_id: int) -> User | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT u.user_id, u.first_name, u.second_name, u.login, u.password, u.role_id, r.role_name
        FROM Users u JOIN Roles r ON u.role_id = r.role_id
        WHERE u.user_id = ?
    """, (user_id,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None

def get_by_login(login: str) -> User | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT u.user_id, u.first_name, u.second_name, u.login, u.password, u.role_id, r.role_name
        FROM Users u JOIN Roles r ON u.role_id = r.role_id
        WHERE u.login = ?
    """, (login,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None

def create(first_name: str, second_name: str, login: str, password: str, role_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO Users (first_name, second_name, login, password, role_id)
        VALUES (?, ?, ?, ?, ?)
    """, (first_name, second_name, login, password, role_id))
    conn.commit()
    conn.close()

def delete(user_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM Users WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()