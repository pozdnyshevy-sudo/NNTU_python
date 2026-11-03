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
    user_id      INTEGER NOT NULL REFERENCES Users(user_id),
    equipment_id INTEGER NOT NULL REFERENCES SportsEquipment(equipment_id),
    booking_date DATE NOT NULL
);

INSERT INTO Roles VALUES
    (1, 'Администратор'), (2, 'Тренер'), (3, 'Клиент');

INSERT INTO Users VALUES
    (1, 'Иванов Иван', 3), (2, 'Петрова Анна', 3),
    (3, 'Сидоров Пётр', 3), (4, 'Кузнецова Мария', 3);

INSERT INTO Authors VALUES
    (1, 'Смирнов Алексей', 1), (2, 'Волкова Елена', 2), (3, 'Орлов Дмитрий', 2);

INSERT INTO SportsEquipment VALUES
    (1, 'Свободные веса', 'Гантели 10 кг', 1),
    (2, 'Кардио', 'Беговая дорожка', 1),
    (3, 'Фитнес', 'Коврик для йоги', 2),
    (4, 'Свободные веса', 'Штанга олимпийская', 3),
    (5, 'Функциональный тренинг', 'Гиря 16 кг', 2);

INSERT INTO Bookings VALUES
    (1, 1, 1, '2026-10-20'), (2, 2, 3, '2026-10-21'),
    (3, 3, 2, '2026-10-21'), (4, 1, 4, '2026-10-22'),
    (5, 4, 5, '2026-10-23');
"""

QUERY = """
SELECT b.booking_id, b.booking_date, u.full_name, ur.role_name,
       e.equipment_name, a.full_name, ar.role_name
FROM Bookings b
JOIN Users u            ON u.user_id = b.user_id
JOIN Roles ur           ON ur.role_id = u.role_id
JOIN SportsEquipment e  ON e.equipment_id = b.equipment_id
JOIN Authors a          ON a.author_id = e.author_id
JOIN Roles ar           ON ar.role_id = a.role_id
ORDER BY b.booking_id;
"""

with sqlite3.connect("gym.db") as conn:
    conn.executescript(SQL)
    print("Ошибки связей:", conn.execute("PRAGMA foreign_key_check").fetchall() or "нет")
    for row in conn.execute(QUERY):
        print(*row, sep=" | ")