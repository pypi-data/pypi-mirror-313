import json
from typing import Any, Dict, Union
from featureflagger.interfaces import FeatureGuard
from featureflagger.guards.criticality import new as new_criticality
from featureflagger.criteria import new_criticality as new_crit

class Feature:
    def __init__(self, id: str, type: str, params: Dict[str, Any]):
        self.id = id
        self.type = type
        self.params = params

    def guard(self) -> FeatureGuard:
        if self.type == "criticality":
            max_crit = self.params.get("max_criticality", 2147483647)
            return new_criticality(new_crit("max", max_crit))
        else:
            raise ValueError(f"Unknown feature type: {self.type}")

class FeatureManager:
    def __init__(self, features: Dict[str, Feature]):
        self.features = features

    def get_guard(self, feature_id: str) -> FeatureGuard:
        feature = self.features.get(feature_id)
        if feature:
            return feature.guard()
        else:
            raise ValueError(f"Feature not found: {feature_id}")

def load_json(json_config: str) -> FeatureManager:
    config = json.loads(json_config)
    features = {f["id"]: Feature(f["id"], f["type"], f["params"]) for f in config["features"]}
    return FeatureManager(features)