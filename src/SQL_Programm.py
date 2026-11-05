import sqlite3

SQL = """
PRAGMA foreign_keys = ON;

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
    user_id     INTEGER PRIMARY KEY,
    first_name  TEXT NOT NULL,
    second_name TEXT NOT NULL,
    login       TEXT NOT NULL UNIQUE,
    password    TEXT NOT NULL,
    role_id     INTEGER NOT NULL REFERENCES Roles(role_id)
);

CREATE TABLE Authors (
    author_id   INTEGER PRIMARY KEY,
    first_name  TEXT NOT NULL,
    second_name TEXT NOT NULL
);

CREATE TABLE SportsEquipment (
    equipment_id   INTEGER PRIMARY KEY,
    view_inventory TEXT,
    equipment_name TEXT NOT NULL,
    author_id      INTEGER NOT NULL REFERENCES Authors(author_id)
);

CREATE TABLE Bookings (
    booking_id   INTEGER PRIMARY KEY,
    user_id      INTEGER NOT NULL REFERENCES Users(user_id),
    equipment_id INTEGER NOT NULL REFERENCES SportsEquipment(equipment_id),
    booking_date DATE NOT NULL,
    status       TEXT NOT NULL DEFAULT 'active'  -- active / returned / cancelled
);

INSERT INTO Roles VALUES
    (1, 'Администратор'), (2, 'Тренер'), (3, 'Клиент');

INSERT INTO Users VALUES
    (1, 'Иван', 'Иванов', 'ivanov', '123', 3),
    (2, 'Анна', 'Петрова', 'petrova', '123', 3),
    (3, 'Пётр', 'Сидоров', 'sidorov', '123', 3),
    (4, 'Мария', 'Кузнецова', 'kuznetsova', '123', 3),
    (5, 'Админ', 'Админов', 'admin', 'admin', 1),
    (6, 'Тренер', 'Тренеров', 'trainer', 'trainer', 2);

INSERT INTO Authors VALUES
    (1, 'Алексей', 'Смирнов'),
    (2, 'Елена', 'Волкова'),
    (3, 'Дмитрий', 'Орлов');

INSERT INTO SportsEquipment VALUES
    (1, 'Свободные веса', 'Гантели 10 кг', 1),
    (2, 'Кардио', 'Беговая дорожка', 1),
    (3, 'Фитнес', 'Коврик для йоги', 2),
    (4, 'Свободные веса', 'Штанга олимпийская', 3),
    (5, 'Функциональный тренинг', 'Гиря 16 кг', 2);

INSERT INTO Bookings VALUES
    (1, 1, 1, '2026-10-20', 'active'),
    (2, 2, 3, '2026-10-21', 'active'),
    (3, 3, 2, '2026-10-21', 'returned'),
    (4, 1, 4, '2026-10-22', 'active'),
    (5, 4, 5, '2026-10-23', 'active');
"""

QUERY = """
SELECT b.booking_id, b.booking_date, b.status,
       u.first_name, u.second_name,
       e.equipment_name,
       a.first_name, a.second_name
FROM Bookings b
JOIN Users u           ON u.user_id = b.user_id
JOIN SportsEquipment e ON e.equipment_id = b.equipment_id
JOIN Authors a         ON a.author_id = e.author_id
ORDER BY b.booking_id;
"""

with sqlite3.connect("gym.db") as conn:
    conn.executescript(SQL)
    print("Ошибки связей:", conn.execute("PRAGMA foreign_key_check").fetchall() or "нет")
    for row in conn.execute(QUERY):
        print(*row, sep=" | ")