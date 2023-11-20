""" task3 """

import cProfile
import copy
import itertools
import math
import os
import pstats
import sys
import queue
from collections import defaultdict

global graph
global vertices_count, best_bound
global edges_weights, m


class Graph:
    """
    almost standard Graph class
    """

    def __init__(self, edge_list):
        self.edges = defaultdict(dict)
        self.weights = set()
        for vertex_u, vertex_v, weight in edge_list:
            self.edges[vertex_u][vertex_v] = weight
            self.edges[vertex_v][vertex_u] = weight
            self.weights.add(weight)

    def get_weight(self, vertex_u, vertex_v):
        """
        :param vertex_u:
        :param vertex_v:
        :return:
        """
        return self.edges[vertex_u][vertex_v]

    def __repr__(self):
        return f'{self.__class__.__qualname__}({dict(self.edges)})'

    def __str__(self):
        return str(dict(self.edges))


def pairwise(iterable):
    """
    s -> (s0, s1), (s1, s2), (s2, s3), ...
    :param iterable:
    :return:
    """
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)


def process_permutations(arr: list, k: int):
    """
     this generator returns all permutation of input string
     """
    if k == 0:
        yield arr
    else:
        yield from process_permutations(arr, k - 1)
        for i in reversed(range(0, k)):
            arr[k], arr[i] = arr[i], arr[k]
            yield from process_permutations(arr, k - 1)
            arr[i], arr[k] = arr[k], arr[i]


def process_string(arr1: list, graph: Graph, k: int):
    """
    processing function for permutations

    :param arr1:
    :param arr2:
    :param k:
    :return:
    """
    if k == -1:
        yield arr1
    else:

        # for item in g.edges[j]:
        for i in graph.edges[k + 1].keys():
            arr1[k] = i
            yield from process_string(arr1, graph, k - 1)


def process_s(v_list: list, graph: Graph):
    """

    :param v_list:
    :param graph:
    :return:
    """
    permutation = process_string([1] * len(v_list), graph, len(v_list) - 1)
    max_w = math.inf
    solution = []

    for item in permutation:
        count_w = 0
        v_list = copy.copy(item)
        v_list.append(v_list[0])
        serv = False
        visited = set()

        for x, y in pairwise(v_list):
            if (y not in graph.edges[x].keys()) or (x in visited):
                # print(f'incorrect solution - {v_list}')
                serv = True
                break
            count_w += graph.edges[x][y]
            visited.add(x)
            # print(visited)
        if serv:
            continue
        if count_w <= max_w:
            max_w = count_w
            solution = v_list[:-1]

    return solution, max_w


def process_p(v_list: list, graph: Graph) -> (list, int):
    """

    :param v_list:
    :param graph:
    :return:
    """
    permutation = process_permutations(v_list, len(v_list) - 1)

    max_w = math.inf
    solution = []

    for item in permutation:

        count_w = 0
        v_list = copy.copy(item)
        v_list.append(v_list[0])
        serv = False

        for x, y in pairwise(v_list):
            if y not in graph.edges[x].keys():
                # print(f'incorrect solution - {v_list}')
                serv = True
                break
            count_w += graph.edges[x][y]
        if serv:
            continue
        if count_w <= max_w:
            max_w = count_w
            solution = v_list[:-1]

    return solution, max_w


def bound(arr: list, k):
    """

    :param arr:
    :param k:
    :return:
    """
    global graph, edges_weights, best_bound

    # отсекаем недопустимые решения
    if arr[-1] not in graph.edges[arr[-2]].keys():
        return False
    if len(arr) != len(set(arr)):
        return False

    # считаем оценку
    current_weights = [graph.edges[x][y] for x, y in pairwise(arr)]
    current_bound = sum(current_weights)
    current_bound += max(edges_weights - set(current_weights)) * (vertices_count - len(arr))

    if current_bound <= best_bound:
        # print(current_bound, best_bound)
        # best_bound = current_bound

        return True

    return False


def new_bound(arr: list):
    global graph, edges_weights, best_bound

    current_weights = [graph.edges[x][y] for x, y in pairwise(arr)]
    current_bound = sum(current_weights)
    if current_bound <= best_bound:
        best_bound = current_bound


def branch(arr: list, n: int):
    global m
    if len(arr) == n:
        new_bound(arr)
        # print(arr)
        yield arr
    else:
        for i in range(2, n + 1):
            arr.append(i)
            if bound(arr, i):  # оценка
                # print(arr)
                yield from branch(arr, n)
            arr.pop()


def process_b(n: int):
    res = []
    gen = branch([1], n)
    for item in gen:
        a = copy.copy(item)
        res.append(a)
    return res


