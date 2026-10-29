Subject: Day 16 — OpenTelemetry Cardinality Risk Guard: deployment and interview guide

To: ohjeffkuston@yahoo.ca

Hello Jeffrey,

Day 16 is the OpenTelemetry Cardinality Risk Guard, a production-focused SRE and platform-engineering project that catches dangerous metric-label cardinality before deployment.

## What the project solves

Each unique metric-label combination becomes a time series. Unbounded values such as user IDs, session IDs, request IDs, or email addresses can create explosive series growth, increase cost and query latency, and expose sensitive data. The guard converts that risk into a testable CI decision.

## How it works

1. A JSON inventory describes metrics, labels, expected distinct counts, bounds, and sensitivity.
2. The analyzer multiplies label counts to estimate projected series.
3. Policy checks score budget pressure, unbounded labels, and sensitive identifiers.
4. The CLI emits a report and exits with code 2 for a blocked release.
5. An optional AI context contains only evidence and recommendations—never raw values.
6. A human approves any OpenTelemetry configuration change through GitOps.

## Deploy it yourself

Clone the repository, create a Python 3.11+ virtual environment, install with `python -m pip install -e .`, and run `python -m unittest discover -s tests -v`.

Run the sample with:

`cardinality-guard examples/telemetry-inventory.json --output report.json --ai-context ai-context.json`

The sample intentionally fails closed because `session_id` is sensitive and unbounded. Replace the sample inventory with one for your own service, begin with `--fail-on never`, compare estimates with production series evidence, tune budgets, and then enforce blocking.

## Security model

- no raw label values are required;
- sensitive metric labels block deterministically;
- AI cannot override the policy or mutate production;
- Collector changes require human review;
- exceptions should have owners, evidence, and expiry dates.

## What to learn deeply

Be able to explain why cardinality is multiplicative, why metrics should not contain unbounded identifiers, why logs or traces may be a better home for detailed dimensions, how CI fail-closed behavior works, and why bounded AI explanation is safer than LLM-only enforcement.

## Interview story

“I built a pre-deployment observability control that estimates metric series growth, blocks sensitive or unbounded labels, and integrates with CI. I separated deterministic enforcement from optional AI explanation, so the system remains testable, auditable, and safe. I also designed an advisory rollout, production reconciliation, exception process, rollback path, and measurable outcomes.”

## Measurable value

Track prevented regressions, active-series growth, ingestion cost, false-positive rate, exception rate, and time to identify the label responsible for a spike.

Repository: https://github.com/ohjeffkuston/otel-cardinality-risk-guard

Regards,
Jeffrey Ikuoyemwen
