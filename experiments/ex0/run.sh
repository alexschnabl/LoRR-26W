#!/usr/bin/env bash
# Exercise 0: run every instance in experiments/ex0/instances/ with the default C++ system.
# Runs in parallel (JOBS at a time) and writes summary-only outputs to RunOutput/ex0/.
#
# Usage (inside WSL, from the repository root):
#   bash experiments/ex0/run.sh            # 1000 ticks, summary output
#   STEPS=200 bash experiments/ex0/run.sh  # quick smoke test
#   EXTRA="--schedulerPython true" bash experiments/ex0/run.sh
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
STEPS="${STEPS:-1000}"
JOBS="${JOBS:-8}"          # each run uses 1-2 cores; too many in parallel distorts results
OUTPUT_LEVEL="${OUTPUT_LEVEL:-3}"  # 3 = summary only; use 1 for PlanViz
EXTRA="${EXTRA:-}"
OUT="$ROOT/RunOutput/ex0"
LIFELONG="$ROOT/Start-Kit/build/lifelong"

[ -x "$LIFELONG" ] || { echo "Build the Start-Kit first (see README)." >&2; exit 1; }
mkdir -p "$OUT"
shopt -s nullglob
instances=("$ROOT"/experiments/ex0/instances/*.json)
[ ${#instances[@]} -gt 0 ] || { echo "No instances; run make_variants.py first." >&2; exit 1; }

# The Python scheduler/executor are imported relative to the working directory.
cd "$ROOT/Start-Kit"
printf '%s\n' "${instances[@]}" | xargs -P "$JOBS" -I{} bash -c '
  name=$(basename "{}" .json)
  "$0" -i "{}" -o "$1/$name.json" -s "$2" -c "$3" -d 2 -l "$1/$name.log" $4 \
    && echo "done: $name"
' "$LIFELONG" "$OUT" "$STEPS" "$OUTPUT_LEVEL" "$EXTRA"

python3 "$ROOT/experiments/ex0/summarize.py" "$OUT"
