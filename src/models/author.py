from dataclasses import dataclass

@dataclass
class Author:
    author_id: int
    first_name: str
    second_name: str

    @property
    def full_name(self):
        return f"{self.first_name} {self.second_name}"