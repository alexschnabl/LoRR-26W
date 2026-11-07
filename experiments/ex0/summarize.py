"""Print a table of the summary fields of every output JSON in a folder.

Usage:  python3 experiments/ex0/summarize.py RunOutput/ex0
"""
import json
import sys
from pathlib import Path

FIELDS = ["teamSize", "agentMaxCounter", "numTaskFinished", "numScheduleErrors",
          "numPlannerErrors", "numEntryTimeouts", "makespan"]


def main(folder):
    rows = []
    for path in sorted(Path(folder).glob("*.json")):
        data = json.loads(path.read_text())
        rows.append([path.stem] + [str(data.get(f, "")) for f in FIELDS])
    if not rows:
        print(f"no output files in {folder}")
        return
    header = ["run"] + FIELDS
    widths = [max(len(r[i]) for r in rows + [header]) for i in range(len(header))]
    for row in [header] + rows:
        print("  ".join(cell.ljust(w) for cell, w in zip(row, widths)))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "RunOutput/ex0")
