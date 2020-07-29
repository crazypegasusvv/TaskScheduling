from random import randint

CLOUDS = 3 + randint(1, 100) % 7
APPS = 2 + randint(1, 100) % 3

MAX_HEIGHT = 5
MIN_HEIGHT = 2
MAX_WIDTH = 3
MIN_WIDTH = 1
PERCENT = 30

DIFF = 5

tasks = {}
APP_MODE = {}
modes = ['BE', 'AR']
arrivals = [0 for i in range(APPS)]
for i in range(APPS):
    APP_MODE[i] = modes[randint(1, 10) % 2]


class Task(object):
    def __init__(self, app):
        self.app = app
        self.burst = 0
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
