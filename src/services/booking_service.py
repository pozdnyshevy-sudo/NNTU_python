from repositories import booking_repository, user_repository, equipment_repository
from services import equipment_service

CLIENT_ROLE_ID = 3

def create_booking(user_id: int, equipment_id: int):
    user = user_repository.get_by_id(user_id)
    if not user:
        raise Exception("Пользователь не найден")
    if user.role_id != CLIENT_ROLE_ID:
        raise Exception("Только клиент может бронировать инвентарь")
    if not equipment_repository.get_by_id(equipment_id):
        raise Exception("Инвентарь не найден")
    if not equipment_service.is_equipment_available(equipment_id):
        raise Exception("Инвентарь уже забронирован")
    booking_repository.create(user_id, equipment_id)

def return_booking(booking_id: int):
    booking = booking_repository.get_by_id(booking_id)
    if not booking:
        raise Exception("Бронирование не найдено")
    if booking.status != 'active':
        raise Exception("Бронирование уже закрыто")
    booking_repository.return_booking(booking_id)

def cancel_booking(booking_id: int):
    booking = booking_repository.get_by_id(booking_id)
    if not booking:
        raise Exception("Бронирование не найдено")
    if booking.status != 'active':
        raise Exception("Бронирование уже закрыто")
    booking_repository.cancel(booking_id)