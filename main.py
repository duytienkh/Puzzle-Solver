from pysat.solvers import Glucose3
import numpy as np

def readFile(filename):
    f = open(filename, 'r')

    _, _ = [int(x) for x in next(f).split()]
    mat = []
    for line in f:
        array = []
        for x in line.split():
            if x != '.':
                array.append(int(x))
            else:
                array.append(-1)
        mat.append(array)
    return mat

def comb(arr, k):
    res = []
    stack = [0]
    pos = 1
    n = len(arr)

    while len(stack) > 0:
        if pos == k:
            res.append([arr[i] for i in stack])
            pos -= 1
        if pos < len(stack):
            if stack[pos] < n - 1:
                stack[pos] += 1
                pos += 1
            else:
                pos -= 1
                stack.pop(-1)
        else:
            if stack[pos - 1] < n - 1:
                stack.append(stack[pos - 1] + 1)
                pos += 1
            else:
                pos -= 2
                stack.pop(-1)

    return res

def adjGet(i, j, row, col):
    cnt = 1
    arr = [i * col + j]
    if i - 1 >= 0 and j - 1 >= 0:
        cnt += 1
        arr.append((i - 1) * col + j - 1)
    if i - 1 >= 0:
        cnt += 1
        arr.append((i - 1) * col + j)
    if i - 1 >= 0 and j + 1 < col:
        cnt += 1
        arr.append((i - 1) * col + j + 1)
    if j - 1 >= 0:
        cnt += 1
        arr.append(i * col + j - 1)
    if j + 1 < col:
        cnt += 1
        arr.append(i * col + j + 1)
    if i + 1 < row and j - 1 >= 0:
        cnt += 1
        arr.append((i + 1) * col + j - 1)
    if i + 1 < row:
        cnt += 1
        arr.append((i + 1) * col + j)
    if i + 1 < row and j + 1 < col:
        cnt += 1
        arr.append((i + 1) * col + j + 1)
    return cnt, [x + 1 for x in arr]

def solve(mat):
    g = Glucose3()

    row, col = len(mat), len(mat[0])

    for i in range(row):
        for j in range(col):
            if mat[i][j] != -1:
                adjCount, arr = adjGet(i, j, row, col)

                k = mat[i][j]
                com = comb([-x for x in arr], k + 1)
                for x in com:
                    g.add_clause(x)
                com = comb(arr, adjCount - k + 1)
                for x in com:
                    g.add_clause(x)
    g.solve()
    arr = g.get_model()

    return arr

def printColor(x, v):
    if x:
        print("\033[0;37;41m  ", end = '\033[0m')
    else:
        print("\033[0;37;42m  ", end = '\033[0m')

def printResult(res, mat):
    for i in range(len(mat)):
        for j in range(len(mat[0])):
            printColor(res[i * len(mat) + j] < 0, mat[i][j])
        print()

def main():
    mat = readFile('input.txt')

    result = solve(mat)

    printResult(result, mat)

if __name__ == "__main__":
    main()