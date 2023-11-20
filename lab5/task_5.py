import cProfile
import copy
import os
import pstats
import sys
from collections import defaultdict


class Graph:
    def __init__(self):

        self.edges_list = []
        self.edges_dict = defaultdict(set)
        self.degrees = defaultdict(list)

    def add_edge(self, u, w):

        self.edges_dict[w].add(u)
        self.edges_dict[u].add(w)
        # self.edges_list.append((u, w))

    def get_edge_list(self):
        edges = set()
        for key in self.edges_dict.keys():
            for item in self.edges_dict[key]:
                if (key, item) in edges or (item, key) in edges:
                    continue
                else:
                    edges.add((key, item))
        return list(edges)

    def add_degrees(self):
        for v in self.edges_dict.keys():
            self.degrees[len(self.edges_dict[v])].append(v)

    def delete_vertex(self, w):
        # self.edges_dict.pop(w, None)
        del self.edges_dict[w]
        for key in self.edges_dict.keys():
            self.edges_dict[key].discard(w)

        self.degrees = defaultdict(list)
        self.add_degrees()

    def __repr__(self):
        return f'{self.__class__.__qualname__}({dict(self.edges_dict)})'

    def __str__(self):
        return str(dict(self.edges_dict))

    def __deepcopy__(self, memo):
        # my_copy = type(self)()
        # memo[id(self)] = my_copy
        # my_copy.degrees = copy.deepcopy(self.degrees, memo)
        # my_copy.edges_dict = copy.deepcopy(self.edges_dict, memo)
        # my_copy.edges_list = copy.deepcopy(self.edges_list, memo)

        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, copy.deepcopy(v, memo))

        return result


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


def check(vert_arr: tuple, edge_list: list, edge_count: int) -> bool:
    check_edge = 0
    vert_arr = set(vert_arr)

    for i in edge_list:
        if i[0] in vert_arr or i[1] in vert_arr:
            check_edge += 1

    if check_edge >= edge_count:
        return True

    return False


def process(graph: Graph, k: int) -> tuple:
    vert_list = list(graph.edges_dict.keys())

    edge_list = graph.get_edge_list()
    edge_count = len(edge_list)

    res = ()

    for item in combinations(vert_list, k):
        if check(item, edge_list, edge_count):
            res = item
            break

    return res


def reduction(graph1: Graph, k: int):
    graph_copy = copy.deepcopy(graph1)
    graph_copy.add_degrees()
    vc = []

    while True:

        a = True
        b = True
        c = True

        degs = graph_copy.degrees.keys()
        for deg in degs:

            if deg == 0:
                for item in graph_copy.degrees[deg]:
                    graph_copy.delete_vertex(item)
                a = False
                break

            elif deg == 1:
                for item in graph_copy.degrees[deg]:
                    vc.append(list(graph_copy.edges_dict.get(item))[0])
                    graph_copy.delete_vertex(list(graph_copy.edges_dict.get(item))[0])
                b = False
                break

            elif deg > k:
                for item in graph_copy.degrees[deg]:
                    vc.append(item)
                    graph_copy.delete_vertex(item)
                c = False
                break

        if a and b and c:
            break

    return graph_copy, vc


def main(*args):
    g1 = Graph()
    with open(args[0], 'r') as f:
        v_count, edge_count = map(int, f.readline().strip().split())

        for _ in range(edge_count):
            g1.add_edge(*map(int, f.readline().strip().split()))

    k = int(args[1])

    with cProfile.Profile() as pr:
        g2, vc1 = reduction(g1, k)
        vc2 = process(g2, k - len(vc1))
    pr.dump_stats('output.prof')

    with open('prof.txt', 'w') as stream:
        stats = pstats.Stats('output.prof', stream=stream)
        stats.sort_stats('cumtime')
        stats.print_stats()
    os.remove('output.prof')

    for i in vc2:
        vc1.append(i)

    with open('vc.txt', 'w') as f:
        if len(vc1) == k:
            f.write(' '.join([*map(str, vc1)]))
        else:
            f.write('нет решения')

    with open('vc_count.txt', 'w') as f:
        if len(vc1) == k:
            f.write(f'{len(vc1)}')
        else:
            f.write('нет решения')

    return 0


if __name__ == '__main__':
    main(*sys.argv[1:])
