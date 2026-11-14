# Exercise 1: scheduler

Beat the naive scheduler.

```bash
assignment1/run.sh --scheduler ex1/hungarian -i Start-Kit/example_problems/random.domain/random-example_400.json -s 1000 -c 3
```

| Scheduler | Completed tasks |
| --- | ---: |
| naive | 426 |
| greedy_manhattan | 686 |
| greedy_bfs | 679 |
| greedy_bfs_precompute | 693 |
| hungarian | 738 |
| C++ default | 697 |
