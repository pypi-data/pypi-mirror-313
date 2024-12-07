from dataclasses import dataclass

# MaxCriticality is a constant that represents the maximum criticality value (i.e. Maximum 32bit integer value)
MaxCriticality = Criticality("MAX", 2147483647)


@dataclass
class Criticality:
    id: str
    value: int

    def id(self) -> str:
        return self.id

    def value(self) -> int:
        return self.value


def new_criticality(id: str, value: int) -> Criticality:
    return Criticality(id, value)