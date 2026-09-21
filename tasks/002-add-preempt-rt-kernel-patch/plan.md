# Task 002 (leaf) — Add PREEMPT_RT patch to the Linux kernel — Acadia-Hardware

Parent task: `Acadia/tasks/002-add-preempt-rt-kernel-patch/plan.md`
- **Task ID:** 002
- **Date:** 2026-09-21
- **Status:** approved 2026-09-21 (aarch64-only scope, D1 resolved) — build-side complete; on-target pending
- **Class:** validation-only

## Scope in this repository

None (no code change). Acadia-Hardware owns the pin-map and board assumptions
that the kernel configuration builds on (e.g. `mcp2515-can0` with
`oscillator=16000000,interrupt=25`, 1-Wire on its assigned GPIO, PWM channel
assignment). The PREEMPT_RT kernel threads IRQ handlers and changes scheduling
latency; those timing assumptions must be re-verified, and any documented
timing figures updated only if measurement shows drift.

## Affected interfaces

- Pin-map / board-rev documentation: re-checked, expected unchanged.
- Peripheral timing assumptions (CAN bus load, 1-Wire probe timing, PWM):
  re-measured on the RT image.

## Expected validation role

1. Confirm `pin-map/board_rev_a.json` mappings are untouched by the kernel
   change (device-tree overlays are identical; only the kernel is RT).
2. On-target peripheral checks (CAN, 1-Wire, PWM) performed jointly with the
   Acadia-OS validation run; results cross-referenced in this leaf's
   `validation.md`.
3. If measured timing deviates from documented assumptions, that is a **new
   scope item** (Hardware doc update or driver configuration change) requiring
   renewed approval.