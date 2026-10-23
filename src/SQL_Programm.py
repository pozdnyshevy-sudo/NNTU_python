import sqlite3

DB_NAME = "gym_inventory.db"

LIBRARY = {
    "roles": [
        "администратор",
        "тренер",
        "клиент",
    ],

    "clients": [
        ("Иванов Иван Иванович",     "клиент"),
        ("Петрова Анна Сергеевна",   "клиент"),
        ("Сидоров Пётр Алексеевич",  "клиент"),
        ("Кузнецова Мария Олеговна", "клиент"),
    ],

    "authors": [
        ("Смирнов Алексей Викторович", "администратор"),
        ("Волкова Елена Дмитриевна",   "тренер"),
        ("Орлов Дмитрий Павлович",     "тренер"),
    ],

    "inventory": [
        ("Свободные веса", "Гантели 10 кг",      "Смирнов Алексей Викторович"),
        ("Кардио",         "Беговая дорожка",    "Смирнов Алексей Викторович"),
        ("Фитнес",         "Коврик для йоги",    "Волкова Елена Дмитриевна"),
        ("Свободные веса", "Штанга олимпийская", "Орлов Дмитрий Павлович"),
        ("Функциональный", "Гиря 16 кг",         "Волкова Елена Дмитриевна"),
    ],

    "bookings": [
        ("Иванов Иван Иванович",     "Гантели 10 кг",      "2026-10-20"),
        ("Петрова Анна Сергеевна",   "Коврик для йоги",    "2026-10-21"),
        ("Сидоров Пётр Алексеевич",  "Беговая дорожка",    "2026-10-21"),
        ("Иванов Иван Иванович",     "Штанга олимпийская", "2026-10-22"),
        ("Кузнецова Мария Олеговна", "Гиря 16 кг",         "2026-10-23"),
    ],
}


def create_connection(db_name: str) -> sqlite3.Connection:
    conn = sqlite3.connect(db_name)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def create_tables(conn: sqlite3.Connection) -> None:
    conn.executescript("""
    DROP TABLE IF EXISTS Bookings;
    DROP TABLE IF EXISTS SportsEquipment;
    DROP TABLE IF EXISTS Authors;
    DROP TABLE IF EXISTS Users;
    DROP TABLE IF EXISTS Roles;

    CREATE TABLE Roles (
        role_id    INTEGER PRIMARY KEY AUTOINCREMENT,
        role_name  TEXT NOT NULL UNIQUE
    );

    CREATE TABLE Users (
        user_id    INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name  TEXT NOT NULL,
        role_id    INTEGER NOT NULL,
        FOREIGN KEY (role_id) REFERENCES Roles(role_id)
            ON UPDATE CASCADE ON DELETE RESTRICT
    );

    CREATE TABLE Authors (
        author_id  INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name  TEXT NOT NULL,
        role_id    INTEGER NOT NULL,
        FOREIGN KEY (role_id) REFERENCES Roles(role_id)
            ON UPDATE CASCADE ON DELETE RESTRICT
    );

    CREATE TABLE SportsEquipment (
        equipment_id   INTEGER PRIMARY KEY AUTOINCREMENT,
        view_inventory TEXT,
        equipment_name TEXT    NOT NULL,
        author_id      INTEGER NOT NULL,
        FOREIGN KEY (author_id) REFERENCES Authors(author_id)
            ON UPDATE CASCADE ON DELETE RESTRICT
    );

    CREATE TABLE Bookings (
        booking_id    INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id       INTEGER NOT NULL,
        equipment_id  INTEGER NOT NULL,
        booking_date  DATE NOT NULL,
        FOREIGN KEY (user_id) REFERENCES Users(user_id)
            ON UPDATE CASCADE ON DELETE CASCADE,
        FOREIGN KEY (equipment_id) REFERENCES SportsEquipment(equipment_id)
            ON UPDATE CASCADE ON DELETE CASCADE
    );
    """)
    conn.commit()


def get_id(conn: sqlite3.Connection, table: str, id_col: str,
           name_col: str, value: str) -> int:
    """Находит id записи по её названию/ФИО."""
    row = conn.execute(
        f"SELECT {id_col} FROM {table} WHERE {name_col} = ?", (value,)
    ).fetchone()
    if row is None:
        raise ValueError(f"В таблице {table} не найдено: {value}")
    return row[0]


def insert_test_data(conn: sqlite3.Connection, library: dict) -> None:
    """Записывает в базу все данные из LIBRARY."""
    conn.executemany(
        "INSERT INTO Roles (role_name) VALUES (?)",
        [(role,) for role in library["roles"]],
    )

    for full_name, role in library["clients"]:
        role_id = get_id(conn, "Roles", "role_id", "role_name", role)
        conn.execute(
            "INSERT INTO Users (full_name, role_id) VALUES (?, ?)",
            (full_name, role_id),
        )

    for full_name, role in library["authors"]:
        role_id = get_id(conn, "Roles", "role_id", "role_name", role)
        conn.execute(
            "INSERT INTO Authors (full_name, role_id) VALUES (?, ?)",
            (full_name, role_id),
        )

    for view, name, author in library["inventory"]:
        author_id = get_id(conn, "Authors", "author_id", "full_name", author)
        conn.execute(
            "INSERT INTO SportsEquipment (view_inventory, equipment_name, author_id) "
            "VALUES (?, ?, ?)",
            (view, name, author_id),
        )

    for client, equipment, date in library["bookings"]:
        user_id = get_id(conn, "Users", "user_id", "full_name", client)
        equipment_id = get_id(conn, "SportsEquipment", "equipment_id",
                              "equipment_name", equipment)
        conn.execute(
            "INSERT INTO Bookings (user_id, equipment_id, booking_date) "
            "VALUES (?, ?, ?)",
            (user_id, equipment_id, date),
        )

    conn.commit()


def show_data(conn: sqlite3.Connection) -> None:
    for table in ("Roles", "Users", "Authors", "SportsEquipment", "Bookings"):
        print(f"\n=== {table} ===")
        for row in conn.execute(f"SELECT * FROM {table}"):
            print(row)

    print("\n=== Бронирования (с JOIN) ===")
    query = """
        SELECT b.booking_id, u.full_name, e.equipment_name, b.booking_date
        FROM Bookings b
        JOIN Users u           ON u.user_id = b.user_id
        JOIN SportsEquipment e ON e.equipment_id = b.equipment_id
        ORDER BY b.booking_date;
    """
    for row in conn.execute(query):
        print(row)


if __name__ == "__main__":
    conn = create_connection(DB_NAME)
    try:
        create_tables(conn)
        insert_test_data(conn, LIBRARY)
        show_data(conn)
    finally:
        conn.close()