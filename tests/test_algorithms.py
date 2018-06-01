from algorithms import prod, outer, casteljau, degree_elevation
import numpy as np


def test_prod():
    assert 20 == prod((1, 4, 5))
    assert 10 == prod((2, 5))


def test_outer():
    result = np.array([[20, 200], [30, 300]])
    assert (outer([2, 3], [10, 100]) == result).all()


def test_casteljau():
    t = np.linspace(0, 1, 5)
    p = np.array([[10, 10], [20, 10], [20, 20]]).T
    result = np.array([[10., 10.],
                       [14.375, 10.625],
                       [17.5, 12.5],
                       [19.375, 15.625],
                       [20., 20.]])
    res = casteljau(t, p)
    assert (res == result).all()


def test_degree_elevation():
    control_points = [[0, 0], [1, 1], [2, 0]]
    expected_new_control_points = np.array([[0, 0], [.75, .75], [1.5, .5], [2, 0]])

    np.testing.assert_array_equal(expected_new_control_points, degree_elevation(control_points))
