# Safe deployment guide

## CI-only introduction

1. Commit `telemetry-inventory.json` beside the service instrumentation.
2. Run the guard with `--fail-on never` for two release cycles.
3. Compare projections with a read-only query of the backend's active-series data.
4. Document acceptable deviations and assign exception expiry dates.
5. Change CI to the default fail-closed behavior.

## Collector rollout

The sample processor removes sensitive attributes before metrics are exported. Confirm the processor is available in your Collector distribution. Validate the configuration with the Collector's config-check command, deploy to a non-production gateway, then canary the change.

Observe:

- exporter send failures;
- Collector CPU and memory;
- active-series delta;
- missing diagnostic dimensions;
- alert and dashboard query failures.

Rollback by reverting the GitOps commit. Do not let the AI explanation stage write configuration or call the Kubernetes API.

## Operational ownership

- Service owners declare intended dimensions.
- The platform/SRE team owns default budgets and policy implementation.
- Security reviews sensitive-label rules.
- FinOps validates cost outcomes.
- Human reviewers approve exceptions and production changes.

