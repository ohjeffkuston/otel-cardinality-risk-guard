import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class CliTests(unittest.TestCase):
    def test_cli_writes_report_and_ai_context(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            inventory = root / "inventory.json"
            report = root / "report.json"
            context = root / "context.json"
            inventory.write_text(json.dumps({"metrics": [{"name": "safe_total", "labels": []}]}))
            completed = subprocess.run([
                sys.executable, "-m", "cardinality_guard.cli", str(inventory),
                "--output", str(report), "--ai-context", str(context),
            ], check=False)
            self.assertEqual(0, completed.returncode)
            self.assertEqual("pass", json.loads(report.read_text())["release_decision"])
            self.assertTrue(context.exists())

    def test_cli_fails_closed_on_block(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "inventory.json"
            path.write_text(json.dumps({"metrics": [{"name": "bad_total", "labels": [
                {"name": "user_id", "distinct_values": 1000, "bounded": False}
            ]}]}))
            completed = subprocess.run([sys.executable, "-m", "cardinality_guard.cli", str(path)], check=False)
            self.assertEqual(2, completed.returncode)


if __name__ == "__main__":
    unittest.main()

