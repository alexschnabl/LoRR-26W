# Exercise 2: better executor

Goal: a Python executor that completes more tasks under delays than the naive one. Default C++
scheduler and planner stay unchanged. Staged actions must stay a prefix of the previously staged
actions plus the new plan. Each executor is one file here defining `class pyExecutor`;
[`naive.py`](naive.py) is the shipped baseline (stages the whole plan, sends random GO / STOP).

```bash
assignment1/run.sh --executor ex2/naive \
    -i Start-Kit/example_problems/random.domain/random-example_400.json \
    -o RunOutput/ex2/naive.json -s 1000 -c 3 -d 2
```

## Results

`random-example_400` (`random-64-64-10`, 400 robots, default delays `pDelay` 0.01), 1000 ticks,
single run.

| Executor | Completed tasks | Planner errors | Entry timeouts |
| --- | ---: | ---: | ---: |
| `naive` (baseline) | 0 | 182 | 0 |
| `naive` + naive scheduler | 0 | 191 | 0 |
| C++ default (reference) | 697 | 0 | 0 |

The naive executor completes no tasks; the unmodified upstream file gives the same result. The log
is full of robots trying to move into walls or off the map. Most likely the random STOPs let the
actual positions drift away from the positions the planner plans from, so the plans no longer fit.
