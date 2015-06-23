from math import ceil
from copy import deepcopy
import sys


sys.setrecursionlimit(200000)


def sequence_alignemt(x, y, g, a):
    """ Determines optimal sequence alignment for two strings (x and y) with\
        O(m.n) space and time complexity.
            Args:
                x   - First string
                y   - Second string
                g   - Gap penalty
                a   - Mismatch penalty
    """
    _x = "*%s" % x
    _y = "*%s" % y
    m = len(_x)  # Number of characters in x
    n = len(_y)  # Number of characters in y
    M = [[0 for i in range(n)] for j in range(m)]

    # Fills the first line of the matrix
    for i in range(m):
        M[i][0] = i*g
    # Fills the first column of the matrix
    for j in range(n):
        M[0][j] = j*g

    for i in range(1, m):
        for j in range(1, n):
            _a = 0 if _x[i] == _y[j] else a
            M[i][j] = min(_a + M[i - 1][j - 1],
                          g + M[i - 1][j],
                          g + M[i][j - 1])
    return M, M[m-1][n-1]


def get_sequence(x, y, g, a, M):
    """ Recovers the sequence alignment based on the matrix of cost.
            Args:
                x   - First string
                y   - Second string
                g   - Gap penalty
                a   - Mismatch penalty
                M   - Matrix of cost
    """
    
    print "x: %s, y: %s " % (x, y)
    diff = [[], []]
    find_sequence(len(x) - 1, len(y) - 1, x, y, g, a, M, diff)
    diff[0].reverse()
    diff[1].reverse()
    return "".join(diff[0]), "".join(diff[1])


def find_sequence(i, j, x, y, g, a, M, diff):
    if i < 0:
        for i in reversed(range(len(y) - 1)):
            _add_to_diff(diff, "*", y[i])
        return
    elif j< 0:
        for i in reversed(range(len(x) - 1)):
            _add_to_diff(diff, x[i], "*")
        return
    if i > 0 or j > 0:
        _a = 0 if x[i] == y[j] else a
        if M[i+1][j+1] == _a + M[i][j]:
            if _a == a:
                _add_to_diff(diff, "<%s>" % x[i], "<%s>" % y[j])
            else:
                _add_to_diff(diff, x[i], y[j])
            return find_sequence(i - 1, j - 1, x, y, g, a, M, diff)
        elif M[i + 1][j + 1] == g + M[i][j + 1]:
            _add_to_diff(diff, x[i], "*")
            return find_sequence(i - 1, j, x, y, g, a, M, diff)
        else:
            _add_to_diff(diff, "*", y[j])
            return find_sequence(i, j - 1, x, y, g, a, M, diff)
    elif j == 0 and i == 0:
        _add_to_diff(diff, x[i], y[j])

def _add_to_diff(diff, x, y):
    diff[0].append(x)
    diff[1].append(y)


def linear_sequence_alignment(x, y, g, a):
    """ Determines optimal sequence alignment for two strings (x and y) with\
        linear space.
            Args:
                x   - First string
                y   - Second string
                g   - Gap penalty
                a   - Mismatch penalty
    """
    _x = "*%s" % x
    _y = "*%s" % y
    m = len(_x)  # Number of characters in x
    n = len(_y)  # Number of characters in y
    CURRENT = [i * g for i in range(m)]

    for j in range(1, n):
        LAST = deepcopy(CURRENT)
        CURRENT[0] = j * g
        for i in range(1, m):
            _a = 0 if (_x[i] == _y[j]) else a
            CURRENT[i] = min(_a + LAST[i - 1], g + LAST[i], g + CURRENT[i - 1])
    return CURRENT, CURRENT[m - 1]


def divide_and_conquer_alignment_1(x, y, g, a):
    m = len(x)
    n = len(y)

    if m >= 0 and n >= 0:
        if m <= 2 or n <= 2:
            print optmal_alignment(x, y, g, a)
        else:
            _f, _ = linear_sequence_alignment(x, y[:int(n/2)], g, a)
            _g, _ = linear_sequence_alignment(x[::-1], y[int(n/2):][::-1], g, a)
            r = [_f[i] + _g[i] for i in range(len(_f))]
            print r
            q = r.index(min(r))
            n = len(r)
            print "q", q
            print "xq", x[q]
            print ">-", x[:q+1], y[:n/2]
            divide_and_conquer_alignment_1(x[:q+1], y[:int(ceil(n / 2.0))], g, a)
            print ">--", x[q+1:], y[n / 2:]
            divide_and_conquer_alignment_1(x[q+1:], y[int(ceil(n / 2.0)):], g, a)


def optmal_alignment(x, y, g, a):
    m, cost = sequence_alignemt(x, y, g, a)
    return get_sequence(x, y, g, a, m)
