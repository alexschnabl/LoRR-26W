# Environment setup

How the development environment for this project is set up and what to watch out for.

## Overview

| Item | Value |
| --- | --- |
| OS | Windows 11 + WSL 2, distro `Ubuntu-24.04` (24.04.5 LTS) |
| Compiler / build | g++ 13.3, CMake 3.28 |
| Boost | 1.83 (`program_options`, `system`, `filesystem`, `log` from apt) |
| Python | 3.12 system Python; numpy, scipy, matplotlib, pandas, pillow, tk from apt |
| pybind11 | **3.0.1, built from source into `/usr/local`** (apt ships 2.11; the Start-Kit needs ≥ 3.0.1) |
| PlanViz | venv in `/opt/planviz-venv` with `PlanViz/requirements.txt` (numba is not in apt) |
| `planviz` command | `/usr/local/bin/planviz` → `tools/planviz_launch.py` → `PlanViz/script/run.py` |

Everything above is installed by [`tools/setup_wsl.sh`](../tools/setup_wsl.sh), which is idempotent and
must run as root. From Windows, in the repository root:

```powershell
wsl -d Ubuntu-24.04 -u root -- bash tools/setup_wsl.sh
```

Re-run it after moving the repository, because the `planviz` wrapper stores the absolute path of the
launcher.

The official competition environment is Ubuntu 22.04 with a conda Python (PyTorch image). For the course
only our own evaluation matters, so the Ubuntu 24.04 setup is sufficient. `Start-Kit/pip.txt` lists
`torch`; it is not installed and not needed so far.

## Building

```bash
cd Start-Kit
cmake -B build ./ -DCMAKE_BUILD_TYPE=Release
make -C build -j"$(nproc)"
```

A full build takes about 40 s with 24 threads. The build directory stores absolute paths, so delete it
and rebuild after moving the repository.

## Gotchas

- **Line endings.** The Start-Kit's shell scripts must keep LF endings to run in WSL. The repository's
  `.gitattributes` enforces LF; with Windows git also set `core.autocrlf=false` for this repository.
- **Working directory.** `lifelong` must be started from `Start-Kit/`: the Python scheduler and
  executor are imported from `python/user_scheduler` and `python/user_executor` relative to the current
  directory.
- **Instance paths.** `mapFile`, `agentFile` and `taskFile` in an instance JSON are resolved relative
  to that JSON file. Variants outside `example_problems/` must rewrite them (see
  [`experiments/ex0/make_variants.py`](../experiments/ex0/make_variants.py)).
- **Output directory.** `lifelong` aborts if the directory of `-o` does not exist.
- **Default WSL distro.** If another distro (e.g. `docker-desktop`) is the default, always pass
  `-d Ubuntu-24.04`. From PowerShell, nested quotes and `$(...)` get mangled; put multi-step commands
  into a `.sh` file and run `wsl -d Ubuntu-24.04 -- bash file.sh`.
- **PlanViz on multiple monitors.** WSLg reports all monitors as one X screen (e.g. 5120×1440), and
  PlanViz sizes its window from that, so the window spans every monitor.
  [`tools/planviz_launch.py`](../tools/planviz_launch.py) makes Tk report the Windows primary monitor's
  work area (× 0.85) and centres the window there, without modifying PlanViz.
  Override with `PLANVIZ_SCREEN=WxH` or `PLANVIZ_SCALE=0.7`.
- `start-wsl.bat` (double-click in Explorer) opens a WSL shell in `Start-Kit/`.

## Run time

The simulator runs in (roughly) real time. In the main loop (`src/CompetitionSystem.cpp`) each
execution tick gets `actionMoveTimeLimit` (`-a`, default 100 ms). A new planning call starts every
`planCommTimeLimit / actionMoveTimeLimit` ticks (`-t` 1000 / 100 = every 10 ticks), and the loop waits
on the wall clock until the planner returns or its budget is used up. The default planner is
*anytime* and uses almost all of its budget, so

    wall time ≈ simulationTime × actionMoveTimeLimit ≈ 1000 × 100 ms ≈ 100 s   (measured: 87 s)

Lowering `-t` alone does not help (more, shorter planning rounds). Lowering `-a` and `-t` together
does, but the planner gets less time and results are no longer comparable.

What helps:

- **Run experiments in parallel.** Each run uses about 1–2 cores. With 24 logical cores, about 8 runs
  at once is safe; many more steal CPU from the anytime planner and change the results.
- `-d 2` (warnings only) or `-l run.log` avoids flooding the terminal with "task revealed" messages.
- `-c 3` writes summary-only output (small and fast); PlanViz needs the full output (`-c 1`).
- `-s 200` (about 20 s) for smoke tests during development.

## Default C++ scheduler vs. naive Python scheduler

With `--schedulerPython true` only the scheduler changes; planner and executor stay the C++ defaults.

- **C++ default** (`default_planner/scheduler.cpp`): greedy. Every free robot takes the open task with
  the shortest exact path (BFS distances) through all of its errands.
- **Python naive** (`python/user_scheduler/pyTaskScheduler.py` as shipped): free robots in id order
  each take the open task with the **lowest id**, ignoring distance. This is the baseline Exercise 1 has
  to beat.
