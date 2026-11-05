from database.database import get_connection
from models.equipment import SportsEquipment

def _map(row) -> SportsEquipment:
    return SportsEquipment(*row)

def get_all() -> list[SportsEquipment]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT e.equipment_id, e.view_inventory, e.equipment_name, e.author_id,
               a.first_name || ' ' || a.second_name
        FROM SportsEquipment e JOIN Authors a ON e.author_id = a.author_id
    """)
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]

def get_by_id(equipment_id: int) -> SportsEquipment | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT e.equipment_id, e.view_inventory, e.equipment_name, e.author_id,
               a.first_name || ' ' || a.second_name
        FROM SportsEquipment e JOIN Authors a ON e.author_id = a.author_id
        WHERE e.equipment_id = ?
    """, (equipment_id,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None

def create(view_inventory: str, equipment_name: str, author_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO SportsEquipment (view_inventory, equipment_name, author_id)
        VALUES (?, ?, ?)
    """, (view_inventory, equipment_name, author_id))
    conn.commit()
    conn.close()

def delete(equipment_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM SportsEquipment WHERE equipment_id = ?", (equipment_id,))
    conn.commit()
    conn.close()