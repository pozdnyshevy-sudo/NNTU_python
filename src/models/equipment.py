from dataclasses import dataclass

@dataclass
class SportsEquipment:
    equipment_id: int
    view_inventory: str | None
    equipment_name: str
    author_id: int
    author_name: str | None = None