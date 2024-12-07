from dataclasses import dataclass
from featureflagger.interfaces import FeatureGuard, Resource
from featureflagger.criteria import Criticality

@dataclass
class CriticalityGuard(FeatureGuard):
    maximum_criticality: Criticality

    def name(self) -> str:
        return "criticality"

    def enabled(self, resource: Resource) -> bool:
        return self.maximum_criticality.value() >= resource.criticality().value()

def new(maximum_criticality: Criticality) -> FeatureGuard:
    return CriticalityGuard(maximum_criticality)