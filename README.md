# LoRR-26W

Course project for **Advanced Topics of Artificial Intelligence** (winter semester 2026/27),
Assignment 1: multi-agent planning on the [League of Robot Runners](https://www.leagueofrobotrunners.org/)
simulator. Hundreds of robots on a grid map complete tasks that appear over time; the goal is to
complete as many tasks as possible.

| Exercise | What | Our code |
| --- | --- | --- |
| 1 | Better task scheduler than the naive baseline | `Start-Kit/python/user_scheduler/` |
| 2 | Better executor under random delays | `Start-Kit/python/user_executor/` |

## Layout

```text
Start-Kit/     LoRR Start-Kit v3.1.0, vendored; only python/user_scheduler and python/user_executor are ours
PlanViz/       LoRR visualiser (submodule, unmodified)
tools/         PlanViz launcher, WSL shortcut
RunOutput/     simulator outputs (not committed)
```

The first commit is upstream Start-Kit
[`v3.1.0`](https://github.com/MAPF-Competition/Start-Kit/tree/9bc75d9dd9883de049294ab2981bf325bbe19d49)
unchanged, so diffs against it show exactly our changes.

## Build and run

Linux or WSL (Ubuntu 24.04) with CMake, Boost and pybind11 ≥ 3.0.1. Clone with submodules:

```bash
git clone --recurse-submodules https://github.com/alexschnabl/LoRR-26W.git
```

Run everything from `Start-Kit/`, because the Python scheduler and executor are imported relative to
the working directory:

```bash
cd Start-Kit
cmake -B build ./ -DCMAKE_BUILD_TYPE=Release && make -C build -j"$(nproc)"

./build/lifelong -i example_problems/random.domain/random-example_400.json -o ../RunOutput/out.json -s 1000
./build/lifelong ... --schedulerPython true --executorPython true   # use our Python code

python3 ../tools/planviz_launch.py --map example_problems/random.domain/maps/random-64-64-10.map --plan ../RunOutput/out.json
```

`tools/planviz_launch.py` runs PlanViz but keeps its window on one monitor (WSLg reports all
monitors as one screen). It needs PlanViz's `requirements.txt` installed.

`-c 3` writes only summary statistics, `-d 2` hides info logs, `-s 200` is a quick smoke test.
A run takes about `ticks × 100 ms`, so run experiments in parallel.

## License

MIT, see [LICENSE](LICENSE). Start-Kit and PlanViz are © The League of Robot Runners, also MIT.
