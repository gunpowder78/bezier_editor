import numpy as np
from scipy.spatial import ConvexHull
from algorithms import casteljau, split_bezier, degree_elevation, degree_reduction
from PyQt4.QtGui import QColor
from PyQt4.QtCore import Qt


class Curve(object):
    def __init__(self, control_points=None, curve_color=QColor(Qt.red), points_color=QColor(Qt.red),
                 hull_color=QColor(Qt.red), size=3, hull_selection=True):
        self.control_points = control_points or []
        self.curve_points = self.compute() if control_points else []
        self.curve_color = curve_color
        self.points_color = points_color
        self.hull_color = hull_color
        self.hull_selection = hull_selection
        self.size = size
        self.center = []
        self.tmp_control_points = []  # used when rotating or moving object
        self.tmp_curve_points = []  # used when rotating or moving object

    def append(self, p):
        self.control_points.append(p)
        self.compute()

    def insert(self, i, p):
        self.control_points.insert(i, p)
        self.compute()

    def pop(self, i):
        point = self.control_points.pop(i)
        self.compute()
        return point

    def change(self, i, p):
        self.control_points[i] = p
        self.compute()

    def copy(self):
        return Curve(control_points=self.control_points[:], curve_color=self.curve_color,
                     points_color=self.points_color, hull_color=self.hull_color, size=self.size,
                     hull_selection=self.hull_selection)

    def split(self, i, n=1000):
        left, right = split_bezier(np.linspace(0, 1, n), np.asarray(self.control_points), i)
        self.control_points = left.tolist()
        self.compute()
        return Curve(control_points=right.tolist(), curve_color=self.curve_color,
                     points_color=self.points_color, hull_color=self.hull_color, size=self.size,
                     hull_selection=self.hull_selection)

    def translate(self, dx, dy):
        self.control_points = [(px-dx, py-dy) for px, py in self.control_points]
        self.curve_points -= [dx, dy]
        self.calculate_center()
        self.update_tmp_points()

    def rotate(self, alpha):
        tmp_control_points = np.array(self.tmp_control_points) - self.center
        tmp_curve_points = self.tmp_curve_points - self.center

        # 2D Rotation matrix
        R = np.array([[np.cos(alpha), -np.sin(alpha)],
                      [np.sin(alpha), np.cos(alpha)]])

        self.control_points = (R[:, None, :].dot(tmp_control_points.T)[:, 0, :].T + self.center).tolist()
        self.curve_points = R[:, None, :].dot(tmp_curve_points.T)[:, 0, :].T + self.center

    def join(self, head, val, c1=False, val2=None):
        assert head in [0, -1]
        dx, dy = self.control_points[head][0] - val[0], self.control_points[head][1] - val[1]
        if c1 and val2 is not None:
            next_val_idx = head + 1 if head == 0 else head - 1
            self.control_points = [(px - dx, py - dy) for px, py in self.control_points]
            self.control_points[next_val_idx] = [2*self.control_points[head][0] - val2[0],
                                                 2*self.control_points[head][1] - val2[1]]
            self.compute()
        else:
            self.translate(dx, dy)

    def degree_elevation(self):
        if len(self.control_points) > 2:
            self.control_points = degree_elevation(self.control_points).tolist()
            self.compute()

    def degree_reduction(self):
        if len(self.control_points) > 3:
            self.control_points = degree_reduction(self.control_points).tolist()
            self.compute()

    def compute(self, n=1000):
        points = np.array(self.control_points)
        if len(points) < 2:
            self.curve_points = np.array(points)
        else:
            self.curve_points = casteljau(np.linspace(0, 1, n), points.T)
            self.calculate_center()
        self.update_tmp_points()
        return self.curve_points

    def calculate_center(self):
        cp = np.array(self.control_points)
        self.center = np.array([(cp[:, 0].max(axis=0) + cp[:, 0].min(axis=0)) / 2,
                                (cp[:, 1].max(axis=0) + cp[:, 1].min(axis=0)) / 2])

    def convex_hull(self):
        points = np.array(self.control_points)
        if len(points) < 3:
            return points
        vertices = ConvexHull(points).vertices.tolist()
        return points[vertices + vertices[:1], :]

    def update_color(self, kind, color):
        if kind == 'curve':
            self.curve_color = color
        elif kind == 'points':
            self.points_color = color
        elif kind == 'hull':
            self.hull_color = color

    def update_tmp_points(self):
        self.tmp_control_points = [[x, y] for x, y in self.control_points]
        self.tmp_curve_points = self.curve_points.copy()