def bd(arr: list, graph: Graph, n: int):
    if arr[-1] not in graph.edges[arr[-2]].keys():
        return False
    if len(arr) != len(set(arr)):
        return False

    current_weights = [graph.edges[x][y] for x, y in pairwise(arr)]
    current_bound = sum(current_weights)
    current_bound += min(graph.weights - set(current_weights)) * (n - len(arr))

    return current_bound


def put_in_queue(arr: list, pq: queue.PriorityQueue, n: int, graph: Graph):
    a = copy.copy(arr)
    for v in range(2, n + 1):
        a.append(v)
        cur_b = bd(a, graph, n)
        if cur_b:
            pq.put((cur_b, copy.copy(a)))

        a.pop()
    return pq


def process_bd(n: int, graph: Graph):
    record = math.inf
    rec_sol = 0
    pq = queue.PriorityQueue()

    a = [1]
    pq = put_in_queue(a, pq, n, graph)

    while not pq.empty():
        b = pq.get()
        if b[0] < record and len(b[1]) == n:
            record = b[0]
            rec_sol = b[1]

        if b[0] > record:
            b = pq.get()

        pq = put_in_queue(b[1], pq, n, graph)

    return rec_sol


def main(*args):
    """
    main function
    """
    global graph
    global vertices_count, best_bound
    global edges_weights, m

    edges_weights = set()
    edges = []

    with open(args[0], 'r', encoding="utf-8") as file:
        n, m, = map(int, file.readline().strip().split())
        for i in range(m):
            edges.append(tuple(map(int, file.readline().strip().split())))
            edges_weights.add(edges[i][2])

    my_graph = Graph(edges)
    graph = Graph(edges)
    vert_list = list(range(1, n + 1))

    vertices_count = n
    best_bound = math.inf

    # process_permutation call
    with cProfile.Profile() as pr1:
        solution, max_w = process_p(vert_list, my_graph)
    pr1.dump_stats('output.prof')

    with open('prof.txt', 'w', encoding="utf-8") as stream:
        stream.write('Profile for process_permutation\n\n')
        stats = pstats.Stats('output.prof', stream=stream)
        stats.sort_stats('cumtime')
        stats.print_stats()
        stream.write('*' * 75 + '\n\n')
    os.remove('output.prof')

    with open('result.txt', 'w', encoding="utf-8") as file:
        file.write('solution by process_permutation\n')
        file.write(' '.join([*map(str, solution)]) + '\n')
        file.write(str(max_w))
        file.write('\n' + '*' * 10 + '\n\n')
    # ******************

    # process_string call
    with cProfile.Profile() as pr2:
        solution, max_w = process_s(vert_list, my_graph)
    pr2.dump_stats('output.prof')

    with open('prof.txt', 'a', encoding="utf-8") as stream:
        stream.write('Profile for process_string\n\n')
        stats = pstats.Stats('output.prof', stream=stream)
        stats.sort_stats('cumtime')
        stats.print_stats()
        stream.write('*' * 75 + '\n\n')
    os.remove('output.prof')

    with open('result.txt', 'a', encoding="utf-8") as file:
        file.write('solution by process_string\n')
        file.write(' '.join([*map(str, solution)]) + '\n')
        file.write(str(max_w))
        file.write('\n' + '*' * 10 + '\n\n')

    # process branch_and_bound call
    with cProfile.Profile() as pr2:
        solution = process_b(n)
    pr2.dump_stats('output.prof')

    with open('prof.txt', 'a', encoding="utf-8") as stream:
        stream.write('Profile for process_b_and_b\n\n')
        stats = pstats.Stats('output.prof', stream=stream)
        stats.sort_stats('cumtime')
        stats.print_stats()
        stream.write('*' * 75 + '\n\n')
    os.remove('output.prof')

    with open('result.txt', 'a', encoding="utf-8") as file:
        file.write('solution by branch and bound\n')
        for item in solution:
            file.write(' '.join([*map(str, item)]) + '\n')
        file.write(str(max_w))
        file.write('\n' + '*' * 10 + '\n\n')
    # ******************

    # process branch_and_bound with  queue call
    with cProfile.Profile() as pr2:
        res = process_bd(n, my_graph)
    pr2.dump_stats('output.prof')

    with open('prof.txt', 'a', encoding="utf-8") as stream:
        stream.write('Profile for process_BD_with_queue\n\n')
        stats = pstats.Stats('output.prof', stream=stream)
        stats.sort_stats('cumtime')
        stats.print_stats()
        stream.write('*' * 75 + '\n\n')
    os.remove('output.prof')

    with open('result.txt', 'a', encoding="utf-8") as file:
        file.write('solution by branch and bound with queue\n')
        file.write(' '.join([*map(str, res)]) + '\n')
        res.append(res[0])
        file.write(str(sum([my_graph.get_weight(x, y) for x, y in pairwise(res)])))
        file.write('\n' + '*' * 10 + '\n\n')
    #*************

    return 0


if __name__ == '__main__':
    main(*sys.argv[1:])
