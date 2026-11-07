"""Write the Exercise 0 instance variants of random-example_400.json.

Each variant changes one parameter (numTasksReveal or agentCounter) and keeps the rest.
Map, agent and task paths in an instance file are resolved relative to that file, so the
variants rewrite them to point back into the Start-Kit's example_problems folder.

Usage (from the repository root):  python3 experiments/ex0/make_variants.py
"""
import json
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = HERE.parents[1] / "Start-Kit" / "example_problems" / "random.domain" / "random-example_400.json"
OUT = HERE / "instances"

SWEEPS = {
    "numTasksReveal": [1.0, 1.5, 3.0],
    "agentCounter": [1, 3, 10],
}


def main():
    base = json.loads(BASE.read_text())
    OUT.mkdir(exist_ok=True)
    for key in ("mapFile", "agentFile", "taskFile"):
        target = BASE.parent / base[key]
        base[key] = Path(os.path.relpath(target, OUT)).as_posix()

    for param, values in SWEEPS.items():
        for value in values:
            inst = dict(base, **{param: value})
            path = OUT / f"random400_{param}-{value}.json"
            path.write_text(json.dumps(inst, indent=4) + "\n", newline="\n")
            print(path.relative_to(HERE.parents[1]))


if __name__ == "__main__":
    main()
