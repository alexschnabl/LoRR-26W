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

Default C++ system, 1000 ticks, one run per variant (`delayConfig.seed` 0), all six in parallel
(87 s wall time in total). Reproduce with:

```bash
python3 experiments/ex0/make_variants.py
bash experiments/ex0/run.sh
```

| Variant | Completed tasks | Relative to default |
| --- | ---: | ---: |
| `numTasksReveal` 1.0 | 544 | 0.79 |
| `numTasksReveal` 1.5 (default) | 693 | 1.00 |
| `numTasksReveal` 3.0 | 932 | 1.35 |
| `agentCounter` 1 | 1535 | 2.23 |
| `agentCounter` 3 (default) | 689 | 1.00 |
| `agentCounter` 10 | 181 | 0.26 |

No schedule errors, planner errors or entry timeouts in any run.

**`numTasksReveal`** sets the size of the open task pool to `numTasksReveal × teamSize`. A larger pool
gives the greedy scheduler more choice, so free robots find tasks closer to them and spend less time
driving empty. Doubling the pool from 1.5 to 3.0 adds 35% throughput without any change to the
algorithms. With 1.0 there are exactly as many open tasks as robots, so a free robot has to take
whatever is left, often far away. This is also why scheduling quality matters: the scheduler decides
how well that choice is used.

**`agentCounter`** is the number of execution ticks a robot needs for one forward or rotate action. In
1000 ticks a robot can make 1000, about 333 or 100 moves for `agentCounter` 1, 3 and 10. Throughput
follows that trend but not proportionally:

- From 3 to 1 (3× faster robots), completed tasks only grow 2.2×. Faster robots meet each other more
  often per planning call (the planner still runs every 10 ticks), so congestion and planning most
  likely limit the gain. PlanViz on an `agentCounter` 1 run would show whether waiting increases.
- From 3 to 10 (3.3× slower robots), completed tasks drop 3.8×, slightly more than the slowdown.
  A likely part of the gap: with fewer moves overall, the unfinished tasks at the end of the
  horizon are a larger share of the work done.

**Noise.** The default variants of both sweeps are the same instance and gave 693 and 689; together
with the two earlier runs (695, 691) this puts run-to-run noise at about ±3 tasks. It comes from the
wall-clock time limits of the anytime planner, so the same seed does not give identical results. For
the graded evaluation, use at least five runs per setting.
