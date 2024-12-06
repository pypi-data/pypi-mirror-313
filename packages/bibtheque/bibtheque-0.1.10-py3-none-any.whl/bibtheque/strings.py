import numpy as np
from numba import njit

#  ──────────────────────────────────────────────────────────────────────────
# functions

@njit(fastmath=True)
def optimal_string_alignment(a, b):
    """Calculates the Optimal String Alignment distance between two strings.

    Parameters
    ----------
    a : str
        First string to compare.
    b : str
        Second string to compare.

    Returns
    -------
    distance : 
    similarity :

    Notes
    -----
    https://en.wikipedia.org/wiki/Damerau–Levenshtein_distance#Optimal_string_alignment_distance
    """

    M = len(a)
    N = len(b)

    d = np.zeros((M + 1, N + 1))
    
    for i in range(d.shape[0]):
        d[i, 0] = i

    for j in range(d.shape[1]):
        d[0, j] = j

    for i in range(M):
        for j in range(N):

            if a[i] == b[j]:
                cost = 0
            else:
                cost = 1

            I = i + 1
            J = j + 1

            d[I, J] = np.min(np.array([d[I - 1, J] + 1, d[I, J - 1] + 1, d[I - 1, J - 1] + cost]))

            if i > 0 and j > 0 and a[i] == b[j - 1] and a[i - 1] == b[j]:
                d[I, J] = np.min(np.array([d[I, J], d[I - 2, J - 2] + 1]))

    distance = d[-1, -1]
    similarity = (M + N - distance) / (M + N)

    return distance, similarity


def matching(a, b, threshold):
    """
    Determines if strings a and b have a similarity greater than the given threshold.
    """

    _, similarity = optimal_string_alignment(a, b)

    if similarity > threshold:
        return True
    else:
        return False
