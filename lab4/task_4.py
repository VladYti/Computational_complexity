import cProfile
import copy
import itertools
import math
import os
import pstats
import sys
import queue
from collections import defaultdict



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
    edges = []
    with open(args[0], 'r', encoding="utf-8") as file:
        n, m, = map(int, file.readline().strip().split())
        for i in range(m):
            edges.append(tuple(map(int, file.readline().strip().split())))
    my_graph = Graph(edges)

    with cProfile.Profile() as pr2:
        res = process_bd(n, my_graph)
    pr2.dump_stats('output.prof')

    with open('prof.txt', 'a', encoding="utf-8") as stream:
        stream.write('Profile for process_bd\n\n')
        stats = pstats.Stats('output.prof', stream=stream)
        stats.sort_stats('cumtime')
        stats.print_stats()
        stream.write('*' * 75 + '\n\n')
    os.remove('output.prof')

    with open('result.txt', 'a', encoding="utf-8") as file:
        file.write('solution by b_and_b\n')
        file.write(' '.join([*map(str, res)]) + '\n')
        res.append(res[0])
        file.write(str(sum([my_graph.get_weight(x, y) for x, y in pairwise(res)])))
        file.write('\n' + '*' * 10 + '\n\n')

    return 0


if __name__ == '__main__':
    main(*sys.argv[1:])
