# Task 003 (Acadia-Hardware) — `/pst` partition platform check

Parent task: `tasks/003-add-pst-partition/plan.md` (Acadia parent repository).
Status: draft — awaiting approval. Date: 2026-09-21. Owner: Sandesh Ghimire.
Classification: **validation-only** — no code change expected.

## Role in cross-repository validation

Acadia-OS adds a 1 GB p4 partition to the A/B SD image
(`sdimage-rpi5.wks`), growing the default image footprint from
≈ 17.15 GiB to ≈ 18.15 GiB (`make flash` media requirement rises by 1 GB).
Per the parent workflow, hardware/platform assumptions are checked here.

## Affected interfaces

- SD card / eMMC media capacity assumptions for flashing new images.
- No drivers, device interfaces, or pin maps are touched (partition table is
  Acadia-OS domain; the SD/SDIO/eMMC block device behaviour is unchanged —
  MBR/DOS label with 5 primary partitions is supported by all Acadia media).

## Expected files

None. If `doc/BUILD_DEPLOY.md`, `README.md`, `Plan.md`, or `pin-map/`
documentation states image sizes or minimum media capacity, an update note
is proposed before editing (escalate for approval — this would be a scope
addition).

## Local tests

- `make check-repo-order` / repository checks unchanged and green.

## Cross-repository validation (with Acadia-OS)

- Confirm the flashed 5-partition image enumerates correctly on the target
  SD/eMMC controller during the Acadia-OS on-target run (same session as the
  fresh-flash validation); record any capacity or enumeration findings in
  this folder's `validation.md`.