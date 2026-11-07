# Task Scheduling and Robust Execution for the League of Robot Runners

[![LoRR Start-Kit](https://img.shields.io/badge/LoRR%20Start--Kit-v3.1.0-1f6feb)](https://github.com/MAPF-Competition/Start-Kit)
![C++17](https://img.shields.io/badge/C%2B%2B-17-00599C?logo=cplusplus&logoColor=white)
![Python](https://img.shields.io/badge/python-3.12-3776AB?logo=python&logoColor=white)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Course project for **Advanced Topics of Artificial Intelligence**, winter semester 2026/27,
Assignment 1 (multi-agent planning).

We work on the [League of Robot Runners (LoRR)](https://www.leagueofrobotrunners.org/) simulator, a
lifelong multi-agent path finding (MAPF) benchmark modelled after robot fleets in fulfilment and
sortation centres. Hundreds of robots move on a grid map; tasks with one or more errands appear over
time and the system has to decide continuously

| Question | Component | Our work |
| --- | --- | --- |
| Which robot does which task? | **Task scheduler** | Exercise 1: replace the naive Python scheduler |
| Which collision-free routes do the robots take? | Planner (MAPF) | Default C++ planner, unchanged |
| What happens when a robot is delayed? | **Executor** | Exercise 2: replace the naive Python executor |

Throughput (number of completed tasks within the simulation horizon) is the main objective.

## Exercises

### Exercise 0: explore the default system (not graded)

Build the Start-Kit, run `random-example_400.json` (400 robots on `random-64-64-10`) for 1000 ticks,
inspect the result in PlanViz (where do robots wait, where does traffic jam), and observe the effect of
`numTasksReveal` (1.0 / 1.5 / 3.0) and `agentCounter` (1 / 3 / 10) on the number of completed tasks.
Scripts are in [`experiments/ex0/`](experiments/ex0), findings in [`docs/exercise-0.md`](docs/exercise-0.md).

### Exercise 1: a better task scheduler

`Start-Kit/python/user_scheduler/pyTaskScheduler.py`, run with `--schedulerPython true`.
The naive baseline gives each free robot the lowest-numbered open task, regardless of distance.
Our scheduler must complete more tasks while producing only valid schedules, and it shares its time
budget with the planner. Directions to explore: optimal assignment (Hungarian method) and auctions,
exact grid distances instead of Manhattan estimates, reassigning tasks whose first errand has not been
reached, congestion-aware costs, and planning task sequences per robot.

### Exercise 2: a robust executor

`Start-Kit/python/user_executor/pyExecutor.py`, run with `--executorPython true`.
Robots are delayed at random (`delayConfig` in the instance file); the executor decides which staged
actions each robot executes (GO / STOP). The naive baseline decides at random. Staged actions must
always remain a prefix of the previously staged actions plus the new plan.

### Evaluation

Four configurations (naive baselines, own scheduler, own executor, both), at least five runs per setting
with different `delayConfig.seed` values, reported as mean and spread. Factors include the map domain
(at least three), team size (100 / 200 / 400), `numTasksReveal`, `agentCounter`, delay probability and
the planning time limit `-t` (500 / 1000 / 2000 ms). Metrics: completed tasks, runtime per call,
schedule errors and entry timeouts.

## Repository layout

```text
.
├── Start-Kit/          LoRR Start-Kit v3.1.0 (vendored, see below); our code lives in
│   ├── python/user_scheduler/   Exercise 1
│   └── python/user_executor/    Exercise 2
├── PlanViz/            LoRR visualiser (git submodule, unmodified)
├── experiments/        instance variants and run scripts per exercise
├── docs/               environment setup and findings
├── tools/              WSL setup script and PlanViz launcher
├── RunOutput/          simulator outputs (not committed)
└── start-wsl.bat       opens a WSL shell in Start-Kit/ (Windows)
```

The Start-Kit is vendored rather than linked as a submodule because the simulator loads the user
scheduler and executor from fixed paths inside it. The first commit imports upstream
[`9bc75d9`](https://github.com/MAPF-Competition/Start-Kit/commit/9bc75d9dd9883de049294ab2981bf325bbe19d49)
(tag `v3.1.0`) unchanged, so `git diff <first commit> -- Start-Kit` shows exactly what we changed.
For the graded work only `python/user_scheduler/` and `python/user_executor/` may change.

## Getting started

The Start-Kit targets Linux. On Windows we use WSL with Ubuntu 24.04; the full environment notes are in
[`docs/setup.md`](docs/setup.md).

```bash
git clone --recurse-submodules https://github.com/alexschnabl/LoRR-26W.git
cd LoRR-26W
sudo bash tools/setup_wsl.sh      # compilers, Boost, pybind11 >= 3.0.1, PlanViz venv + `planviz` command
```

Build and run (inside WSL, from `Start-Kit/`, because the Python modules are imported relative to the
working directory):

```bash
cd Start-Kit
cmake -B build ./ -DCMAKE_BUILD_TYPE=Release && make -C build -j"$(nproc)"

# default C++ system, 1000 ticks
./build/lifelong -i example_problems/random.domain/random-example_400.json -o ../RunOutput/random400.json -s 1000

# our Python scheduler and/or executor
./build/lifelong -i example_problems/random.domain/random-example_400.json -o ../RunOutput/random400_py.json -s 1000 \
    --schedulerPython true --executorPython true

# visualise a full output (-c 1, the default)
planviz --map example_problems/random.domain/maps/random-64-64-10.map --plan ../RunOutput/random400.json
```

Useful flags: `-c 3` writes only summary statistics, `-d 2` shows only warnings, `-l run.log` redirects
the log, and `-s 200` gives a quick ~20 s smoke test. A run takes roughly `ticks × 100 ms` of wall time
because the simulator runs in real time; see [`docs/setup.md`](docs/setup.md#run-time) for details.

Exercise 0 sweeps:

```bash
python3 experiments/ex0/make_variants.py   # writes experiments/ex0/instances/*.json
bash experiments/ex0/run.sh                # runs them in parallel, prints a summary table
```

## References

- H. Ma, J. Li, T. K. S. Kumar, S. Koenig. [Lifelong Multi-Agent Path Finding for Online Pickup and Delivery Tasks](https://arxiv.org/abs/1705.10868). AAMAS, 2017.
- J. Li, A. Tinka, S. Kiesel, J. W. Durham, T. K. S. Kumar, S. Koenig. [Lifelong Multi-Agent Path Finding in Large-Scale Warehouses](https://arxiv.org/abs/2005.07371). AAAI, 2021.
- S.-H. Chan et al. [The League of Robot Runners: Competition Goals, Designs, and Implementation](https://shchan13.github.io/publications/ChanICAPS24). ICAPS System Demonstrations, 2024.
- H. W. Kuhn. The Hungarian method for the assignment problem. *Naval Research Logistics Quarterly* 2(1–2), 1955.
- K. Okumura, M. Machida, X. Défago, Y. Tamura. [Priority Inheritance with Backtracking for Iterative Multi-agent Path Finding](https://arxiv.org/abs/1901.11282). IJCAI, 2019.
- H. Ma, T. K. S. Kumar, S. Koenig. [Multi-Agent Path Finding with Delay Probabilities](https://arxiv.org/abs/1612.05309). AAAI, 2017.
- W. Hönig, S. Kiesel, A. Tinka, J. W. Durham, N. Ayanian. [Persistent and Robust Execution of MAPF Schedules in Warehouses](https://act.usc.edu/publications/Hoenig_RAL2019.pdf). *IEEE Robotics and Automation Letters* 4(2), 2019.

## License

Our code is released under the [MIT License](LICENSE). The vendored Start-Kit and the PlanViz submodule are
© The League of Robot Runners, also under the MIT License (see `Start-Kit/LICENSE` and `PlanViz/LICENSE`).
