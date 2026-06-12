# CLAUDE.md — Acadia-Hardware

This file provides guidance to Claude Code (claude.ai/code) when working
with code in this repository.

The master SoCcentric CLAUDE.md (`~/.claude/CLAUDE.md`) applies in full
and **wins on any conflict** — flag the conflict to the user. This file
adds only local knowledge specific to `Acadia-Hardware`.

## What this repo is

`Acadia-Hardware` is one of the 7 components of the Acadia project, and
the **design source of truth** for the Acadia platform. Per global
CLAUDE.md §3, Acadia targets the Raspberry Pi CM4/CM5 with a Pico W
(RP2040) co-processor. Per global §4, the `*-Hardware` component holds
schematics / PCB / CAD and is **read-only design context** — see the
"Hard rules" section below.

## Hard rules (apply on top of the master CLAUDE.md)

These are easy to forget and bite hard:

- **`*-Hardware` is read-only.** Per global §4, Claude must **never**
  modify, build, or file *code* issues against this repo. Hardware
  design changes are done by a human hardware engineer and committed
  directly. The legitimate Claude work here is **review** (verifying
  the design and the README against requirements) and **README
  cleanup** — never the design itself.
- **No interface contract changes from this repo.** The HAL API, gRPC
  `.proto`, `.fbs`, GraphQL schema, and PySDK public API (per global
  §4) live in their owning component repos. If a design change would
  force a contract change, the request originates in the *consumer*
  (`Acadia-HAL` etc.), not here.
- **No submodules, no live secrets** (global §⛔ rules).
- **No tagging / no releases** from this repo unless explicitly told.
  Release flow goes through the root `project-managers` Makefile,
  which reads `.version`.

## Current state (as of last Claude visit, 2026-06-12)

Tracked files in the working tree:

- `README.md` — populated (Description, Setup, Usage all
  replaced; commits `6644980`, `b022314`, `c13f9be` on
  `develop`).
- `CLAUDE.md` — this file (added by `/init`, updated by the
  fix in this branch).

Still missing (tracked as open or closed `requirements` issues):

- No design source files — #4 (closed: human hardware engineer's
  call per global §4).
- No `Makefile` — #5 (closed: human hardware engineer's call).
- No `LICENSE` — #6 (closed: business decision, not a code
  review).
- No `.gitignore` — #7 (closed: depends on EDA tool choice).
- No EDA tool version pin — #8 (closed: depends on EDA tool
  choice).
- No `docs/` directory — implied by the missing design (#4).

Branches: `develop`, `main`, `release` all at `c13f9be` (the
last fix-merge commit on `develop`).

**Implication for future Claude sessions:** the docs surface is
honest; the design surface is still empty. The most useful work
is `gh issue list --state open --label requirements` to see what
review findings are still open. Anything that touches design
content (schematics, PCB, BOM, gerbers) routes to the human
hardware engineer.

## Build / Test / Lint

Per global §12, a top-level `Makefile` is **mandatory** for every
component repo, with at minimum `help`, `build`, `test`, `lint`,
`run`, `clean` targets. For a Hardware repo the targets adapt to the
EDA domain (e.g. `make build` runs DRC/ERC, `make run` generates
gerbers). This repo currently has **no Makefile** — the gap is
tracked as an open `requirements`-labelled issue.

When the Makefile is added, validate via `make help && make -n build
test lint run clean` and then run the full `make build && make test
&& make lint` triple (per global §9 step 6) before any push. Any
actual command that succeeds should be appended to **Do** below; any
that fails (and the fix) should go in **Don't**.

## Architecture / structure

The repo will eventually be organised roughly as:

```
Acadia-Hardware/
├── Makefile                  # entry point (see §12)
├── README.md
├── CLAUDE.md                 # this file
├── LICENSE                   # required — hardware without a license
│                             # is not legally usable downstream
├── hardware/                 # EDA project (KiCad / Altium / EAGLE)
│   ├── Acadia.<ext>          # project file
│   ├── schematics/
│   ├── pcb/
│   ├── libraries/            # symbols, footprints, 3D models
│   └── manufacturing/<rev>/  # gerbers, drill, BOM, POS per board rev
├── docs/                     # pin map, revision history, errata
└── .gitignore                # exclude EDA temp / autosave / backup
```

This is a target shape, not a current one — it should be confirmed
against whatever the human hardware engineer lands first.

## Do

_(Empty — populate as commands succeed. Per global §11, every
working command goes here. Examples of what will eventually land: "Run
DRC: `make build` (wraps `kicad-cli pcb drc ...`)", "Generate
gerbers: `make run` (wraps `kicad-cli pcb export gerbers ...`)",
"Validate: `make build && make test && make lint`".)_

## Don't

- Don't add code, schematics, PCB layouts, or symbol/footprint
  libraries to this repo. The `*-Hardware` repo is read-only design
  context (global §4). A human hardware engineer owns the design;
  Claude files review findings, never implements them.
- Don't create an EDA project, BOM, or gerber outputs. Even if a
  user asks, surface the global §4 rule and route the request to the
  hardware engineer.
- Don't write the README "Description" / "Setup" / "Usage" sections
  from imagination. Those sections must describe the *real* design;
  prose written before the design lands will be wrong or aspirational
  and will be rejected by §9 step 6 validation.
- Don't add tags or bump versions in this repo. The root
  `project-managers` Makefile is the only release path; it reads
  `.version` and tags every leaf.
- Don't commit secrets. The global `GH_TOKEN` env var is the only
  auth; never embed it.
- Don't add `.gitmodules` or use `git submodule` (global §⛔).
- Don't file *code* issues (memory-safety, concurrency, etc.) here —
  there is no code in this repo. The `requirements` label is the
  right label for design-vs-requirements findings; `bug`/`security`/
  etc. belong in the consuming component (`Acadia-HAL`,
  `Acadia-OS`, …).
