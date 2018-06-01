import pytest
from mock import sentinel, mock
import curve
from curve import Curve


@pytest.fixture
def basic_curve_parameters():
    return {'control_points': None,
            'curve_color': sentinel.curve_color,
            'points_color': sentinel.points_color,
            'hull_color': sentinel.hull_color,
            'size': sentinel.size,
            'hull_selection': sentinel.hull_selection}


@pytest.fixture
def basic_curve(basic_curve_parameters):
    curve = Curve(**basic_curve_parameters)
    curve.compute = mock.Mock()
    return curve


class TestCurveInit:
    def test_init_empty_curve(self, basic_curve, basic_curve_parameters):
        assert [] == basic_curve.control_points
        assert basic_curve_parameters['curve_color'] == basic_curve.curve_color
        assert basic_curve_parameters['points_color'] == basic_curve.points_color
        assert basic_curve_parameters['hull_color'] == basic_curve.hull_color
        assert basic_curve_parameters['size'] == basic_curve.size
        assert basic_curve_parameters['hull_selection'] == basic_curve.hull_selection


class TestCurveAppend:
    def test_basic_append(self, basic_curve):
        point = (sentinel.x, sentinel.y)
        basic_curve.append(point)
        assert point in basic_curve.control_points


class TestCurveInsert:
    def test_basic_insert(self, basic_curve):
        basic_curve.control_points = [(sentinel.xa, sentinel.ya), (sentinel.xc, sentinel.yc)]
        index = 1
        point = (sentinel.xb, sentinel.yb)

        basic_curve.insert(index, point)
        assert point in basic_curve.control_points
        assert point == basic_curve.control_points[index]


class TestCurvePop:
    def test_basic_pop(self, basic_curve):
        point = (sentinel.xb, sentinel.yb)
        basic_curve.control_points = [(sentinel.xa, sentinel.ya), point, (sentinel.xc, sentinel.yc)]
        index = 1

        result = basic_curve.pop(index)
        assert point not in basic_curve.control_points
        assert point == result


class TestCurveChange:
    def test_basic_change(self, basic_curve):
        point = (sentinel.xb, sentinel.yb)
        basic_curve.control_points = [(sentinel.xa, sentinel.ya), point, (sentinel.xc, sentinel.yc)]
        index = 1

        basic_curve.change(index, point)
        assert point == basic_curve.control_points[index]


class TestCurveCopy:
    def test_basic_change(self, basic_curve):
        basic_curve.control_points = [(sentinel.xa, sentinel.ya)]

        new_curve = basic_curve.copy()
        assert new_curve.control_points == basic_curve.control_points
        assert new_curve.curve_color == basic_curve.curve_color
        assert new_curve.points_color == basic_curve.points_color
        assert new_curve.hull_color == basic_curve.hull_color
        assert new_curve.size == basic_curve.size
        assert new_curve.hull_selection == basic_curve.hull_selection


class TestCurveSplit:
    def test_basic_split(self, basic_curve):
        points = [[sentinel.xa, sentinel.ya], [sentinel.xb, sentinel.yb]]
        basic_curve.control_points = points
        curve.split_bezier = lambda a, x, b: x

        new_curve = basic_curve.split(sentinel.index)

        assert new_curve.control_points == points[1]
        assert basic_curve.control_points == points[0]

        assert new_curve.curve_color == basic_curve.curve_color
        assert new_curve.points_color == basic_curve.points_color
        assert new_curve.hull_color == basic_curve.hull_color
        assert new_curve.size == basic_curve.size
        assert new_curve.hull_selection == basic_curve.hull_selection
