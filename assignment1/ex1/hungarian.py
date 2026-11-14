"""
hungarian.py — optimal assignment with the Hungarian method, true (BFS) distance computed in initialize.

All free robots and free tasks are assigned at once so that the total distance is minimal
"""
from collections import deque

from scipy.optimize import linear_sum_assignment

import MAPF


class pyTaskScheduler:
    def __init__(self):
        self.env = None
        self.free_agents = set()
        self.free_tasks = set()
        self.dist_cache = {}
        self.nbrs = []

    def initialize(self, preprocess_time_limit: int):
        size = self.env.rows * self.env.cols
        self.nbrs = [self.neighbours(cell) for cell in range(size)]

        for cell in range(size):
            if self.env.map[cell] == 0:
                self.dist_cache[cell] = self.bfs_dist(cell)

    def calc_task_distance(self, curr_loc, task_id):
        total_dist = 0
        for trgt_loc in self.env.task_pool[task_id].locations:
            total_dist += self.true_dist(curr_loc, trgt_loc)
            curr_loc = trgt_loc
        return total_dist

    def true_dist(self, curr_loc, trgt_loc):
        # one BFS per target location, computed the first time it is needed
        if trgt_loc not in self.dist_cache:
            self.dist_cache[trgt_loc] = self.bfs_dist(trgt_loc)
        return self.dist_cache[trgt_loc][curr_loc]

    def neighbours(self, curr_loc):
        cols = self.env.cols
        size = self.env.rows * cols
        neighbours = []

        up = curr_loc - cols
        down = curr_loc + cols
        right = curr_loc + 1
        left = curr_loc - 1

        # not in the first row
        if curr_loc >= cols and self.env.map[up] == 0:
            neighbours.append(up)

        # not in the last row
        if down < size and self.env.map[down] == 0:
            neighbours.append(down)

        # not in the last column
        if curr_loc % cols != cols - 1 and self.env.map[right] == 0:
            neighbours.append(right)

        # not in the first column
        if curr_loc % cols != 0 and self.env.map[left] == 0:
            neighbours.append(left)

        return neighbours

    def bfs_dist(self, start_loc):
        dists = [-1] * (self.env.rows * self.env.cols)  # -1 = not reached yet
        dists[start_loc] = 0

        queue = deque([start_loc])
        while queue:
            curr_loc = queue.popleft()
            for nbr in self.nbrs[curr_loc]:
                if dists[nbr] == -1:
                    dists[nbr] = dists[curr_loc] + 1
                    queue.append(nbr)

        return dists

    def plan(self, time_limit: int) -> list:
        self.free_agents.update(self.env.new_freeagents)
        self.free_tasks.update(self.env.new_tasks)

        schedule = list(self.env.curr_task_schedule)
        if not self.free_agents or not self.free_tasks:
            return schedule

        agents = sorted(self.free_agents)
        tasks = list(self.free_tasks)

        # cost[i][j] = total distance of agent i doing task j
        cost = []
        for agent_id in agents:
            agent_loc = self.env.curr_states[agent_id].location
            cost.append([self.calc_task_distance(agent_loc, task) for task in tasks])

        rows, cols = linear_sum_assignment(cost)

        for i, j in zip(rows, cols):
            schedule[agents[i]] = tasks[j]
            self.free_agents.discard(agents[i])
            self.free_tasks.discard(tasks[j])

        return schedule
