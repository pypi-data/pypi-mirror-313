from typing import Protocol
from dataclasses import dataclass

class Criticality(Protocol):
    def id(self) -> str:
        ...

    def value(self) -> int:
        ...

class Resource(Protocol):
    def id(self) -> str:
        ...

    def criticality(self) -> Criticality:
        ...

class FeatureGuard(Protocol):
    def enabled(self, resource: Resource) -> bool:
        ...

    def name(self) -> str:
        ...