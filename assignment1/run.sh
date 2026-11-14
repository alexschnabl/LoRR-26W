#!/usr/bin/env bash
# Run the LoRR simulator with one of our schedulers and/or executors.
#
#   assignment1/run.sh [--scheduler ex1/NAME] [--executor ex2/NAME] [lifelong options]
#
# NAME is a file in that folder (without .py). Without --scheduler / --executor the C++
# defaults are used. Paths for -i / -o / -l are relative to where you call this from.
# Builds the Start-Kit first if it is not built yet and prints a summary at the end.
#
# Example:
#   assignment1/run.sh --scheduler ex1/naive \
#       -i Start-Kit/example_problems/random.domain/random-example_400.json \
#       -o RunOutput/naive.json -s 1000 -c 3
set -euo pipefail

A1="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KIT="$(cd "$A1/../Start-Kit" && pwd)"

impl() {  # impl <folder/name> -> absolute .py path, or exit
  local f="$A1/${1%.py}.py"
  [ -f "$f" ] || { echo "not found: $f" >&2; exit 1; }
  echo "$f"
}

args=()
out="$KIT/output.json"
while [ $# -gt 0 ]; do
  case "$1" in
    --scheduler) LORR_SCHEDULER="$(impl "$2")"; export LORR_SCHEDULER
                 args+=(--schedulerPython true); shift 2 ;;
    --executor)  LORR_EXECUTOR="$(impl "$2")"; export LORR_EXECUTOR
                 args+=(--executorPython true); shift 2 ;;
    -i|--inputFile) args+=("$1" "$(realpath "$2")"); shift 2 ;;
    -o|--output) mkdir -p "$(dirname "$2")"; out="$(realpath -m "$2")"; args+=("$1" "$out"); shift 2 ;;
    -l|--logFile)
                 mkdir -p "$(dirname "$2")"; args+=("$1" "$(realpath -m "$2")"); shift 2 ;;
    *)           args+=("$1"); shift ;;
  esac
done

if [ ! -x "$KIT/build/lifelong" ]; then
  cmake -S "$KIT" -B "$KIT/build" -DCMAKE_BUILD_TYPE=Release
  make -C "$KIT/build" -j"$(nproc)"
fi

# The simulator imports the Python modules relative to the working directory.
cd "$KIT"
./build/lifelong "${args[@]}"

# Summary of the output JSON
python3 - "$out" <<'EOF'
import json, sys
d = json.load(open(sys.argv[1]))
rows = [("Tasks finished", "numTaskFinished"), ("Schedule errors", "numScheduleErrors"),
        ("Planner errors", "numPlannerErrors"), ("Entry timeouts", "numEntryTimeouts"),
        ("Robots", "teamSize"), ("Ticks", "makespan")]
print()
for label, key in rows:
    print(f"{label:<16} {d.get(key, '-'):>6}")
print(f"{'Output':<16} {sys.argv[1]}")
EOF
