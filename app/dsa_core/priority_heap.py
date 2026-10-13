# DSA ALGORITHM: Min-Heap / Priority Queue
# USED FOR: Urgency-based task scheduling (Irrigation, Spraying, Fertilization).

import heapq

class TaskPriorityQueue:
    def __init__(self):
        self.heap = []
        self.task_counter = 0

    def push_task(self, days_due, title, category):
        """DSA: Heap Push - O(log N)"""
        self.task_counter += 1
        heapq.heappush(self.heap, (days_due, self.task_counter, {"title": title, "category": category, "days": days_due}))

    def pop_task(self):
        """DSA: Heap Pop - O(log N) - extracts highest urgency task."""
        if self.heap:
            return heapq.heappop(self.heap)[2]
        return None

    def get_all_sorted(self):
        """DSA: Returns tasks sorted by urgency key."""
        sorted_tasks = []
        temp_heap = list(self.heap)
        while temp_heap:
            sorted_tasks.append(heapq.heappop(temp_heap)[2])
        return sorted_tasks
