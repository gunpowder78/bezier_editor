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


def casteljau(t, p, by=None, weights=None):
    t = asarray(t)
    p = asarray(p)

    n = shape(p)[-1] - 1  # number of parameters
    if weights is None:
        w = outer(ones(shape(t)), ones(shape(p)))
    else:
        assert len(weights) == shape(p)[-1]
        w = asarray(weights).reshape((1, len(weights)))
        w = outer(ones(shape(t)), np.vstack((w, w)))

    b = outer(ones(shape(t)), p)
    if by is not None:
        _coefs = []
        _coefs_w = []
    x = outer(1. - t, ones(shape(p[..., 0])))
    y = outer(t, ones(shape(p[..., 0])))

    for j in xrange(n):
        for i in xrange(n - j):
            w_i = x * w[..., i] + y * w[..., i+1]
            b[..., i] = x * w[..., i] / w_i * b[..., i] + y * w[..., i+1] / w_i * b[..., i+1]
            w[..., i] = w_i
            if by:
                _coefs.append(tuple(b[by, :, i]))
                _coefs_w.append(w[by, 0, i])
    if by:
        return b[..., 0], _coefs, _coefs_w
    return b[..., 0]


def split_bezier(t, p, by, w=None):
    _, coefs, coefs_w = casteljau(t, p.T, by, weights=w)
    left_curve = [p[0, :]]
    right_curve = []
    n = len(p) - 1
    for a in np.split(coefs, cumsum(range(n, 0, -1)))[:-1]:
        left_curve.append(a[0])
        right_curve.append(a[-1])
    right_curve = right_curve[::-1] + [p[-1, :]]

    left_w = []
    right_w = []
    if w is not None:
        left_w.append(w[0])
        for a in np.split(coefs_w, cumsum(range(n, 0, -1)))[:-1]:
            left_w.append(a[0])
            right_w.append(a[-1])
        right_w = right_w[::-1] + [w[-1]]
    return asarray(left_curve), asarray(right_curve), asarray(left_w), asarray(right_w)


def degree_elevation(p, w=None):
    n = len(p)
    w = asarray(w).reshape((n, 1)) if w is not None else np.ones((n, 1))
    pp = np.hstack((np.array(p) * w, w))

    new_points = np.zeros((n+1, 3))
    new_points[0, ...] = pp[0, ...]
    new_points[-1, ...] = pp[-1, ...]

    coefs = np.arange(1, n, dtype=float).reshape(n - 1, 1)
    new_points[1:-1, :] = (coefs * pp[:-1, :] + (n - coefs + 1) * pp[1:, :]) / (n + 1.)
    return new_points[:, :-1] / new_points[:, -1, None], new_points[:, -1]


def degree_reduction(p, w=None):
    n = len(p)
    w = asarray(w).reshape((n, 1)) if w is not None else np.ones((n, 1))
    pp = np.hstack((np.array(p) * w, w))

    left_points = [0]*(n/2)
    left_points[0] = pp[0, :]
    for k in xrange(1, n/2):
        coef = float(k)/(n-k)
        left_points[k] = (1 + coef) * pp[k, :] - coef * left_points[k-1]

    right_points = [0] * (n-n/2)
    right_points[-1] = pp[-1, :]
    for k in xrange(n-2, n/2-1, -1):
        coef = n/float(k)
        right_points[k-n/2] = coef * pp[k, :] + (1-coef) * right_points[k-n/2+1]

    if (left_points[-1] != right_points[0]).any():
        right_points[0] = (left_points[-1] + right_points[0]) / 2

    new_points = np.array(left_points[:-1] + right_points)
    return new_points[:, :-1] / new_points[:, -1, None], new_points[:, -1]

