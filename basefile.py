from config import *

graph = {}


def generate_dag():
    nodes = 0
    edges = []
    height = MIN_HEIGHT + randint(1, 20) % (MAX_HEIGHT - MIN_HEIGHT + 1)
    for i in range(height):
        children = MIN_WIDTH + randint(1, 20) % (MAX_WIDTH - MIN_WIDTH + 1)
        for j in range(nodes):
            for k in range(children):
                if randint(1, 200) % 100 < PERCENT:
                    edges.append((j, k + nodes))
        nodes += children
    return edges, nodes


def initialize_infra():
    global graph
    num_tasks = 0
    min_arrival = 16
    for i in range(APPS):
        edges, num = generate_dag()
        arrival_time = randint(1, 100) % 15
        min_arrival = min(arrival_time, min_arrival)
        arrivals[i] = arrival_time
        for j in range(num):
            tasks[num_tasks + j] = Task(i)
        for edge in edges:
            from_node = edge[0] + num_tasks
            to_node = edge[1] + num_tasks
            tasks[to_node].increase_indegree()
            if from_node not in graph.keys():
                graph[from_node] = [to_node]
            else:
                tmp_nodes = list(graph[from_node])
                tmp_nodes.append(to_node)
                graph[from_node] = tmp_nodes
        num_tasks += num
    return num_tasks, min_arrival


def assign_clouds(num_tasks):
    etc_matrix = [[2 + randint(1, 100) % 16 for i in range(CLOUDS)] for j in range(num_tasks)]
    VMs = [[] for i in range(CLOUDS)]
    for i in range(num_tasks):
        top_two = sorted(range(CLOUDS), key=lambda i: etc_matrix[i])[:2]
        if etc_matrix[i][top_two[1]] - etc_matrix[i][top_two[0]] > DIFF:
            VMs[top_two[0]].append(i)
            tasks[i].set_burst(etc_matrix[i][top_two[0]])
        else:
            tasks[i].set_burst(etc_matrix[i][top_two[1]])
            VMs[top_two[1]].append(i)
    return VMs


def schedule(min_arrival, VMs):
    print(min_arrival, 'scheduler')
    while True:
        for i in range(CLOUDS):
            print('tmp')


def __main__():
    total_tasks, start_time = initialize_infra()
    VMs = assign_clouds(total_tasks)
    if start_time > 0:
        print('All clouds are empty until ' + str(start_time - 1))
    schedule(start_time, VMs)


__main__()
