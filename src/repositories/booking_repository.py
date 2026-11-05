from database.database import get_connection
from models.booking import Booking
from datetime import date

def _map(row) -> Booking:
    return Booking(*row)

def get_all() -> list[Booking]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT b.booking_id, b.user_id, b.equipment_id, b.booking_date, b.status,
               u.first_name || ' ' || u.second_name, e.equipment_name
        FROM Bookings b
        JOIN Users u ON b.user_id = u.user_id
        JOIN SportsEquipment e ON b.equipment_id = e.equipment_id
    """)
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]

def get_by_id(booking_id: int) -> Booking | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT b.booking_id, b.user_id, b.equipment_id, b.booking_date, b.status,
               u.first_name || ' ' || u.second_name, e.equipment_name
        FROM Bookings b
        JOIN Users u ON b.user_id = u.user_id
        JOIN SportsEquipment e ON b.equipment_id = e.equipment_id
        WHERE b.booking_id = ?
    """, (booking_id,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None

def create(user_id: int, equipment_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO Bookings (user_id, equipment_id, booking_date, status)
        VALUES (?, ?, ?, 'active')
    """, (user_id, equipment_id, date.today().isoformat()))
    conn.commit()
    conn.close()

def return_booking(booking_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE Bookings SET status = 'returned' WHERE booking_id = ?", (booking_id,))
    conn.commit()
    conn.close()

def cancel(booking_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE Bookings SET status = 'cancelled' WHERE booking_id = ?", (booking_id,))
    conn.commit()
    conn.close()

def delete(booking_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM Bookings WHERE booking_id = ?", (booking_id,))
    conn.commit()
    conn.close()