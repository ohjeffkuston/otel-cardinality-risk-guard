from __future__ import annotations

from math import prod
from typing import Any

from .models import LabelAssessment, MetricAssessment


SENSITIVE_MARKERS = {
    "email", "user_id", "userid", "session_id", "sessionid", "ip_address",
    "customer_id", "account_id", "token", "request_id", "trace_id",
}


def _label_assessment(label: dict[str, Any], unbounded_threshold: int) -> LabelAssessment:
    name = str(label["name"])
    distinct = max(1, int(label.get("distinct_values", 1)))
    normalized = name.lower().replace("-", "_")
    sensitive = bool(label.get("sensitive", False)) or normalized in SENSITIVE_MARKERS
    bounded = bool(label.get("bounded", distinct <= unbounded_threshold))
    if sensitive:
        risk = "critical"
    elif not bounded or distinct > unbounded_threshold:
        risk = "high"
    elif distinct > max(10, unbounded_threshold // 4):
        risk = "medium"
    else:
        risk = "low"
    return LabelAssessment(name, distinct, bounded, sensitive, risk)


def _actions(labels: list[LabelAssessment], projected: int, budget: int) -> tuple[str, ...]:
    actions: list[str] = []
    sensitive = sorted(label.name for label in labels if label.sensitive)
    unbounded = sorted(label.name for label in labels if not label.bounded)
    if sensitive:
        actions.append("drop or hash sensitive labels before export: " + ", ".join(sensitive))
    if unbounded:
        actions.append("remove unbounded labels from metrics and move detail to logs/traces: " + ", ".join(unbounded))
    if projected > budget:
        actions.append(f"reduce projected series from {projected} to the configured budget of {budget}")
    if not actions:
        actions.append("retain labels and monitor active-series growth after deployment")
    return tuple(actions)


def analyze_inventory(inventory: dict[str, Any]) -> dict[str, Any]:
    defaults = inventory.get("defaults", {})
    default_budget = int(defaults.get("series_budget", 1000))
    threshold = int(defaults.get("unbounded_threshold", 100))
    results: list[MetricAssessment] = []

    for metric in sorted(inventory.get("metrics", []), key=lambda item: item["name"]):
        labels = [_label_assessment(label, threshold) for label in metric.get("labels", [])]
        projected = prod(label.distinct_values for label in labels) if labels else 1
        budget = int(metric.get("series_budget", default_budget))
        ratio_points = min(60, round(60 * projected / max(1, budget)))
        high_points = 15 * sum(label.risk == "high" for label in labels)
        critical_points = 30 * sum(label.risk == "critical" for label in labels)
        score = min(100, ratio_points + high_points + critical_points)
        decision = "block" if score >= 70 or any(label.sensitive for label in labels) else "review" if score >= 40 else "pass"
        results.append(MetricAssessment(
            metric=str(metric["name"]),
            projected_series=projected,
            budget=budget,
            score=score,
            decision=decision,
            risky_labels=tuple(label for label in labels if label.risk != "low"),
            recommended_actions=_actions(labels, projected, budget),
        ))

    counts = {decision: sum(item.decision == decision for item in results) for decision in ("pass", "review", "block")}
    return {
        "schema_version": "1.0",
        "summary": {"metrics": len(results), **counts},
        "release_decision": "block" if counts["block"] else "review" if counts["review"] else "pass",
        "metrics": [item.to_dict() for item in results],
    }

