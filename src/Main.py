import sqlite3

DB_NAME = "gym_inventory.db"


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


def insert_test_data(conn: sqlite3.Connection) -> None:
    conn.executescript("""
                       INSERT INTO Roles (role_name)VALUES
        ('администратор'),
        ('тренер'),
        ('клиент');

    INSERT INTO Users (full_name, role_id) VALUES
        ('Иванов Иван Иванович', 3),
        ('Петрова Анна Сергеевна', 3),
        ('Сидоров Пётр Алексеевич', 3),
        ('Кузнецова Мария Олеговна', 2);

    INSERT INTO Authors (full_name, role_id) VALUES
        ('Смирнов Алексей Викторович', 1),
        ('Волкова Елена Дмитриевна', 2),
        ('Орлов Дмитрий Павлович', 2);

    INSERT INTO SportsEquipment (view_inventory, equipment_name, author_id) VALUES
        ('Свободные веса',  'Гантели 10 кг',        1),
        ('Кардио',          'Беговая дорожка',      1),
        ('Фитнес',          'Коврик для йоги',      2),
        ('Свободные веса',  'Штанга олимпийская',   3),
        ('Функциональный', 'Гиря 16 кг', 2);

    INSERT INTO Bookings (user_id, equipment_id, booking_date) VALUES
        (1, 1, '2026-10-20'),
        (2, 3, '2026-10-21'),
        (3, 2, '2026-10-21'),
        (1, 4, '2026-10-22'),
        (4, 5, '2026-10-23');
    """)
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
        insert_test_data(conn)
        show_data(conn)
    finally:
        conn.close()
