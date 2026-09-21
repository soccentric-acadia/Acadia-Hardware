# Task 001 — Add version support (Acadia-Hardware scope)

Parent task: `tasks/001-add-version-support-all-repos/plan.md` (Acadia parent repo).

## Scope (this repository)

- Add `VERSION` file containing `1.0.0` (fleet-consistent with Instrumentation/HAL).
- Add a minimal top-level `Makefile` with the self-documenting `help` pattern used
  by the other leaves (mirroring Acadia-Client) plus a `version` target
  (CONV-004) that prints the VERSION file content:

  ```make
  version: ## Print the project version (CONV-004)
  	@echo "$$(cat VERSION)"
  ```

## Affected interfaces

- New files only; no existing behavior, pin-map data, or tooling touched.
- Parent `make versions` will read this repo's `version` target (fleet table).

## Expected files

- `VERSION` (new)
- `Makefile` (new)

## Local validation

- `make version` → `1.0.0`
- `make help` → lists `version`

## Cross-repo role

- Validation-only for the rest: parent `make versions` must show this repo with
  a version instead of `-`.

## Status

Complete (2026-09-21).