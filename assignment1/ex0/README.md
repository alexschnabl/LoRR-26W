# Exercise 0: explore the default system

Not graded. Default C++ scheduler, planner and executor on `random-example_400.json`
(`random-64-64-10`, 400 robots), 1000 ticks.

```bash
# 1. run with full output and open it in PlanViz
assignment1/run.sh -i Start-Kit/example_problems/random.domain/random-example_400.json \
    -o RunOutput/ex0.json -s 1000 -d 2
python3 tools/planviz_launch.py --map Start-Kit/example_problems/random.domain/maps/random-64-64-10.map \
    --plan RunOutput/ex0.json
```

For steps 3 and 4, copy the instance JSON **next to the original** (map/agent/task paths are relative
to the JSON file), change one field, and run it the same way with `-c 3`.

## Results

| Setting | Completed tasks |
| --- | ---: |
| Default (`numTasksReveal` 1.5, `agentCounter` 3) | 689–697 |
| `numTasksReveal` 1.0 | 544 |
| `numTasksReveal` 3.0 | 932 |
| `agentCounter` 1 | 1535 |
| `agentCounter` 10 | 181 |

No schedule errors or entry timeouts. The default setting was run five times; the spread comes from
the wall-clock time limits of the anytime planner. A larger task pool gives the greedy scheduler more
choice (shorter empty trips). `agentCounter` is the number of ticks per move, so lower means faster
robots, but throughput does not scale proportionally.

PlanViz observations (where robots wait, where traffic jams): _open_.
