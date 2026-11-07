# Assignment 1: multi-agent planning

Deadline 10.12.2026, 23:59 (Teach Center). Groups of up to two, 45 + 5 (presentation) points.

| Exercise | Goal | Folder |
| --- | --- | --- |
| [0](ex0/) | Explore the default system (not graded) | `ex0/` |
| [1](ex1/) | Scheduler that completes more tasks than the naive one (20 pts) | `ex1/` |
| [2](ex2/) | Executor that completes more tasks under delays than the naive one (25 pts) | `ex2/` |

## How our code is loaded

The simulator always imports `pyTaskScheduler` from `Start-Kit/python/user_scheduler/` and
`pyExecutor` from `Start-Kit/python/user_executor/`. Those two files are small loaders that load the
file named in `LORR_SCHEDULER` / `LORR_EXECUTOR` instead (default: the naive baselines). So every
scheduler is one file in `ex1/` defining `class pyTaskScheduler`, and every executor is one file in
`ex2/` defining `class pyExecutor`. Helper modules next to them can be imported normally.

## Running

```bash
assignment1/run.sh [--scheduler ex1/NAME] [--executor ex2/NAME] [lifelong options]
```

Without `--scheduler` / `--executor` the C++ defaults are used. The script builds the Start-Kit if
needed and runs it from the right directory; `-i` / `-o` paths are relative to where you call it.

```bash
assignment1/run.sh --scheduler ex1/naive \
    -i Start-Kit/example_problems/random.domain/random-example_400.json \
    -o RunOutput/naive.json -s 1000 -c 3 -d 2
```

`-c 3` writes summary statistics only (use the default `-c 1` for PlanViz), `-d 2` hides info logs,
`-s 200` is a quick smoke test. A run takes about `ticks × 100 ms`.

## Evaluation (Ex. 1 and 2)

Four configurations (naive baselines, own scheduler, own executor, both), at least five runs per
setting with different `delayConfig.seed`, mean and spread. Factors: at least three map domains, team
size (100 / 200 / 400), `numTasksReveal` (1.0 / 1.5 / 3.0), `agentCounter` (1 / 3 / 10), delay
probability (0, default, 10×), planning time `-t` (500 / 1000 / 2000 ms). Metrics: completed tasks,
runtime per call, schedule errors, entry timeouts.
