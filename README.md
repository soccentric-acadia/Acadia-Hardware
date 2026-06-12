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

This repository is the design source of truth. "Setup" here means
opening and validating the EDA project, not building or running
code.

### Current state

The EDA project has not been committed yet (tracked by #4). Until
the hardware engineer lands the design:

1. Clone the repo.
2. Read this `README.md` and [`CLAUDE.md`](./CLAUDE.md).
3. Read the [open issues](https://github.com/SiliconCentric/Acadia-Hardware/issues)
   to see the gaps.

### Once the EDA project is committed

The expected workflow (to be added to [`CLAUDE.md`](./CLAUDE.md)
**Do** as the engineer confirms each step):

1. **Open the project** with the EDA tool pinned in
   `tools/<eda>.version` (or equivalent — tracked by #8). Common
   choice: **KiCad 8.x**.
2. **Locate the source files** under `hardware/`:
   - `hardware/Acadia.<ext>` — the project file (e.g. `Acadia.kicad_pro`).
   - `hardware/schematics/` — schematic sheets.
   - `hardware/pcb/` — PCB layout.
   - `hardware/libraries/` — project-local symbols, footprints, 3D
     models.
3. **Build the BOM** — `make run` (or the equivalent) should export
   a CSV to `hardware/manufacturing/<rev>/BOM.csv`.
4. **Run DRC / ERC** — `make build` runs design-rule and
   electrical-rule checks. The CI / pre-push step (`make build &&
   make test && make lint`, per global §9 step 6) must pass.
5. **Produce gerbers / drill / POS** — `make run` writes outputs to
   `hardware/manufacturing/<rev>/` for the contract manufacturer.

For the moment, the only setup is to clone the repo and read this
README. Manufacturing partners should request the gerber / BOM
bundle from the hardware engineer — there is no automated export
target yet.

## Usage

Add usage instructions here.
