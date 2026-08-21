# Acadia-Hardware

## Project Description

Acadia-Hardware is intended to be the electrical design source of truth for the Acadia platform:
schematics, PCB layout, component libraries, bill of materials, manufacturing exports, pin
mapping, revision history, and errata. The design context names a Raspberry Pi CM4/CM5
application processor paired with a Pico W/RP2040 real-time co-processor. Downstream software
repositories consume its board facts when implementing HAL, OS, Client, Server, Dashboard, and
PySDK behavior; interface contracts remain owned by those software repositories.

The repository is currently not an implemented EDA project. Existing documentation explicitly
says that no committed EDA project, schematic, PCB, library, manufacturing bundle, or automated
export target is present. This README therefore records planned deliverables and repository
relationships rather than pretending a board revision exists. There is no executable source,
hardware test suite, or software build to run. The expected future workflow is to open the EDA
project under `hardware/`, run electrical/design-rule checks, export a revisioned BOM and
manufacturing files, and publish a pin map and revision history.

The useful current actions are documentation and issue review: read `CLAUDE.md`, inspect the
design gaps, and coordinate changes with the human hardware engineer. Downstream teams should
treat electrical assumptions as provisional until the first design revision is committed and
reviewed. Manufacturing partners should not infer that Gerbers, drill files, pick-and-place
data, or a BOM are available from this checkout.

## Feature Status

| # | Name / Description | Implemented? | Test Coverage? | Manual Test |
|---:|---|---|---|---|
| 1 | Design repository and ownership documentation | Implemented | Documentation only | [ ] Manual verification required |
| 2 | Raspberry Pi CM4/CM5 plus Pico W/RP2040 definition | Planned | None | [ ] Manual verification required |
| 3 | Schematic project | Planned: no committed EDA project | None | [ ] Manual verification required |
| 4 | PCB layout | Planned: no committed EDA project | None | [ ] Manual verification required |
| 5 | Symbols, footprints, and 3D models | Planned | None | [ ] Manual verification required |
| 6 | Pin map and revision history | Planned | None | [ ] Manual verification required |
| 7 | BOM, Gerbers, drill, and pick-and-place exports | Planned | None | [ ] Manual verification required |
| 8 | ERC/DRC and manufacturing automation | Planned | None | [ ] Manual verification required |
| 9 | Downstream electrical-consumer contract | Partial: relationship documented; data absent | None | [ ] Manual verification required |
| 10 | Hardware errata and revision records | Planned | None | [ ] Manual verification required |

Design source of truth for the **Acadia** platform. Acadia is one of the 9 SoCcentric projects
and targets the **Raspberry Pi CM4/CM5** as the application processor with a **Pico W (RP2040)**
as the real-time co-processor (see the global `~/.claude/CLAUDE.md` §3).

This repository holds the **schematics, PCB layout, BOM, and manufacturing artefacts** for the
Acadia board. It is the authoritative hardware definition that the other six Acadia components
(`Acadia-HAL`, `Acadia-OS`, `Acadia-Client`, `Acadia-Server`, `Acadia-Dashboard`,
`Acadia-PySDK`) validate against. Per global §4, this repo is **read-only design context** —
design changes are committed by a human hardware engineer.

**Design status:** in design (no committed EDA project yet). See the [open
issues](https://github.com/soccentric-acadia/Acadia-Hardware/issues) for the gaps; the planned
layout is under `hardware/Acadia.<ext>`.

## Description

What lives here:

- The Acadia board schematic and PCB layout.
- The symbol, footprint, and 3D-model libraries the project uses.
- The BOM, gerbers, drill, and pick-and-place outputs per board revision, under
`hardware/manufacturing/<rev>/`.
- A pin map, a revision history, and any hardware errata, under `docs/`.

What does **not** live here:

- Code that runs on the board — that belongs in `Acadia-OS`, `Acadia-HAL`, etc.
- The HAL API, gRPC `.proto`, FlatBuffers `.fbs`, GraphQL schema, or PySDK public API. Those
interface contracts live in their owning component repos.

## Setup

This repository is the design source of truth. "Setup" here means opening and validating the EDA
project, not building or running code.

### Current state

The EDA project has not been committed yet (tracked by #4). Until the hardware engineer lands
the design:

1. Clone the repo.
2. Read this `README.md` and [`CLAUDE.md`](./CLAUDE.md).
3. Read the [open issues](https://github.com/soccentric-acadia/Acadia-Hardware/issues) to see
the gaps.

### Once the EDA project is committed

The expected workflow (to be added to [`CLAUDE.md`](./CLAUDE.md) **Do** as the engineer confirms
each step):

1. **Open the project** with the EDA tool pinned in `tools/<eda>.version` (or equivalent —
tracked by #8). Common choice: **KiCad 8.x**.
2. **Locate the source files** under `hardware/`:
- `hardware/Acadia.<ext>` — the project file (e.g. `Acadia.kicad_pro`).
- `hardware/schematics/` — schematic sheets.
- `hardware/pcb/` — PCB layout.
- `hardware/libraries/` — project-local symbols, footprints, 3D models.
3. **Build the BOM** — `make run` (or the equivalent) should export a CSV to
`hardware/manufacturing/<rev>/BOM.csv`.
4. **Run DRC / ERC** — `make build` runs design-rule and electrical-rule checks. The CI /
pre-push step (`make build && make test && make lint`, per global §9 step 6) must pass.
5. **Produce gerbers / drill / POS** — `make run` writes outputs to
`hardware/manufacturing/<rev>/` for the contract manufacturer.

For the moment, the only setup is to clone the repo and read this README. Manufacturing partners
should request the gerber / BOM bundle from the hardware engineer — there is no automated
export target yet.

## Usage

This repository is the **design source of truth** for the Acadia board. "Usage" here is the
workflow downstream components and manufacturing partners follow when consuming the design.

### Who consumes this design

| Consumer | What they take from here | Tracking issue (open) |
|---|---|---|
| `Acadia-HAL` | Exported netlist, pin map, and any HAL-relevant board notes | #4 (export tooling) |
| `Acadia-OS` | Pin map → device tree, board revision for the BSP | #4 (export tooling) |
| `Acadia-Client`, `Acadia-Server`, `Acadia-Dashboard`, `Acadia-PySDK` | Validate their logic against the manufactured board (post-prototype) | n/a |
| Contract manufacturer (CM) | Gerbers, drill, BOM, pick-and-place files | #4 (artefacts not yet generated) |

### Revision history

A revision-history table is added to `docs/REVISIONS.md` once the first board revision is
committed. Format:

| Rev | Date | Changes | Known errata |
|---|---|---|---|
| _none yet_ | — | — | — |

### Contracts surfaced by this design

This repo is the source of truth for **electrical** behaviour; it is **not** the source of truth
for any interface contract. The following contracts are owned by their respective component
repos and must not be changed from here:

- **HAL API** — `Acadia-HAL/include/`
- **gRPC `.proto` + FlatBuffers `.fbs`** — `Acadia-Client/proto/`
- **GraphQL schema** — `Acadia-Server/graphql/`
- **PySDK public API** — `Acadia-PySDK/`

If a board revision forces a contract change, the change originates in the consumer component
and is approved per global §5. This repo simply records the design; it does not unilaterally
change contracts.
