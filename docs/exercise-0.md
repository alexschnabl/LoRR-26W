# Exercise 0: exploring the default system

Instance: `random-example_400.json` (map `random-64-64-10`, 400 robots, `numTasksReveal` 1.5,
`agentCounter` 3), 1000 ticks, default time limits (`-a 100`, `-t 1000`).

## Step 1: default system vs. naive Python scheduler

| Scheduler | Completed tasks | Schedule errors | Entry timeouts | Wall time |
| --- | ---: | ---: | ---: | ---: |
| C++ default (greedy) | 695 | 0 | 0 | 87 s |
| Python naive (`--schedulerPython true`) | 417 | 0 | 0 | 86 s |

The lecture slides report 694 (greedy) and 427 (naive) for the same setting, so the setup reproduces
the reference numbers up to run-to-run noise.

## Step 2: PlanViz observations

_Open._ Where do robots wait, and where does traffic jam?

## Steps 3 and 4: `numTasksReveal` and `agentCounter`

_Open._ Generate the instance variants and run them:

```bash
python3 experiments/ex0/make_variants.py
bash experiments/ex0/run.sh
```

| Variant | Completed tasks |
| --- | ---: |
| `numTasksReveal` 1.0 | |
| `numTasksReveal` 1.5 | |
| `numTasksReveal` 3.0 | |
| `agentCounter` 1 | |
| `agentCounter` 3 | |
| `agentCounter` 10 | |
