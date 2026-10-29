# Demand and technical research

Checked: 2026-10-29 (America/Detroit)

## Authoritative technical sources

- Prometheus, [Metric and label naming](https://prometheus.io/docs/practices/naming/): every unique label combination creates a time series; unbounded values such as user IDs and emails should not be metric labels.
- Prometheus, [Instrumentation](https://prometheus.io/docs/practices/instrumentation/): labelsets consume RAM, CPU, disk, and network; cardinality above 100 warrants investigation and often a different data path.
- OpenTelemetry, [Collector processors](https://opentelemetry.io/docs/collector/components/processor/): processors transform, filter, and enrich telemetry; current contrib listings include a cardinality guardian processor.

## Recurring live-job requirements

The topic was validated against multiple current postings, not selected from a generic trend list:

- [Zingtree — Senior DevOps / Platform Reliability Engineer](https://jobs.lever.co/zingtree/8cae8c0a-2f42-472c-9707-e70a69f81f54): production EKS, Argo CD, Terraform, Prometheus, OpenTelemetry, AI-workload telemetry, SLOs, security, and cost controls.
- [Shield AI — Staff Engineer, Platform](https://jobs.lever.co/shieldai/c946dfe1-c619-46f1-a7d7-8faaaebe763c): Kubernetes-native AI platform services, OpenTelemetry/Prometheus/Grafana, SLOs, incident management, Terraform, Helm, and Argo CD.
- [Bright Machines — Staff Platform Engineer](https://jobs.lever.co/brightmachines/ec448598-89ab-439c-96e5-00a882d5997d): AI/data-center platform engineering with Kubernetes, IaC, GitOps, and Prometheus/Grafana/OpenTelemetry.
- [Zopa — Platform Engineer](https://jobs.lever.co/zopa/a87c80d9-4a4d-4238-80e2-d3eebcb74c5a): AWS, Kubernetes/EKS, Terraform, CI/CD, observability including OpenTelemetry, and pragmatic AI-assisted engineering.

## Demand rationale

The recurring hiring signal is not “build an AI demo.” It is “operate cloud-native and AI workloads safely with Kubernetes, IaC, GitOps, observability, reliability, and security.” Cardinality control is a credible production problem at that intersection: it protects telemetry reliability and cost while creating a safe, bounded place for AI-assisted explanation.

