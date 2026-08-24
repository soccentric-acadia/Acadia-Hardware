#!/usr/bin/env bash
# Acadia-Hardware — per-repo validation gate.
#
# Hardware is HUMAN-OWNED and READONLY (fleet-deps.yaml: category none,
# stack none). It is never built by an automated pipeline and is never edited
# by an agent (listing it in a loop's repos: is a scope violation). Its "gate"
# is therefore a reference-integrity check, not a build gate: it confirms the
# human-owned design references are present and warns on anything that would
# silently go stale.
#
#   quick   seconds. Reference integrity.
#   full    same as quick — there is no build to run.
set -uo pipefail
# shellcheck source=lib/validate-lib.sh
source "$(dirname "${BASH_SOURCE[0]}")/lib/validate-lib.sh"

TIER="$(tier_or_die "${1:-quick}")"

# --- quick -----------------------------------------------------------------

assert "README present (human-owned reference)" 'test -f README.md'
assert "CLAUDE.md present (owner contract)" 'test -f CLAUDE.md'

# The pin-map / electrical-limits contract (task 19) is the executable artifact
# OS/HAL consume. Its presence is a hard requirement of this gate.
check "pin-map JSON is valid + versioned" "python3" \
  'python3 - <<PY
import json, glob, sys
files = glob.glob("pin-map/*.json")
if not files:
    print("no pin-map/*.json contract present"); sys.exit(1)
for f in files:
    d = json.load(open(f))
    for k in ("board_revision", "gpio", "electrical_limits"):
        if k not in d:
            print(f"{f} missing required key {k}"); sys.exit(1)
    if not isinstance(d["gpio"], list):
        print(f"{f} gpio must be a list"); sys.exit(1)
    rev = d["board_revision"]
    print(f"OK: {len(files)} pin-map file(s), board_revision={rev}")
PY'

# This repo is never in a fleet build; its gate must not pretend otherwise.
assert "not consumed as a build dependency" \
  '! grep -rqE "add_subdirectory\(.*Acadia-Hardware|Acadia-Hardware" ../Acadia-*/CMakeLists.txt ../Acadia-*/Makefile 2>/dev/null'

[ "$TIER" = "quick" ] && { report "$TIER"; exit $?; }

# --- full ------------------------------------------------------------------
# No build/test/lint for a human-owned readonly reference. Full == quick.
report "$TIER"
