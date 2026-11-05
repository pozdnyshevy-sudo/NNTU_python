from dataclasses import dataclass

@dataclass
class User:
    user_id: int
    first_name: str
    second_name: str
    login: str
    password: str
    role_id: int
    role_name: str | None = None

    @property
    def full_name(self):
        return f"{self.first_name} {self.second_name}"