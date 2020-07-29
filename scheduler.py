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


def schedule_cloud(vm, current, cloud_num):
    global graph
    vm.sort(key=lambda x: tasks[x].indegree())
    available = []
    for task_id in vm:
        if tasks[task_id].indegree() == 0 and arrivals[tasks[task_id].app_num()] <= current:
            available.append(task_id)
    if len(available) > 0:
        available.sort(key=lambda x: APP_MODE[tasks[x].app_num()], reverse=True)
        task_id = available[0]
        print('At t=' + str(current) + ' cloud ' + str(cloud_num) + ' runs ' + str(task_id))
        tasks[task_id].set_start(current)
        rem = tasks[task_id].burst_time()
        if rem == 1:
            tasks[task_id].set_end(current)
            if task_id in graph.keys():
                for node in graph[task_id]:
                    tasks[node].decrease_indegree()
            vm.remove(task_id)
        tasks[task_id].set_burst(rem - 1)
    return vm


def schedule(min_arrival, VMs):
    current_time = min_arrival
    all_scheduled = False
    while not all_scheduled:
        all_scheduled = True
        for i in range(CLOUDS):
            if len(VMs[i]) > 0:
                all_scheduled = False
                VMs[i] = schedule_cloud(VMs[i], current_time, i)
            else:
                all_scheduled = all_scheduled and True
        current_time += 1
    print('All tasks completed')


def __main__():
    total_tasks, start_time = initialize_infra()
    VMs = assign_clouds(total_tasks)
    if start_time > 0:
        print('All clouds are empty until ' + str(start_time - 1))
    schedule(start_time, VMs)


print('Total Clouds: ' + str(CLOUDS))
print('Total workflows: ' + str(APPS))

__main__()

for process in tasks.keys():
    print('Task ' + str(process) + ' belongs to workflow ' + str(tasks[process].app_num()))
    makespan = tasks[process].get_end() - tasks[process].get_start()
    print('Makespan for task=' + str(process) + ' is ' + str(makespan))
