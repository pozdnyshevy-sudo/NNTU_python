import sqlite3

SQL = """
PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS BookingItems;
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
    user_id    INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name  TEXT NOT NULL,
    role_id    INTEGER NOT NULL REFERENCES Roles
);
CREATE TABLE Authors (
    author_id  INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name  TEXT NOT NULL,
    role_id    INTEGER NOT NULL REFERENCES Roles
);
CREATE TABLE SportsEquipment (
    equipment_id   INTEGER PRIMARY KEY,
    view_inventory TEXT,
    equipment_name TEXT NOT NULL,
    author_id      INTEGER NOT NULL REFERENCES Authors
);
CREATE TABLE Bookings (
    booking_id   INTEGER PRIMARY KEY,
    user_id      INTEGER NOT NULL REFERENCES Users,
    booking_date DATE NOT NULL
);
CREATE TABLE BookingItems (
    booking_item_id INTEGER PRIMARY KEY,
    booking_id      INTEGER NOT NULL REFERENCES Bookings ON DELETE CASCADE,
    equipment_id    INTEGER NOT NULL REFERENCES SportsEquipment,
    quantity        INTEGER NOT NULL DEFAULT 1,
    UNIQUE (booking_id, equipment_id)
);

INSERT INTO Roles VALUES (1,'Администратор'), (2,'Тренер'), (3,'Клиент');

INSERT INTO Authors VALUES
    (1,'Алексей','Смирнов',1), (2,'Елена','Волкова',2), (3,'Дмитрий','Орлов',2);

INSERT INTO Users VALUES
    (1,'Иван','Иванов',3), (2,'Анна','Петрова',3),
    (3,'Пётр','Сидоров',3), (4,'Мария','Кузнецова',3);

INSERT INTO SportsEquipment VALUES
    (1,'Свободные веса','Гантели 10 кг',1),
    (2,'Кардио','Беговая дорожка',1),
    (3,'Фитнес','Коврик для йоги',2),
    (4,'Свободные веса','Штанга олимпийская',3),
    (5,'Функциональный тренинг','Гиря 16 кг',2);

INSERT INTO Bookings VALUES
    (1,1,'2026-10-20'), (2,2,'2026-10-21'), (3,3,'2026-10-21'),
    (4,1,'2026-10-22'), (5,4,'2026-10-23');

INSERT INTO BookingItems (booking_id, equipment_id, quantity) VALUES
    (1,1,2), (1,3,1), (2,3,1), (3,2,1), (4,4,1), (5,5,1);
"""

conn = sqlite3