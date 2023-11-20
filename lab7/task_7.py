import itertools as it
import math
import os
import random
import sys
import copy
import cProfile
import pstats
from collections import defaultdict

global G, edge_count
global alpha


class Graph:
    def __init__(self):
        self.v_count = 0
        self.edges = defaultdict(list)
        self.serv_edges = []
        self.vertices = set()
        self.degrees = {}

    def add_edge(self, u, w):
        self.serv_edges.append((u, w))
        self.edges[u].append(w)
        self.edges[w].append(u)
        self.v_count = max([u, w, self.v_count])
        self.vertices.add(u)
        self.vertices.add(w)

    def add_degrees(self):
        for v in self.vertices:
            self.degrees[v] = len(self.edges[v])

    def __repr__(self):
        return f'{self.__class__.__qualname__}({dict(self.edges)})'

    def __str__(self):
        return str(dict(self.edges))


def pik_next(visited: set) -> int:
    global G
    allow_vertices = G.vertices - visited
    serv_d = {x: G.degrees[x] for x in allow_vertices}
    serv_d = dict(zip(serv_d.values(), serv_d.keys()))
    return serv_d[max(serv_d)]


def check(vert_arr: tuple) -> bool:
    global G, edge_count
    # check_edge = 0
    vert_arr = set(vert_arr)

    for i in G.serv_edges:
        if (i[0] not in vert_arr) and (i[1] not in vert_arr):
            return False

    # if check_edge == edge_count:
    #     return True

    return True


def find_simple_sol() -> list:
    sol = []
    visited = set()
    while True:
        next_vert = pik_next(visited)
        sol.append(next_vert)
        visited.add(next_vert)
        if check(tuple(sol)):
            break

    return sol


# def neighbour(current_v: list, count_v: int) -> list:
#     all_vertices = set(range(1, count_v + 1))
#     comb_two = it.combinations(current_v, 2)
#     for item in comb_two:
#         serv = set(item)
#         for v in it.combinations(all_vertices - serv, 2):
#             res = list(set(current_v) - serv)
#             yield res
#             yield res + [v[0]]
#             yield res + [v[0], v[1]]


def nn(current_v: list, count_v: int) -> list:
    for v in current_v:
        res = set(current_v) - {v}
        yield list(res)
        serv = set(range(1, count_v + 1)) - set(current_v)
        # for i in serv:
        #     yield list(res) + [i]
        for j in it.combinations(serv, 2):
            yield list(res) + [j[0], j[1]]


def check_random(p: float) -> bool:
    n = random.random()
    if p > n:
        return True
    else:
        return False


def simulated_ann(initial_sol: list, v_count: int, n: int, k, t):
    global alpha
    solution = copy.copy(initial_sol)

    for i in range(n):

        gen = nn(solution, v_count)
        # print(solution)
        for item in gen:
            if not check(item):
                continue
            else:
                if len(item) < len(solution):
                    solution = copy.copy(item)
                    t *= alpha
                    # print('change by len')
                    # print(len(solution))
                    break
                else:
                    p = math.exp(-(len(item) - len(solution)) / (k * t))

                    if check_random(p):
                        solution = copy.copy(item)
                        # print('change by p')
                        # print(len(solution))

                        t *= alpha
                        break
        if i % 100 == 0:
            print('*' * 10)
            print(f'it number - {i}')
            print(f'current len of solution - {len(solution)}')
            print('*' * 10, end='\n\n')

    return solution


def main(*args):
    global G, edge_count, alpha
    k = 1
    # T = 1000
    # N = 900

    G = Graph()

    with open(args[0], 'r') as f:
        v_count, edge_count = map(int, f.readline().strip().split())

        for _ in range(edge_count):
            G.add_edge(*map(int, f.readline().strip().split()))
    G.add_degrees()

    with open(args[1], 'r') as f:
        T = int(f.readline().strip())
        alpha = float(f.readline().strip())
        N = int(f.readline().strip())

    solution = find_simple_sol()

    with cProfile.Profile() as pr2:
        result = simulated_ann(solution, v_count, N, k, T)
    pr2.dump_stats('output.prof')

    with open('prof.txt', 'w', encoding="utf-8") as stream:
        stream.write('Profile for Simulated annealing\n\n')
        stats = pstats.Stats('output.prof', stream=stream)
        stats.sort_stats('cumtime')
        stats.print_stats()
        stream.write('*' * 75 + '\n\n')
    os.remove('output.prof')

    with open('vertex_cover.txt', 'w') as f:
        f.write(' '.join([*map(str, result)]))

    with open('cardinality_of_vc.txt', 'w') as f:
        f.write(str(len(result)))


if __name__ == '__main__':
    main(*sys.argv[1:])
