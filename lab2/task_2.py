import os
import sys
import copy
import cProfile
import pstats
import time
from collections import defaultdict

global G, edge_count


class Graph:
    def __init__(self):
        self.v_count = 0
        self.edges = []
        self.vertices = set()

    def add_edge(self, u, w):
        self.edges.append((u, w))
        # self.edges[w].append(u)
        self.v_count = max([u, w, self.v_count])
        self.vertices.add(u)
        self.vertices.add(w)


def check(vert_arr: tuple):
    global G, edge_count
    check_edge = 0
    vert_arr = set(vert_arr)

    for i in G.edges:
        if i[0] in vert_arr or i[1] in vert_arr:
            check_edge += 1

    if check_edge >= edge_count:
        return True

    return False


def process_combination(a: list, n: int, k: int):
    if k == 0:
        print(a)
    else:
        # print(k-1, n)
        for i in range(k - 1, n):
            # print(f'i = {i}')
            a[k - 1] = i
            process_combination(a, i - 1, k - 1)


def combinations(iterable, r):
    pool = tuple(iterable)
    n = len(pool)
    if r > n:
        return
    indices = list(range(r))
    yield tuple(pool[i] for i in indices)
    while True:
        for i in reversed(range(r)):
            if indices[i] != i + n - r:
                break
        else:
            return
        indices[i] += 1
        for j in range(i + 1, r):
            indices[j] = indices[j - 1] + 1
        yield tuple(pool[i] for i in indices)


def process(vert_list: list) -> tuple:
    max_v, min_v = len(vert_list), 1
    k = max_v // 2
    res = ()
    while True:
        print(max_v, min_v)
        if max_v - min_v == 1:
            break

        # time.sleep(1)
        c = False
        print(k)
        for item in combinations(vert_list, k):
            if check(item):
                print(f'for k = {k} found solution')
                print(f'item - {item}\n')
                max_v = k
                k = (max_v + min_v) // 2
                c = True
                res = item
                break
            # else:
            #     print(0)

        if not c:
            print(f'for k = {k}  not found\n')
            min_v = k
            k = (max_v + min_v) // 2

    return res


def main(*args):
    global G, edge_count

    G = Graph()

    with open(args[0], 'r') as f:
        v_count, edge_count = map(int, f.readline().strip().split())

        for _ in range(edge_count):
            G.add_edge(*map(int, f.readline().strip().split()))

    vertices = list(G.vertices)

    print(G.edges)
    print(vertices)
    with cProfile.Profile() as pr:
        vertex_cover = process(vertices)
    pr.dump_stats('output.prof')

    with open(args[3], 'w') as stream:
        stats = pstats.Stats('output.prof', stream=stream)
        stats.sort_stats('cumtime')
        stats.print_stats()
    os.remove('output.prof')

    with open(args[1], 'w') as f:
        f.write(' '.join([*map(str, vertex_cover)]))

    with open(args[2], 'w') as f:
        f.write(str(len(vertex_cover)))

    return 0


if __name__ == '__main__':
    main(*sys.argv[1:])
