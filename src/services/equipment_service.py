from repositories import equipment_repository, booking_repository

def add_equipment(view_inventory: str, equipment_name: str, author_id: int):
    if not equipment_name.strip():
        raise Exception("Название инвентаря не может быть пустым")
    equipment_repository.create(view_inventory, equipment_name, author_id)

def is_equipment_available(equipment_id: int) -> bool:
    bookings = booking_repository.get_all()
    for b in bookings:
        if b.equipment_id == equipment_id and b.status == 'active':
            return False
    return True