# Task 001 — Validation (Acadia-Hardware)

Parent task: `tasks/001-add-version-support-all-repos/validation.md` (Acadia parent repo).

| # | Check | Command | Result |
|---|---|---|---|
| 1 | Version target | `make version` | PASS — prints `1.0.0` |
| 2 | Help target | `make help` | PASS — lists `version`, `help` |
| 3 | Fleet table | parent `make versions` | PASS — Acadia-Hardware row shows `1.0.0` |

- Revision: local HEAD + this task's two new files; no other changes in the
  worktree.
- Build/test: N/A — repository ships data and validation tools, no build system
  (per plan).
- Skipped checks: none.
- Known limitations: none.