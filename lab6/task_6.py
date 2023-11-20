import cProfile
import copy
import os
import pstats
import sys

import numpy as np


def dynamic_program(capacity: int, vector_w: list, vector_p: list) -> list:
    n = len(vector_w)
    m = int(sum(vector_p))

    a = np.zeros((n + 1, m + 1))
    p = np.zeros((n + 1, m + 1))
    a[0, 1:] = np.inf
    a[:, 0] = 0

    for i in range(1, n + 1):
        for r in range(1, m + 1):
            if vector_p[i - 1] <= r:
                if a[i - 1, r - vector_p[i - 1]] + vector_w[i - 1] < a[i - 1, r]:
                    a[i, r] = a[i - 1, r - vector_p[i - 1]] + vector_w[i - 1]
                    p[i, r] = 1
                else:
                    a[i, r] = a[i - 1, r]
                # a[i, r] = min(a[i - 1, r - vector_p[i - 1]] + vector_w[i - 1], a[i - 1, r])
            else:
                a[i, r] = a[i - 1, r]

    serv = np.where(a[n] <= capacity)[0][-1]
    res = []
    b = copy.copy(serv)
    print(b)
    for i in reversed(range(1, n + 1)):
        if p[i, b] == 1:
            res.append(i)
            b -= vector_p[i - 1]
        else:
            continue

    return res


def eval_t(eps: float, n: int, c_max: int) -> int:
    return np.floor(((eps / 2) * c_max) / n)


def main(*args):
    with open(args[0], 'r') as f:
        capacity = int(f.readline())
    # print(capacity)

    with open(args[1], 'r') as f:
        vector_w = list(map(int, f.readlines()))

    with open(args[2], 'r') as f:
        vector_p = list(map(int, f.readlines()))

    with open(args[3], 'r') as f:
        eps = float(f.readline().strip())

    # result1 = dynamic_program(capacity, vector_w, vector_p)
    # print(result1)

    print(vector_p)
    t2 = eval_t(eps, len(vector_p), max(vector_p))
    print(t2)
    new_vector_p = [int(np.floor(x / t2)) for x in vector_p]
    print(new_vector_p)

    with cProfile.Profile() as pr2:
        res = dynamic_program(capacity, vector_w, new_vector_p)
    pr2.dump_stats('output.prof')

    with open('prof.txt', 'w', encoding="utf-8") as stream:
        stream.write('Profile for process_bd\n\n')
        stats = pstats.Stats('output.prof', stream=stream)
        stats.sort_stats('cumtime')
        stats.print_stats()
        stream.write('*' * 75 + '\n\n')
    os.remove('output.prof')

    solution = np.zeros(len(vector_p), dtype=int)
    solution[[np.array(res) - 1]] = 1
    s = np.sum(np.array(vector_p)[np.array(res) - 1])

    with open('solution.txt', 'w') as f:
        for item in solution:
            f.write(str(item) + '\n')

    with open('value_of_solution.txt', 'w') as f:
        f.write(str(s) + '\n')

    return 0


if __name__ == '__main__':
    main(*sys.argv[1:])
