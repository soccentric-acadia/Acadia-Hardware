#!/usr/bin/env python3
"""check_pin_map.py — UART/GPIO allocation drift gate (T-P15, HW-003).

Parses the executable pin map and asserts the consumers agree with it:

  1. pin map structural sanity: contract_version, board_revision, unique
     linux_device per UART consumer, do-not-touch pins don't collide with
     owned GPIO,
  2. Acadia-HAL platform_rpi5.h constants match the allocation table
     (RS-485, Pico link, debug console),
  3. the WebConfig board manifest (acadia.json) serial entries match and
     CAN fd is false (MCP2515 is classic CAN only),
  4. the OS console device (SERIAL_CONSOLES) is the reserved debug UART.

Exit 1 on any drift. Run before any release cut and in CI.
"""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
REPO_ROOT = ROOT.parent

PIN_MAP = ROOT / "pin-map" / "board_rev_a.json"
HAL_HEADER = REPO_ROOT / "Acadia-HAL" / "src" / "platform_rpi5.h"
CFG_MANIFEST = REPO_ROOT / "Acadia-Configuration" / "board-manifests" / "acadia.json"
OS_MACHINE_CONF = (
    REPO_ROOT
    / "Acadia-OS"
    / "layers"
    / "meta-raspberrypi"
    / "conf"
    / "machine"
    / "raspberrypi5.conf"
)

failures: list[str] = []


def check(cond: bool, msg: str) -> None:
    if not cond:
        failures.append(msg)


def hal_const(name: str, text: str) -> str:
    for line in text.splitlines():
        if f"constexpr const char* {name}" in line:
            return line.split('"')[1]
    return ""


def serial_ok(serials: dict) -> bool:
    return serials == {
        "ttyAMA0": "/dev/ttyAMA0",  # RS-485 (GPIO14/15)
        "ttyAMA2": "/dev/ttyAMA2",  # Pico link (GPIO0/1)
    }


def main() -> int:
    m = json.loads(PIN_MAP.read_text())
    check(m.get("contract_version") == "1.0", "pin map contract_version must be 1.0")
    check(m["board_revision"] == "rpi5-cm5-bom-rev-c", "board_revision drifted")
    check(m.get("updated") == "2026-09-23", "pin map 'updated' not current for rev-c")

    # 1. unique linux_device per UART row
    devices = [u.get("linux_device") for u in m["uart"]]
    check(len(devices) == len(set(devices)), f"uart rows share a linux_device: {devices}")

    # owner contract (doc/uart-allocation.md)
    by_dev = {u["linux_device"]: u for u in m["uart"]}
    check(
        by_dev.get("/dev/ttyAMA10", {}).get("owner") == "os_debug_console"
        and by_dev["/dev/ttyAMA10"].get("reserved") is True,
        "ttyAMA10 must be the reserved OS debug console",
    )
    check(
        by_dev.get("/dev/ttyAMA0", {}).get("owner") == "hal_rs485",
        "/dev/ttyAMA0 (GPIO14/15) must be owned by HAL RS-485 (HAL-501)",
    )
    check(
        by_dev.get("/dev/ttyAMA2", {}).get("owner") == "pico_link",
        "/dev/ttyAMA2 (GPIO0/1, uart2 overlay) must be the Pico link",
    )
    check(
        m["pico_uart"]["linux_device"] == "/dev/ttyAMA2",
        "pico_uart linux_device must be /dev/ttyAMA2 (console is ttyAMA10, RS-485 is ttyAMA0)",
    )

    # do-not-touch must not overlap owned gpio
    owned = {g["rpi_gpio"] for g in m["gpio"]}
    for pin in m["do_not_touch"]["pins"]:
        check(
            pin["rpi_gpio"] not in owned,
            f"do-not-touch pin GPIO{pin['rpi_gpio']} is also an owned gpio[] entry",
        )

    # 2. HAL constants
    hal = HAL_HEADER.read_text()
    check(
        hal_const("RPI5_RS485_UART", hal) == "/dev/ttyAMA0",
        "HAL RPI5_RS485_UART must be /dev/ttyAMA0 (uart-allocation.md row 2)",
    )
    check(
        hal_const("RPI5_UART1", hal) == "/dev/ttyAMA2",
        "HAL RPI5_UART1 (Pico link) must be /dev/ttyAMA2 (uart-allocation.md row 3)",
    )
    check(
        hal_const("RPI5_DEBUG_UART", hal) == "/dev/ttyAMA10",
        "HAL RPI5_DEBUG_UART must be /dev/ttyAMA10 (dedicated debug header = console)",
    )

    # 3. WebConfig manifest serial entries
    cfg = json.loads(CFG_MANIFEST.read_text())
    serials = {p["id"]: p["device"] for p in cfg["peripherals"] if p.get("kind") == "serial"}
    check(
        serial_ok(serials),
        f"WebConfig manifest serial entries must match the allocation: {serials}",
    )
    for c in (p for p in cfg["peripherals"] if p.get("kind") == "can"):
        check(
            c.get("caps", {}).get("fd") is False,
            f"{c['id']}: fd must be false — MCP2515 is classic CAN only (HW-009)",
        )

    # 4. OS console device
    if OS_MACHINE_CONF.exists():
        check(
            "ttyAMA10" in OS_MACHINE_CONF.read_text(),
            "SERIAL_CONSOLES must keep the console on the dedicated debug header (/dev/ttyAMA10)",
        )
    else:
        print("NOTE: raspberrypi5.conf not found — OS console cross-check skipped")

    if failures:
        print("PIN-MAP DRIFT:")
        for f in failures:
            print(f"  FAIL: {f}")
        return 1
    print(f"pin map drift gate: OK ({m['board_revision']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())