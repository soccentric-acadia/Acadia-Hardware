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

# The pin-map / electrical-limits contract (task 19) is not yet committed. It is
# tracked and owned, so record it as a NOTE rather than failing the gate.
if find . -iname "*pin*map*" -o -iname "*contract*" 2>/dev/null | grep -q .; then
  note "pin-map / hardware contract present" "task 19 artifact committed"
else
  note "pin-map / hardware contract absent" "tracked by task 19; not part of this gate's pass/fail"
fi

# This repo is never in a fleet build; its gate must not pretend otherwise.
assert "not consumed as a build dependency" \
  '! grep -rqE "add_subdirectory\(.*Acadia-Hardware|Acadia-Hardware" ../Acadia-*/CMakeLists.txt ../Acadia-*/Makefile 2>/dev/null'

[ "$TIER" = "quick" ] && { report "$TIER"; exit $?; }

# --- full ------------------------------------------------------------------
# No build/test/lint for a human-owned readonly reference. Full == quick.
report "$TIER"
