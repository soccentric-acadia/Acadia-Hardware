# Acadia-Hardware

Design source of truth for the **Acadia** platform. Acadia is one of
the 9 SoCcentric projects and targets the **Raspberry Pi CM4/CM5** as
the application processor with a **Pico W (RP2040)** as the real-time
co-processor (see the global `~/.claude/CLAUDE.md` §3).

This repository holds the **schematics, PCB layout, BOM, and
manufacturing artefacts** for the Acadia board. It is the
authoritative hardware definition that the other six Acadia
components (`Acadia-HAL`, `Acadia-OS`, `Acadia-Client`,
`Acadia-Server`, `Acadia-Dashboard`, `Acadia-PySDK`) validate
against. Per global §4, this repo is **read-only design context** —
design changes are committed by a human hardware engineer.

**Design status:** in design (no committed EDA project yet). See the
[open issues](https://github.com/SiliconCentric/Acadia-Hardware/issues)
for the gaps; the planned layout is under `hardware/Acadia.<ext>`.

## Description

What lives here:

- The Acadia board schematic and PCB layout.
- The symbol, footprint, and 3D-model libraries the project uses.
- The BOM, gerbers, drill, and pick-and-place outputs per board
  revision, under `hardware/manufacturing/<rev>/`.
- A pin map, a revision history, and any hardware errata, under
  `docs/`.

What does **not** live here:

- Code that runs on the board — that belongs in `Acadia-OS`,
  `Acadia-HAL`, etc.
- The HAL API, gRPC `.proto`, FlatBuffers `.fbs`, GraphQL schema, or
  PySDK public API. Those interface contracts live in their owning
  component repos.

## Setup

Add setup instructions here.

## Usage

Add usage instructions here.
