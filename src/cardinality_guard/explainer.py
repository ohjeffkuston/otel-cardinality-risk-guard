from __future__ import annotations

from typing import Any


def build_bounded_ai_context(report: dict[str, Any]) -> dict[str, Any]:
    """Create a value-free payload for an optional LLM explanation step.

    Raw label values never enter this payload. The deterministic decision remains authoritative.
    """
    return {
        "instruction": "Explain the deterministic telemetry risk decision without changing it or proposing automatic production changes.",
        "release_decision": report["release_decision"],
        "summary": report["summary"],
        "metrics": [
            {
                "metric": item["metric"],
                "decision": item["decision"],
                "score": item["score"],
                "projected_series": item["projected_series"],
                "budget": item["budget"],
                "risky_labels": [
                    {"name": label["name"], "risk": label["risk"]}
                    for label in item["risky_labels"]
                ],
                "recommended_actions": item["recommended_actions"],
            }
            for item in report["metrics"]
        ],
        "guardrails": [
            "Do not invent telemetry data, incident impact, or cost savings.",
            "Do not override the deterministic decision.",
            "Require human approval before telemetry configuration changes.",
        ],
    }

