# Task 003 (Acadia-Hardware) — validation record

Classification: validation-only — no code changes made to this repository.

## Platform check

- Image footprint grows from ≈ 17.15 GiB to ≈ 17.75 GiB (1 GB `/pst` data
  partition added; GPT table overhead included). `make flash` media
  requirement rises by ~1 GB.
- No driver, device-interface, or pin-map involvement: the SD/eMMC block
  device behaviour is unchanged; the MBR→GPT table change is Acadia-OS
  domain (all Acadia media support GPT; CM5 NVMe boot already requires it).
- `doc/BUILD_DEPLOY.md`, `README.md`, `Plan.md`, `pin-map/` contain no image
  size or minimum-capacity statements — no doc update needed.

## Local tests

- Repository checks unchanged and green (no files changed).

## Cross-repository validation (with Acadia-OS)

- Partition enumeration on target hardware is part of the pending on-target
  session (fresh-flash step in parent `validation.md`); owner: Acadia-OS
  maintainers.