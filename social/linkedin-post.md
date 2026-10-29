Telemetry cardinality problems rarely announce themselves in code review.

A single label such as `session_id`, `user_id`, or `request_id` can multiply one metric into thousands of time series. The result is higher observability cost, slower queries, noisier operations, and a possible privacy problem—often discovered only after deployment.

The practical solution is to treat telemetry design like any other production change: define a budget, test it in CI, and fail safely before it reaches the OpenTelemetry pipeline.

I built the OpenTelemetry Cardinality Risk Guard to do that. It:

• calculates projected time-series growth from label dimensions
• detects unbounded and sensitive labels
• produces an auditable pass, review, or block decision
• fails closed in GitHub Actions
• creates a value-free context for optional AI explanation without allowing AI to override policy or modify production

The project also includes tests, sample telemetry, a Collector configuration example, deployment guidance, security controls, measurable outcomes, and the architecture shown here.

Repository: https://github.com/ohjeffkuston/otel-cardinality-risk-guard

The broader lesson: AI is most useful in operations when it explains evidence around a deterministic control—not when it silently becomes the control plane.

What telemetry guardrail would prevent the most expensive surprise in your environment?

Follow my profile for practical Cloud, DevOps, SRE, Platform Engineering, and AI-infrastructure projects.

#OpenTelemetry #Prometheus #SRE #PlatformEngineering #DevOps #Observability #Kubernetes #AIInfrastructure

