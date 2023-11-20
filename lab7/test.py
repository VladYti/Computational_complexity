import itertools as it
import math


# def neighbour(current_v: list, count_v: int) -> list:
#     all_vertices = set(range(1, count_v+1))
#     comb_two = it.combinations(current_v, 2)
#     for item in comb_two:
#         serv = set(item)
#         for v in all_vertices-serv:
#             yield list(set(current_v)-serv)+[v]

def neighbour(current_v: list, count_v: int) -> list:
    all_vertices = set(range(1, count_v + 1))
    comb_two = it.combinations(current_v, 2)
    for item in comb_two:
        serv = set(item)
        for v in it.combinations((all_vertices - set(current_v)).union(serv), 3):
            res = list(set(current_v) - serv)
            yield res + [v[2]]


def nn(current_v: list, count_v: int) -> list:
    for v in current_v:
        res = set(current_v)-{v}
        yield list(res)
        serv = set(range(1, count_v+1))-set(current_v)
        for i in serv:
            yield list(res) + [i]
        for j in it.combinations(serv, 2):
            yield list(res) + [j[0], j[1]]

def main():
    print(math.exp(-1/0.0099))
    #
    # gen = (x for l in range(len(a)-1, len(a)+2) for x in it.combinations((set(range(1, 13)) - set(a)).union({3,5}), l))
    # for i in gen:
    #     print(i)

    # gen = nn(a, v)
    # for item in gen:
    #     print(item)

if __name__ == '__main__':
    main()
