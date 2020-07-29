from random import randint

CLOUDS = 3 + randint(1, 100) % 4
APPS = 2 + randint(1, 100) % 5

MAX_HEIGHT = 5
MIN_HEIGHT = 2
MAX_WIDTH = 3
MIN_WIDTH = 1
PERCENT = 30

DIFF = 5

tasks = {}
APP_MODE = {}
arrivals = [0 for i in range(APPS)]
for i in range(APPS):
    APP_MODE[i] = randint(1, 10) % 2


class Task(object):
    def __init__(self, app):
        self.app = app
        self.burst = 0
        self.start = 0
        self.end = 0
        self.in_degree = 0

    def burst_time(self):
        return self.burst

    def set_burst(self, burst_time):
        self.burst = burst_time

    def app_num(self):
        return self.app

    def indegree(self):
        return self.in_degree

    def decrease_indegree(self):
        self.in_degree -= 1

    def increase_indegree(self):
        self.in_degree += 1

    def set_start(self, start):
        if self.start == 0:
            self.start = start

    def get_start(self):
        return self.start

    def set_end(self, end):
        self.end = end

    def get_end(self):
        return self.end
