from algorithms import prod, outer, casteljau, degree_elevation, degree_reduction, split_bezier
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
    np.testing.assert_array_equal(result, casteljau(t, p))


def test_casteljau_with_weights():
    t = np.linspace(0, 1, 5)
    p = np.array([[10, 10], [20, 10], [20, 20]]).T
    w = [.5, 1, 1]
    result = np.array([[10., 10.],
                       [16.08695652, 10.86956522],
                       [18.57142857, 12.85714286],
                       [19.67741935, 15.80645161],
                       [20., 20.]])
    np.testing.assert_array_almost_equal(result, casteljau(t, p, weights=w))


def test_split_bezier():
    t = np.linspace(0, 1, 5)
    p = np.array([[0, 0], [0, 1], [1, 2], [2, 1], [2, 0]])
    expected_left = np.array([[0., 0.],
                              [0., 0.5],
                              [0.25, 1.],
                              [0.625, 1.25],
                              [1., 1.25]])
    expected_right = np.array([[1., 1.25],
                               [1.375, 1.25],
                               [1.75, 1.],
                               [2., 0.5],
                               [2., 0.]])

    left, right, _, _ = split_bezier(t, p, by=2)
    np.testing.assert_array_equal(expected_left, left)
    np.testing.assert_array_equal(expected_right, right)


def test_split_bezier_with_weights_only_ones():
    t = np.linspace(0, 1, 5)
    p = np.array([[0, 0], [0, 1], [1, 2], [2, 1], [2, 0]])
    weights = [1, 1, 1, 1, 1]
    expected_left = np.array([[0., 0.],
                              [0., 0.5],
                              [0.25, 1.],
                              [0.625, 1.25],
                              [1., 1.25]])
    expected_right = np.array([[1., 1.25],
                               [1.375, 1.25],
                               [1.75, 1.],
                               [2., 0.5],
                               [2., 0.]])

    left, right, l_w, r_w = split_bezier(t, p, by=2, w=weights)
    np.testing.assert_array_equal(expected_left, left)
    np.testing.assert_array_equal(expected_right, right)
    np.testing.assert_array_equal(np.ones(len(weights)), l_w)
    np.testing.assert_array_equal(np.ones(len(weights)), r_w)


def test_split_bezier_with_weights():
    t = np.linspace(0, 1, 5)
    p = np.array([[0, 0], [0, 1], [1, 2], [2, 1], [2, 0]])
    weights = [1, 2, 1, 2, 1]
    expected_left = np.array([[0., 0.],
                              [0., 0.66666667],
                              [0.16666667, 1.],
                              [0.58333333, 1.16666667],
                              [1., 1.16666667]])
    expected_right = np.array([[1., 1.16666667],
                               [1.41666667, 1.16666667],
                               [1.83333333, 1.],
                               [2., 0.66666667],
                               [2., 0.]])
    expected_l_w = np.array([1., 1.5, 1.5, 1.5, 1.5])
    expected_r_w = np.array([1.5, 1.5, 1.5, 1.5, 1.])

    left, right, l_w, r_w = split_bezier(t, p, by=2, w=weights)

    np.testing.assert_array_almost_equal(expected_left, left)
    np.testing.assert_array_almost_equal(expected_right, right)
    np.testing.assert_array_equal(expected_l_w, l_w)
    np.testing.assert_array_equal(expected_r_w, r_w)


def test_degree_elevation_without_weights():
    control_points = [[0, 0], [1, 1], [2, 0]]
    expected_new_control_points = np.array([[0, 0], [.75, .75], [1.5, .5], [2, 0]])
    expected_new_weights = np.ones((len(control_points) + 1))

    new_points, new_weights = degree_elevation(control_points)
    np.testing.assert_array_equal(expected_new_control_points, new_points)
    np.testing.assert_array_equal(expected_new_weights, new_weights)


def test_degree_elevation_with_weights():
    control_points = [[0, 0], [1, 1], [2, 0]]
    weights = [1, 2, 3]
    expected_new_control_points = np.array([[0, 0], [6/7., 6/7.], [1.6, .4], [2, 0]])
    expected_new_weights = np.array([1, 1.75, 2.5, 3])

    new_points, new_weights = degree_elevation(control_points, w=weights)
    np.testing.assert_array_equal(expected_new_control_points, new_points)
    np.testing.assert_array_equal(expected_new_weights, new_weights)


def test_degree_reduction_matching():
    control_points = [[0, 0], [.75, .75], [1.5, .5], [2, 0]]
    expected_new_control_points = np.array([[0, 0], [1, 1], [2, 0]])
    expected_new_weights = np.ones((len(control_points) - 1))

    new_points, new_weights = degree_reduction(control_points)
    np.testing.assert_array_equal(expected_new_control_points, new_points)
    np.testing.assert_array_equal(expected_new_weights, new_weights)


def test_degree_reduction_non_matching():
    control_points = [[0, 0], [1, 1], [1.5, .5], [2, 0]]
    expected_new_control_points = np.array([[0, 0], [7./6, 7./6], [2, 0]])
    expected_new_weights = np.ones((len(control_points) - 1))

    new_points, new_weights = degree_reduction(control_points)
    np.testing.assert_array_almost_equal(expected_new_control_points, new_points, decimal=6)
    np.testing.assert_array_equal(expected_new_weights, new_weights)


def test_degree_reduction_matching_with_weights():
    control_points = [[0, 0], [6/7., 6/7.], [1.6, .4], [2, 0]]
    weights = [1, 1.75, 2.5, 3]
    expected_new_control_points = np.array([[0, 0], [1, 1], [2, 0]])
    expected_new_weights = np.array([1, 2, 3])

    new_points, new_weights = degree_reduction(control_points, w=weights)
    np.testing.assert_array_equal(expected_new_control_points, new_points)
    np.testing.assert_array_equal(expected_new_weights, new_weights)


def test_degree_reduction_non_matching_with_weights():
    control_points = [[0, 0], [.75, .75], [1.5, .5], [2, 0]]
    weights = [1, 2, 3, 4]
    expected_new_control_points = np.array([[0, 0], [9./13, 15./13], [2, 0]])
    expected_new_weights = np.array([1, 13./6, 4])

    new_points, new_weights = degree_reduction(control_points, w=weights)
    np.testing.assert_array_almost_equal(expected_new_control_points, new_points, decimal=6)
    np.testing.assert_array_almost_equal(expected_new_weights, new_weights, decimal=6)

