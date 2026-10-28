# Task 014 — Acadia-Hardware validation scope

Parent plan: [Acadia Task 014](../../../../tasks/014-production-flow-operational-readiness/plan.md).

## Scope

Hardware is validation-only. It supplies the supported board/revision and peripheral authority for P0-04, P0-14 through P1-18, P1-21, and P0-26. No product-code change is expected unless validation discovers that the published capability/pin/boot assumptions are wrong.

## Cross-repository validation

Confirm the supported-board matrix, boot media, watchdog, reset, storage, network, identity, and recovery assumptions. Provide sacrificial HIL boards and evidence for boot, update, forced rollback, factory reset, and re-enrollment on every supported hardware revision.
