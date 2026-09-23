# Acadia UART allocation (authoritative)

> **Authority** for every serial/UART allocation on Acadia boards. The pin map
> (`pin-map/board_rev_a.json`) is the machine-readable projection of this
> table; Acadia-HAL platform tables, the OS console configuration and the
> WebConfig board manifest are **generated from / cross-checked against** it
> (`tools/check_pin_map.py` gate). Changes are cross-repo breaking events:
> edit the table + pin map together, bump `board_revision`, then update the
> consumers in the same release.
>
> HIL flags mark allocations whose device-node name still needs on-target
> confirmation; every consumer resolves device nodes through HAL accessors
> (`acadia_rs485_uart()` etc.), never a hard-coded `/dev` path, so a node
> rename is a table edit, not a code hunt.

Board scope: Raspberry Pi 5 / CM5 (BCM2712 + RP1), board rev `rpi5-cm5-bom-rev-c`.

## Allocation

| # | UART (RP1) | Pins | Linux device | Owner | Contract |
|---|---|---|---|---|---|
| 1 | UART10 (dedicated debug header) | header-adjacent 3-pin debug connector | `/dev/ttyAMA10` | **OS debug console** (`SERIAL_CONSOLES=115200;ttyAMA10`, getty per F04 policy) | RESERVED — never a module port |
| 2 | UART0 | GPIO14/15 | `/dev/ttyAMA0` | **HAL RS-485** (`RPI5_RS485_UART`, `acadia_rs485_uart()`) | RS-485 half-duplex, TIOCSRS485 direction control |
| 3 | UART2 (overlay `uart2`) | GPIO0/1 | `/dev/ttyAMA2` *(HIL-verify node)* | **Pico W co-processor link** (`RPI5_UART1`, MCU interface) | 115200 8N1, no flow control |

## Decisions recorded (T-P15, HW-004/X-005 re-open)

1. **The Pi 5 console lives on the dedicated debug-header UART** —
   `meta-raspberrypi` sets `SERIAL_CONSOLES = "115200;ttyAMA10"` for Pi 5.
   The earlier pin-map note claiming "UART0 on GPIO14/15 = the OS debug
   console" was wrong for the Pi 5/CM5 machines this board targets.
2. **`/dev/ttyAMA10` is therefore RESERVED**: it is the console, not a
   module port. HAL-501 (RS-485 must not be the debug console) is satisfied
   by returning RS-485 to UART0/GPIO14/15 — the review regression ("Pico
   link and HAL RS-485 default are both /dev/ttyAMA10") is resolved by
   moving RS-485 off the console and the Pico off both.
3. **GPIO0/1 are free for the Pico link**: on this board the module EEPROM
   sits on I2C1 (pin map `i2c[0]`), so the HAT ID-EEPROM function of
   GPIO0/1 (I2C0, ID_SD/ID_SC) is unused — documented board decision. The
   upstream `uart2` overlay routes RP1 UART2 there.
4. **`/dev/ttyS0` does not exist on the Pi 5** (the BCM2711 mini-UART is
   gone); WebConfig manifest serial entries reference only real nodes.
5. **Do-not-touch pins**: everything in the pin map `gpio[]` list is
   owned (PWR_EN 17, PICO_RESET 22, CAN_STANDBY 27, LED_STATUS 5); every
   header pin NOT listed there — in particular GPIO6 (reserved for the
   RTC/EEPROM write-protect strap), GPIO12/13 (PWM fan header) and GPIO7
   (SPI CE1) — is reserved and must not be driven by module code.

## Consumers (single source of truth)

| Consumer | Resolved via |
|---|---|
| Acadia-OS console | `SERIAL_CONSOLES=115200;ttyAMA10` (meta-raspberrypi machine conf) |
| Acadia-HAL RS-485 | `RPI5_RS485_UART = /dev/ttyAMA0`, env override `ACADIA_RS485_UART` |
| Acadia-HAL Pico link | `RPI5_UART1 = /dev/ttyAMA2` |
| WebConfig manifest | `board-manifests/acadia.json` serial peripherals (ttyAMA0, ttyAMA2) |
| Pico overlay | `dtoverlay=uart2` in kas `RPI_EXTRA_CONFIG` |

## Verification gate

`tools/check_pin_map.py` (run in CI, and before any release cut) parses the
pin map and asserts the HAL constants and the WebConfig manifest agree with
this table. Device-node names for overlay-created UARTs are HIL-verified
before a board_revision bump ships.