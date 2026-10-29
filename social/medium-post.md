# Preventing OpenTelemetry Cardinality Regressions Before Production

Observability systems are designed to make production easier to understand. But a small instrumentation change can turn the observability platform itself into an operational risk.

Every unique combination of metric labels creates a time series. Add an unbounded value such as a session, request, account, or user identifier and one harmless-looking metric can expand into thousands or millions of series. That growth consumes memory, storage, network bandwidth, and query capacity. It can also move sensitive identifiers into systems that were never meant to hold them.

This is not a generic AI problem. It is a release-engineering and SRE problem that benefits from a narrow, controlled use of AI.

![OpenTelemetry Cardinality Risk Guard architecture](https://raw.githubusercontent.com/ohjeffkuston/otel-cardinality-risk-guard/main/docs/architecture.png)

## Why this matters now

Prometheus guidance explicitly warns that every unique label combination creates a time series and advises against high-cardinality dimensions such as user IDs and email addresses. Its instrumentation guidance recommends investigating alternatives when a metric can exceed 100 distinct values.

The hiring signal is equally clear. Current platform, DevOps, SRE, and AI-infrastructure roles repeatedly combine Kubernetes, Terraform, GitOps, Prometheus, OpenTelemetry, SLOs, incident response, and production AI operations. Teams need engineers who can operate AI workloads and use AI responsibly inside the operational workflow.

## The project

I built the OpenTelemetry Cardinality Risk Guard as a deterministic pre-deployment control.

A service owner declares the expected dimensions for each metric. The analyzer calculates the Cartesian product of label values, evaluates configured budgets, detects unbounded or sensitive dimensions, and emits a reproducible pass, review, or block decision.

The release decision is never delegated to a language model. An optional AI stage receives only metric names, counts, budgets, risk classifications, and deterministic recommendations. It can explain the evidence, but it cannot change the decision, see raw label values, or modify production.

## Architecture

The workflow has six stages:

1. A telemetry inventory enters CI.
2. The analyzer projects active-series growth.
3. Policy checks classify budget pressure, unbounded labels, and sensitive identifiers.
4. CI records a machine-readable report and fails closed on high risk.
5. A bounded AI context supports human-readable explanation.
6. A human approves any Collector or instrumentation change through GitOps.

This separation is deliberate. Deterministic logic is testable and auditable; AI is useful for explanation and triage, not enforcement.

## Implementation choices

The implementation is a dependency-free Python package with a CLI, typed data models, deterministic sorting, and explicit exit codes. Projected series are calculated as the product of expected distinct label values. Sensitive labels force a block even when their current count is low because their privacy risk is independent of cardinality.

The repository also includes an OpenTelemetry Collector configuration example that removes sensitive attributes before export. It is guidance, not an automatic mutation: teams must verify component compatibility, stage the change, canary it, and observe exporter health and active-series deltas.

## Tests and validation

The suite covers bounded safe metrics, budget-exceeding unbounded labels, sensitive-label blocking, deterministic output order, privacy-preserving AI context, CLI report creation, and fail-closed exit behavior.

GitHub Actions runs the tests and executes a deliberately unsafe sample. CI succeeds only when the sample is blocked as expected. This makes policy behavior part of the software contract.

## Deployment guidance

I would introduce the guard in advisory mode for two release cycles, compare projections with a read-only view of production series data, tune false positives, and only then enforce blocking. Approved exceptions should be evidence-based, owned, and time-limited.

Removing labels blindly can damage diagnostics. High-cardinality detail often belongs in controlled logs or traces rather than metrics. The goal is not less observability; it is using the right telemetry signal for the right question.

## Security and reliability

Raw label values never enter the inventory or AI context. AI output is non-authoritative. Collector changes remain behind human approval. The policy fails closed for known sensitive identifiers and produces repeatable evidence for review.

The main failure mode is estimation drift. Declared counts can differ from production behavior, so the guard should be reconciled regularly with backend data. Static budgets must also reflect real retention, ingestion, and query costs.

## Measurable outcomes

The useful measures are concrete:

- high-cardinality regressions caught before production
- active-series growth per release
- telemetry ingestion and storage cost
- false-positive and exception rates
- mean time to identify the label responsible for a spike
- percentage of telemetry changes evaluated in CI

## Interview positioning

This project demonstrates how I approach a production SRE problem: identify a measurable failure mode, design a deterministic control, put it into CI, preserve privacy, define safe rollout and rollback paths, and use AI only where it adds value without becoming the control plane.

It is relevant to Cloud Engineering, DevOps, SRE, Platform Engineering, and AI-infrastructure roles because it combines observability, policy automation, CI/CD, OpenTelemetry, Prometheus, testing, security, FinOps thinking, and responsible AI orchestration.

Repository: https://github.com/ohjeffkuston/otel-cardinality-risk-guard

