import sqlite3

ROLES = ["администратор", "тренер", "клиент"]

CLIENTS = [
    "Иванов Иван Иванович",
    "Петрова Анна Сергеевна",
    "Сидоров Пётр Алексеевич",
    "Кузнецова Мария Олеговна",
]

AUTHORS = [
    ("Смирнов Алексей Викторович", "администратор"),
    ("Волкова Елена Дмитриевна",   "тренер"),
    ("Орлов Дмитрий Павлович",     "тренер"),
]

EQUIPMENT = [
    ("Свободные веса", "Гантели 10 кг",      "Смирнов Алексей Викторович"),
    ("Кардио",         "Беговая дорожка",    "Смирнов Алексей Викторович"),
    ("Фитнес",         "Коврик для йоги",    "Волкова Елена Дмитриевна"),
    ("Свободные веса", "Штанга олимпийская", "Орлов Дмитрий Павлович"),
    ("Функциональный", "Гиря 16 кг",         "Волкова Елена Дмитриевна"),
]

BOOKINGS = [
    ("Иванов Иван Иванович",     "Гантели 10 кг",      "2026-10-20"),
    ("Петрова Анна Сергеевна",   "Коврик для йоги",    "2026-10-21"),
    ("Сидоров Пётр Алексеевич",  "Беговая дорожка",    "2026-10-21"),
    ("Иванов Иван Иванович",     "Штанга олимпийская", "2026-10-22"),
    ("Кузнецова Мария Олеговна", "Гиря 16 кг",         "2026-10-23"),
]

SCHEMA = """
DROP TABLE IF EXISTS Bookings;
DROP TABLE IF EXISTS SportsEquipment;
DROP TABLE IF EXISTS Authors;
DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Roles;

CREATE TABLE Roles (
    role_id   INTEGER PRIMARY KEY,
    role_name TEXT NOT NULL UNIQUE
);
CREATE TABLE Users (
    user_id   INTEGER PRIMARY KEY,
    full_name TEXT NOT NULL,
    role_id   INTEGER NOT NULL REFERENCES Roles(role_id)
);
CREATE TABLE Authors (
    author_id INTEGER PRIMARY KEY,
    full_name TEXT NOT NULL,
    role_id   INTEGER NOT NULL REFERENCES Roles(role_id)
);
CREATE TABLE SportsEquipment (
    equipment_id   INTEGER PRIMARY KEY,
    view_inventory TEXT,
    equipment_name TEXT NOT NULL,
    author_id      INTEGER NOT NULL REFERENCES Authors(author_id)
);
CREATE TABLE Bookings (
    booking_id   INTEGER PRIMARY KEY,
    user_id      INTEGER NOT NULL REFERENCES Users(user_id) ON DELETE CASCADE,
    equipment_id INTEGER NOT NULL REFERENCES SportsEquipment(equipment_id) ON DELETE CASCADE,
    booking_date DATE NOT NULL
);
"""


def fill(conn):
    conn.executemany("INSERT INTO Roles (role_name) VALUES (?)",
                     [(r,) for r in ROLES])

    conn.executemany("""INSERT INTO Users (full_name, role_id) VALUES
        (?, (SELECT role_id FROM Roles WHERE role_name = 'клиент'))""",
        [(c,) for c in CLIENTS])

    conn.executemany("""INSERT INTO Authors (full_name, role_id) VALUES
        (?, (SELECT role_id FROM Roles WHERE role_name = ?))""", AUTHORS)

    conn.executemany("""INSERT INTO SportsEquipment (view_inventory, equipment_name, author_id) VALUES
        (?, ?, (SELECT author_id FROM Authors WHERE full_name = ?))""", EQUIPMENT)

    conn.executemany("""INSERT INTO Bookings (user_id, equipment_id, booking_date) VALUES
        ((SELECT user_id FROM Users WHERE full_name = ?),
         (SELECT equipment_id FROM SportsEquipment WHERE equipment_name = ?), ?)""", BOOKINGS)


def show(conn):
    for table in ("Roles", "Users", "Authors", "SportsEquipment", "Bookings"):
        print(f"\n=== {table} ===")
        for row in conn.execute(f"SELECT * FROM {table}"):
            print(row)

    print("\n=== Бронирования (с JOIN) ===")
    for row in conn.execute("""
        SELECT b.booking_id, u.full_name, e.equipment_name, b.booking_date
        FROM Bookings b
        JOIN Users u           ON u.user_id = b.user_id
        JOIN SportsEquipment e ON e.equipment_id = b.equipment_id
        ORDER BY b.booking_date"""):
        print(row)


conn = sqlite3.connect("gym_inventory.db")
conn.execute("PRAGMA foreign_keys = ON")
conn.executescript(SCHEMA)
fill(conn)
conn.commit()
show(conn)
conn.close()