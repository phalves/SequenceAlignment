from copy import copy
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
    m = len(x)  # Number of characters in x
    n = len(y)  # Number of characters in y
    M = [[0 for i in range(n)] for j in range(m)]

    # Fills the first line of the matrix
    for i in range(m):
        M[i][0] = i*g
    # Fills the first column of the matrix
    for j in range(n):
        M[0][j] = j*g

    for i in range(1, m):
        for j in range(1, n):
            _a = 0 if x[i] == y[j] else a
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
    diff = [[], []]
    find_sequence(len(x) - 1, len(y) - 1, x, y, g, a, M, diff)
    diff[0].reverse()
    diff[1].reverse()
    return "".join(diff[0]), "".join(diff[1])


def find_sequence(i, j, x, y, g, a, M, diff):
    if i > 0 or j > 0:
        _a = 0 if x[i] == y[j] else a
        if M[i][j] == _a + M[i - 1][j - 1]:
            if _a == a:
                _add_to_diff(diff, "<%s>" % x[i], "<%s>" % y[j])
            _add_to_diff(diff, x[i], y[j])
            return find_sequence(i - 1, j - 1, x, y, g, a, M, diff)
        elif M[i][j] == g + M[i - 1][j]:
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
    m = len(x)  # Number of characters in x
    n = len(y)  # Number of characters in y
    CURRENT = [i * g for i in range(m)]

    for j in range(1, n):
        LAST = copy(CURRENT)
        CURRENT[0] = j * a
        for i in range(1, m):
            _a = 0 if (x[i] == y[j]) else a
            CURRENT[i] = min(_a + LAST[i - 1], g + LAST[i], g + CURRENT[i - 1])

    return CURRENT, CURRENT[m - 1]
