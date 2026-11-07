#!/usr/bin/env bash
# Run the LoRR simulator with one of our schedulers and/or executors.
#
#   assignment1/run.sh [--scheduler ex1/NAME] [--executor ex2/NAME] [lifelong options]
#
# NAME is a file in that folder (without .py). Without --scheduler / --executor the C++
# defaults are used. Paths for -i / -o / -l are relative to where you call this from.
# Builds the Start-Kit first if it is not built yet.
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
while [ $# -gt 0 ]; do
  case "$1" in
    --scheduler) LORR_SCHEDULER="$(impl "$2")"; export LORR_SCHEDULER
                 args+=(--schedulerPython true); shift 2 ;;
    --executor)  LORR_EXECUTOR="$(impl "$2")"; export LORR_EXECUTOR
                 args+=(--executorPython true); shift 2 ;;
    -i|--inputFile) args+=("$1" "$(realpath "$2")"); shift 2 ;;
    -o|--output|-l|--logFile)
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
exec ./build/lifelong "${args[@]}"
