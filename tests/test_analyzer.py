import unittest

from cardinality_guard.analyzer import analyze_inventory
from cardinality_guard.explainer import build_bounded_ai_context


class AnalyzerTests(unittest.TestCase):
    def test_safe_metric_passes(self):
        report = analyze_inventory({"metrics": [{"name": "http_requests_total", "labels": [
            {"name": "method", "distinct_values": 5, "bounded": True},
            {"name": "status_class", "distinct_values": 5, "bounded": True},
        ]}]})
        self.assertEqual("pass", report["release_decision"])
        self.assertEqual(25, report["metrics"][0]["projected_series"])

    def test_unbounded_label_blocks_when_budget_exceeded(self):
        report = analyze_inventory({"defaults": {"series_budget": 1000}, "metrics": [{
            "name": "checkout_latency_seconds",
            "labels": [
                {"name": "route", "distinct_values": 40, "bounded": True},
                {"name": "session_id", "distinct_values": 5000, "bounded": False},
            ],
        }]})
        self.assertEqual("block", report["release_decision"])
        self.assertEqual(200000, report["metrics"][0]["projected_series"])

    def test_sensitive_label_always_blocks(self):
        report = analyze_inventory({"metrics": [{"name": "login_total", "labels": [
            {"name": "email", "distinct_values": 2, "bounded": True}
        ]}]})
        self.assertEqual("block", report["release_decision"])

    def test_results_are_sorted_for_reproducibility(self):
        report = analyze_inventory({"metrics": [
            {"name": "z_metric", "labels": []}, {"name": "a_metric", "labels": []}
        ]})
        self.assertEqual(["a_metric", "z_metric"], [item["metric"] for item in report["metrics"]])

    def test_ai_context_excludes_raw_values_and_preserves_decision(self):
        report = analyze_inventory({"metrics": [{"name": "requests_total", "labels": [
            {"name": "route", "distinct_values": 2, "bounded": True}
        ]}]})
        context = build_bounded_ai_context(report)
        self.assertEqual(report["release_decision"], context["release_decision"])
        self.assertNotIn("values", str(context).lower())


if __name__ == "__main__":
    unittest.main()

