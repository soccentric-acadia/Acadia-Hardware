# Task 014 — Acadia-Hardware execution record

- **Approval date:** 2026-09-28
- **Approved scope:** Parent Task 014 P0-04 validation authority.

## Checklist

- [x] P0-04 Publish the supported production capability matrix.

## Implementation record

### 2026-09-28 — P0-04

- Added [`doc/supported-capability-matrix-v1.md`](../../doc/supported-capability-matrix-v1.md),
  version `1.0.0`, as the production hardware authority for board revision
  `rpi5-cm5-bom-rev-c` and pin-map contract `1.0`.
- Grounded the matrix only in the existing pin map and UART allocation:
  console, RS-485, Pico link, GPIO ownership, reserved pins, I2C, SPI, and
  the existing classic-CAN constraint. It explicitly marks absent peripheral
  facts and the Pico device-node HIL confirmation as unsupported/conditional
  rather than inferring support.
- Did not add schema tooling: this leaf's existing `tools/check_pin_map.py`
  provides the supported structural/cross-repository drift validation pattern;
  no existing schema contract establishes additional fields.
- Documented the required downstream OS, Configuration, and Instrumentation
  consumption, rejection behavior, and negative-test ownership without
  modifying those repositories.

## Validation

- `python3 -m json.tool pin-map/board_rev_a.json` — passed; the published
  board-revision source remains valid JSON.
- `python3 tools/check_pin_map.py` — passed:
  `pin map drift gate: OK (rpi5-cm5-bom-rev-c)`.
- `git diff --check` — passed; no whitespace errors in the matrix or execution
  record.
