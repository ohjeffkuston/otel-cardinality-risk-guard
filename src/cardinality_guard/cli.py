from __future__ import annotations

import argparse
import json
from pathlib import Path

from .analyzer import analyze_inventory
from .explainer import build_bounded_ai_context


def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate telemetry cardinality before deployment")
    parser.add_argument("inventory", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--ai-context", type=Path)
    parser.add_argument("--fail-on", choices=("never", "block"), default="block")
    args = parser.parse_args()

    report = analyze_inventory(json.loads(args.inventory.read_text()))
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered)
    else:
        print(rendered, end="")
    if args.ai_context:
        args.ai_context.write_text(json.dumps(build_bounded_ai_context(report), indent=2, sort_keys=True) + "\n")
    return 2 if args.fail_on == "block" and report["release_decision"] == "block" else 0


if __name__ == "__main__":
    raise SystemExit(main())

