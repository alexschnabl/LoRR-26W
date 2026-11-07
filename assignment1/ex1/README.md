# Exercise 1: better task scheduler

Goal: a Python scheduler that completes more tasks than the naive one, with valid schedules only.
Default C++ planner and executor stay unchanged. Each scheduler is one file here defining
`class pyTaskScheduler`; [`naive.py`](naive.py) is the shipped baseline (each free robot takes the
lowest open task id, ignoring distance).

```bash
assignment1/run.sh --scheduler ex1/naive \
    -i Start-Kit/example_problems/random.domain/random-example_400.json \
    -o RunOutput/ex1/naive.json -s 1000 -c 3 -d 2
```

## Results

`random-example_400` (`random-64-64-10`, 400 robots, `numTasksReveal` 1.5), 1000 ticks, single run.

| Scheduler | Completed tasks | Schedule errors | Entry timeouts |
| --- | ---: | ---: | ---: |
| `naive` (baseline) | 426 | 0 | 0 |
| C++ default (greedy, reference) | 697 | 0 | 0 |

The lecture slides report 427 (naive) and 694 (greedy) for the same setting.
