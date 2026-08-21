# Acadia-Hardware Build and Deployment

## Scope

Acadia-Hardware is the hardware inventory/board-definition leaf. At the time of this guide, the
repository contains identity and hardware documentation but no Makefile, package manifest, build
manifest, board build target, executable, deployment script, or automated test command.

## 1. Prerequisites

No repository-specific toolchain is declared. For documentation-only work, use a Markdown editor
and the repository's normal review tooling. Any future board description, electrical validation,
or acceptance harness must define its own prerequisites before commands can be documented.

## 2. Setup

There is no setup command. Read the existing `README.md` and `CLAUDE.md` files for the current
hardware scope and planned interfaces. Do not assume that a sibling HAL or OS build consumes
this tree automatically.

## 3. Build and compile

No build or compile target exists. Do not run `make`, CMake, Cargo, npm, or Python packaging
commands in this leaf expecting an artifact.

## 4. Test and lint

No test or lint command is declared in this repository. Hardware acceptance, pinout, revision,
and interface checks remain manual until an executable test harness and its build configuration
are added.

## 5. Packaging and artifacts

No package or artifact target exists. There is currently no image, firmware, board manifest
bundle, library, or installer produced by this leaf.

## 6. Deployment, install, and run

No install, deployment, runtime, or cloud command exists. Hardware records must be applied
through the owning OS/HAL/product deployment process once those consumers and their exact
interfaces are established.

## 7. Cleanup

No repository-specific cleanup target exists. There are no declared build or package directories
to remove.

## 8. Hardware, cloud, and manual verification caveats

This repository is hardware-specific by purpose but currently has no executable verification
surface. Board identity, revision, component inventory, pinout, electrical constraints,
peripheral availability, HAL compatibility, and acceptance testing all require manual review
against the physical design and target hardware. Do not treat the presence of documentation as
proof of an assembled or supported board. Cloud deployment is out of scope.
