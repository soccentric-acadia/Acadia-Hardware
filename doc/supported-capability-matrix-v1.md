# Acadia supported production capability matrix v1

| Field | Value |
|---|---|
| Matrix version | `1.0.0` |
| Status | Published hardware authority for Task 014 P0-04 |
| Board-revision contract | `rpi5-cm5-bom-rev-c` |
| Pin-map contract | `1.0` (`pin-map/board_rev_a.json`) |
| Source date | 2026-09-23 pin-map revision |

This is the versioned, production-facing capability authority for Acadia
hardware. It applies only to the Raspberry Pi 5 / CM5 (BCM2712 + RP1) board
family built to the stated board-revision contract. No other board, board
revision, peripheral, pin assignment, or device node is approved by this
matrix. The pin map and [UART allocation](uart-allocation.md) remain the
authoritative detailed electrical and UART records; this document makes their
production support boundary explicit.

## Board support

| Board family | Supported revision | Production constraint |
|---|---|---|
| Raspberry Pi 5 / CM5 (BCM2712 + RP1) | `rpi5-cm5-bom-rev-c` only | Consumers must select this exact revision before enabling a board-specific capability. |
| Any other Raspberry Pi, CM5 revision, or board | None | Unsupported. Consumers must reject board-specific provisioning and actions rather than applying this matrix. |

## Peripheral capability matrix

| Capability | Production status | Allowed allocation / constraint | Consumer action |
|---|---|---|---|
| OS debug console | Supported and reserved | RP1 UART10, `/dev/ttyAMA10`, dedicated debug header | Keep as the OS console; never allocate it to a module or peripheral. |
| HAL RS-485 | Supported | RP1 UART0, GPIO14/15, `/dev/ttyAMA0`; 115200 8N1, no flow control, half-duplex with `TIOCSRS485` direction control | Use the HAL accessor/configuration, not a conflicting console or a guessed device node. |
| Pico W co-processor link | Conditionally supported | RP1 UART2, GPIO0/1, expected `/dev/ttyAMA2`; 115200 8N1, no flow control; requires `dtoverlay=uart2` | Enable only after the target's overlay-created device node is HIL-confirmed. |
| I2C board bus | Board-defined; peripheral probing not approved | `i2c1`, GPIO2/3, 400 kHz, external 1.8 kΩ pulls; records name RTC and EEPROM but no addresses | Do not provision or probe an assumed device address from this matrix. |
| SPI board bus | Board-defined; peripheral operation not approved | `spi0`, GPIO9/10/11, CS GPIO8, mode 0, 1 MHz | Do not enable a device-specific driver or action: no attached peripheral identity is published. |
| CAN | Constrained | The existing cross-check requires classic CAN only (`fd: false`); the pin map records `CAN_STANDBY` GPIO27 but no controller IRQ or oscillator | Reject CAN FD and do not derive controller setup from this matrix. |
| Controlled GPIO | Supported only for named allocations | `PWR_EN` GPIO17, `PICO_RESET` GPIO22, `CAN_STANDBY` GPIO27, `LED_STATUS` GPIO5; all are 3.3 V logic | Limit output control to the published signal semantics and defaults in the pin map. |
| Reserved GPIO/header functions | Unsupported for module control | GPIO6 (RTC/EEPROM write-protect), GPIO12/13 (fan header), GPIO7 (SPI CE1), and every unlisted header pin | Reject requests that drive or reassign these pins. |

## Compatibility and rejection rules

1. **Revision match is mandatory.** Acadia-OS, Acadia-Configuration, and
   Acadia-Instrumentation must carry the matrix version and board-revision
   contract in their build/provisioning metadata. A missing, mismatched, or
   unsupported board revision must prevent board-specific provisioning and
   peripheral actions.
2. **No inferred hardware support.** A capability listed as board-defined,
   conditionally supported, or constrained is not authorization to invent a
   peripheral identity, address, IRQ, oscillator, or pin allocation. Consumers
   must reject the unsupported action until a later versioned matrix publishes
   the missing hardware facts.
3. **Preserve serial ownership.** Consumers must retain the three-way UART
   allocation: console on `ttyAMA10`, RS-485 on `ttyAMA0`, and Pico link on
   `ttyAMA2`. They must not hard-code a replacement device node.
4. **Respect electrical and pin protections.** All GPIO are 3.3 V logic and
   must not be exposed above 3.3 V without level shifting. Consumers must not
   drive reserved or unlisted header pins.
5. **Verify before release.** The Pico overlay device node remains an explicit
   HIL check. The existing pin-map drift gate must pass before a release cut;
   it cross-checks the hardware allocation with HAL, Configuration, and OS
   source records when those sibling worktrees are present.

## Required downstream integration

This hardware leaf publishes the authority; it does not implement runtime
enforcement. The following work remains with the owning leaves:

- **Acadia-OS:** identify the board revision during image selection or
  provisioning, package only compatible overlays/services, and reject
  unsupported board/peripheral requests.
- **Acadia-Configuration:** consume the matrix version and revision during
  provisioning; reject configuration operations that target unsupported UARTs,
  pins, CAN FD, or unapproved I2C/SPI devices.
- **Acadia-Instrumentation:** expose compatible board capability/version state
  and reject operations outside the selected matrix, including unverified Pico
  transport use.

Those consumers must add their own negative tests for mismatched revisions and
each prohibited action. This document does not claim those tests or enforcement
already exist.
