"""
greedy_manhattan.py — greedy scheduler with Manhattan distance.

Every free robot takes the free task with the smallest total distance
"""
import MAPF


class pyTaskScheduler:
    def __init__(self):
        self.env = None
        self.free_agents = set()
        self.free_tasks = set()

    def initialize(self, preprocess_time_limit: int):
        pass

    def calc_task_distance(self, curr_loc, task_id):
        total_dist = 0
        for trgt_loc in self.env.task_pool[task_id].locations:
            total_dist += self.manhattan_dist(curr_loc, trgt_loc)
            curr_loc = trgt_loc
        return total_dist

    def manhattan_dist(self, curr_loc, trgt_loc):
        # dist = difference in rows + difference in columns
        cols = self.env.cols
        row_diff = abs(curr_loc // cols - trgt_loc // cols)
        col_diff = abs(curr_loc % cols - trgt_loc % cols)
        return row_diff + col_diff

    def plan(self, time_limit: int) -> list:
        self.free_agents.update(self.env.new_freeagents)
        self.free_tasks.update(self.env.new_tasks)

        schedule = list(self.env.curr_task_schedule)
        assigned_agents = []

        for agent_id in sorted(self.free_agents):
            if not self.free_tasks:
                break

            agent_loc = self.env.curr_states[agent_id].location

            # pick the task with the lowest total distance
            task_id = min(self.free_tasks, key=lambda task: self.calc_task_distance(agent_loc, task))

            schedule[agent_id] = task_id
            assigned_agents.append(agent_id)
            self.free_tasks.discard(task_id)

        for assgn_agent in assigned_agents:
            self.free_agents.discard(assgn_agent)

        return schedule
