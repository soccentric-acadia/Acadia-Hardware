# Changelog

## 2026-09-21 — Root-agent feature workflow guard (task 006)

- Added a canonical instruction requiring leaf-started agents to refuse feature
  changes and direct the user to the Acadia parent root.

## 2026-09-21 — Version support (task 001)

### Added

- Added `VERSION` file (1.0.0) and a minimal top-level `Makefile` with the
  self-documenting `help` pattern and the fleet-standard `version` target
  (CONV-004), so the parent `make versions` table covers this repository.

Task records: `tasks/001-add-version-support-all-repos/`.

## 2026-09-18 — Agent documentation and task workflow standardization

### Added

- `AGENTS.md` and `CLAUDE.md` pointers to `.claude/CLAUDE.md`.
- A canonical document limited to the project title, summary, and explicit
  no-software-build instruction.
- Ignored local `Plan.md` and `Task.md` task-workflow artifacts.

### Validation

- Confirmed the required pointer and canonical-document structure.
- Confirmed the repository defines no Makefile or software build target.
