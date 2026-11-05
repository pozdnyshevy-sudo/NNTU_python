from dataclasses import dataclass

@dataclass
class Booking:
    booking_id: int
    user_id: int
    equipment_id: int
    booking_date: str
    status: str
    user_name: str | None = None
    equipment_name: str | None = None