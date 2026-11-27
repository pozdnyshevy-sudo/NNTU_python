
import csv
import json
import sqlite3
import xml.etree.ElementTree as ET
from pathlib import Path

import yaml

from database.database import get_connection


def export_bookings():
    """Экспорт бронирований в JSON, CSV, XML и YAML."""

    conn = get_connection()
    conn.row_factory = sqlite3.Row

    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                b.booking_id,
                b.booking_date,
                b.status,
                u.user_id,
                u.first_name,
                u.second_name,
                e.equipment_id,
                e.equipment_name,
                e.view_inventory,
                a.author_id,
                a.first_name AS author_first_name,
                a.second_name AS author_second_name
            FROM Bookings b
            JOIN Users u ON b.user_id = u.user_id
            JOIN SportsEquipment e ON b.equipment_id = e.equipment_id
            LEFT JOIN Authors a ON e.author_id = a.author_id
            ORDER BY b.booking_id
        """)

        rows = cursor.fetchall()

    finally:
        conn.close()

    data = []

    for row in rows:
        data.append({
            "booking_id": row["booking_id"],
            "booking_date": row["booking_date"],
            "status": row["status"],
            "user": {
                "user_id": row["user_id"],
                "first_name": row["first_name"],
                "second_name": row["second_name"]
            },
            "equipment": {
                "equipment_id": row["equipment_id"],
                "name": row["equipment_name"],
                "type": row["view_inventory"],
                "author": {
                    "author_id": row["author_id"],
                    "first_name": row["author_first_name"],
                    "second_name": row["author_second_name"]
                } if row["author_id"] is not None else None
            }
        })

    project_dir = Path(__file__).resolve().parents[2]
    output_dir = project_dir / "out"
    output_dir.mkdir(parents=True, exist_ok=True)

    # JSON
    with open(output_dir / "bookings.json", "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    # CSV
    fields = [
        "booking_id", "booking_date", "status",
        "user_id", "user_first_name", "user_second_name",
        "equipment_id", "equipment_name", "equipment_type",
        "author_id", "author_first_name", "author_second_name"
    ]

    with open(output_dir / "booking.csv", "w", encoding="utf-8-sig",
              newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()

        for item in data:
            user = item["user"]
            equipment = item["equipment"]
            author = equipment["author"] or {}

            writer.writerow({
                "booking_id": item["booking_id"],
                "booking_date": item["booking_date"],
                "status": item["status"],
                "user_id": user["user_id"],
                "user_first_name": user["first_name"],
                "user_second_name": user["second_name"],
                "equipment_id": equipment["equipment_id"],
                "equipment_name": equipment["name"],
                "equipment_type": equipment["type"],
                "author_id": author.get("author_id"),
                "author_first_name": author.get("first_name"),
                "author_second_name": author.get("second_name")
            })

    # XML
    root = ET.Element("bookings")

    for item in data:
        booking = ET.SubElement(root, "booking")

        for key in ("booking_id", "booking_date", "status"):
            ET.SubElement(booking, key).text = str(item[key])

        user = ET.SubElement(booking, "user")
        for key, value in item["user"].items():
            ET.SubElement(user, key).text = str(value)

        equipment = ET.SubElement(booking, "equipment")

        for key in ("equipment_id", "name", "type"):
            value = item["equipment"][key]
            ET.SubElement(equipment, key).text = str(value or "")

        author = item["equipment"]["author"]
        if author:
            author_element = ET.SubElement(equipment, "author")
            for key, value in author.items():
                ET.SubElement(author_element, key).text = str(value)

    tree = ET.ElementTree(root)
    ET.indent(tree, space="    ")
    tree.write(
        output_dir / "booking.xml",
        encoding="utf-8",
        xml_declaration=True
    )

    # YAML
    with open(output_dir / "booking.yaml", "w", encoding="utf-8") as file:
        yaml.safe_dump(
            data,
            file,
            allow_unicode=True,
            sort_keys=False
        )

    print(f"\nЭкспорт завершён! Записей: {len(data)}")
    print(f"Файлы сохранены в папке: {output_dir}")
