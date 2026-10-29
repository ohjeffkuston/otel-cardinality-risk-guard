from dataclasses import dataclass, asdict
from typing import Any


@dataclass(frozen=True)
class LabelAssessment:
    name: str
    distinct_values: int
    bounded: bool
    sensitive: bool
    risk: str


@dataclass(frozen=True)
class MetricAssessment:
    metric: str
    projected_series: int
    budget: int
    score: int
    decision: str
    risky_labels: tuple[LabelAssessment, ...]
    recommended_actions: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        result = asdict(self)
        result["risky_labels"] = [asdict(item) for item in self.risky_labels]
        result["recommended_actions"] = list(self.recommended_actions)
        return result

