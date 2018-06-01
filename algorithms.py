from numpy import asarray, shape, dot, ones, cumsum
import numpy as np


def prod(ns):
    return reduce(lambda x, y: x * y, ns, 1)


def outer(A, B):
    """Outer product, differs from numpy version for special cases
    of scalar arguments:
        >>> outer([2, 3], [10, 100])
        array([[ 20, 200],
               [ 30, 300]])
        >>> outer([2, 3], 10)
        array([20, 30])
        >>> outer(10, [2, 3])
        array([20, 30])
    """
    M = prod(shape(A))
    N = prod(shape(B))
    K = 1

    A = asarray(A)
    B = asarray(B)

    C = dot(A.reshape(M, K), B.reshape(K, N))
    return C.reshape(shape(A) + shape(B))


def casteljau(t, p, by=None):
    t = asarray(t)
    p = asarray(p)

    n = shape(p)[-1] - 1  # number of parameters

    b = outer(ones(shape(t)), p)
    if by is not None:
        _coefs = []
    x = outer(1. - t, ones(shape(p[..., 0])))
    y = outer(t, ones(shape(p[..., 0])))

    for j in xrange(n):
        for i in xrange(n - j):
            b[..., i] = x * b[..., i] + y * b[..., i+1]
            if by:
                _coefs.append(tuple(b[by, :, i]))
    if by:
        return b[..., 0], _coefs
    return b[..., 0]


def split_bezier(t, p, by):
    _, coefs = casteljau(t, p.T, by)
    left_curve = [p[0, :]]
    right_curve = []
    n = len(p) - 1
    for a in np.split(coefs, cumsum(range(n, 0, -1)))[:-1]:
        left_curve.append(a[0])
        right_curve.append(a[-1])
    right_curve = right_curve[::-1] + [p[-1, :]]
    return asarray(left_curve), asarray(right_curve)
