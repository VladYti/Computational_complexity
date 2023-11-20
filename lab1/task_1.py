import os
import sys
import copy
import cProfile
import pstats

# define global variables
global capacity, vector_w, vector_p
global record, opt_s


def process(a: list):
    global capacity, vector_w, vector_p
    global record, opt_s

    service_1 = sum(vector_w[i] if a[i] == 1 else 0 for i in range(len(a)))
    if service_1 <= capacity:

        service_2 = sum(vector_p[i] if a[i] == 1 else 0 for i in range(len(a)))
        if service_2 > record:
            opt_s = copy.copy(a)
            record = service_2
    pass


def binary_process(a: list, k: int):
    if k == -1:
        process(a)
        return
    else:
        a[k] = 0
        binary_process(a, k - 1)

        a[k] = 1
        binary_process(a, k - 1)
    pass


def main(*args):
    global capacity, vector_w, vector_p
    global record, opt_s

    print(args)

    try:
        with open(args[0], 'r') as f:
            capacity = float(f.readline())
        print(capacity)

        with open(args[1], 'r') as f:
            vector_w = list(map(float, f.readlines()))

        with open(args[2], 'r') as f:
            vector_p = list(map(float, f.readlines()))

    except IndexError:
        print('required file names not found')

    record = 0
    opt_s = []
    a = [0] * len(vector_p)

    with cProfile.Profile() as pr:
        binary_process(a, len(a) - 1)
    pr.dump_stats('output.prof')

    try:
        with open(args[3], 'w') as stream:
            stats = pstats.Stats('output.prof', stream=stream)
            stats.sort_stats('cumtime')
            stats.print_stats()
        os.remove('output.prof')

        with open(args[4], 'a') as f:
            for item in opt_s:
                f.write(str(item) + '\n')

        with open(args[5], 'a') as f:
            f.write(str(record) + '\n')

    except IndexError:
        print('required file names not found')

    return 0


if __name__ == '__main__':
    main(*sys.argv[1:])
