from dataclasses import dataclass

@dataclass
class Concern:
    sector: str
    department: str
    concern: str
    degree: str
    degree_level: int

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)
