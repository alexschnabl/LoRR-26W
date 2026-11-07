# LoRR-26W

Course project for **Advanced Topics of Artificial Intelligence** (winter semester 2026/27).
Assignment 1 is multi-agent planning on the [League of Robot Runners](https://www.leagueofrobotrunners.org/)
simulator: hundreds of robots on a grid map complete tasks that appear over time, and the goal is to
complete as many tasks as possible.

## Layout

```text
assignment1/   our schedulers (ex1/), executors (ex2/), results per exercise, run.sh
Start-Kit/     LoRR Start-Kit v3.1.0, vendored; only the two loader files in python/user_* are changed
PlanViz/       LoRR visualiser (submodule, unmodified)
tools/         PlanViz launcher, WSL shortcut
RunOutput/     simulator outputs (not committed)
```

The first commit is upstream Start-Kit
[`v3.1.0`](https://github.com/MAPF-Competition/Start-Kit/tree/9bc75d9dd9883de049294ab2981bf325bbe19d49)
unchanged, so diffs against it show exactly our changes. See [assignment1/](assignment1/) for how our
code is loaded and run.

## Setup

Linux or WSL (Ubuntu 24.04) with CMake, Boost and pybind11 ≥ 3.0.1.

```bash
git clone --recurse-submodules https://github.com/alexschnabl/LoRR-26W.git
cd LoRR-26W
assignment1/run.sh --scheduler ex1/naive -i Start-Kit/example_problems/random.domain/random-example_400.json -s 200
```

`run.sh` builds the Start-Kit on first use. To visualise a run (full output, i.e. without `-c 3`):

```bash
python3 tools/planviz_launch.py --map <file.map> --plan RunOutput/<output.json>
```

The launcher keeps the PlanViz window on one monitor (WSLg reports all monitors as one screen) and
needs PlanViz's `requirements.txt` installed.

## License

MIT, see [LICENSE](LICENSE). Start-Kit and PlanViz are © The League of Robot Runners, also MIT.
