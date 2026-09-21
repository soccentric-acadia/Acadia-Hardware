# Task 001 — Execution log (Acadia-Hardware)

Parent task: `tasks/001-add-version-support-all-repos/execution.md` (Acadia parent repo).

## Approved scope

Add `VERSION` file (1.0.0) and minimal Makefile with self-documenting `help`
plus `version` target (CONV-004).

## Checklist

- [x] Add `VERSION` (content `1.0.0`)
- [x] Add `Makefile` (help + version)
- [x] Validate `make version` → `1.0.0`; `make help` lists `version`

## Files changed

- `VERSION` (new)
- `Makefile` (new)

## Notes

- No existing files (pin-map, tools, doc) touched. No deviations.