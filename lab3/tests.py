import time


def process_string(arr1: list, arr2: list, k: int):
    if k == -1:
        yield arr1
    else:
        for i in range(len(arr1)):
            arr1[k] = arr2[i]
            yield from process_string(arr1, arr2, k - 1)


def process_permutations(arr: list, k: int):
    if k == -1:
        yield arr
    else:
        yield from process_permutations(arr, k - 1)
        for i in reversed(range(0, k)):
            print(f'sevr - {arr}')
            arr[k], arr[i] = arr[i], arr[k]
            yield from process_permutations(arr, k - 1)
            arr[i], arr[k] = arr[k], arr[i]


def check(i):
    if i%2 == 0 or i%3 == 0:
        return True
    else:
        return False


b = {1: (2, 3, 4), 2:(4, 5, 6), 3:(6, 5, 1), 4:(1, 2, 5), 5:(6, 4, 3), 6:(1, 2, 3)}



def ps(arr):
    if len(arr) == 4:
        print(arr)
    else:
        for i in b[arr[-1]]:
            if check(i):
                arr.append(i)
                ps(arr)
                arr.pop()
            else:
                continue


def branch(arr: list, n: int):
    if len(arr) == n:
        yield arr
    else:
        for i in range(2, n + 1):
            arr.append(i)
            yield from branch(arr, n)
            arr.pop()

def main():
    gen = branch([1], 5)
    for item in gen:
        print(item)
    return 0

if __name__ == '__main__':
    main()
# print()
# for item in it2:
#     print(item)
#
#
# print(b1==b2)

#
# a = '1234'
# count = 0
# for item in it.product(a, repeat=4):
#     print(''.join(item))
#     count += 1
# print(count)
