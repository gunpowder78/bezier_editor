from PyQt4.QtGui import QWidget, QPolygonF, QPainter, QPen, QBrush, QColor, \
    QVBoxLayout, QPalette, QPixmap, QCursor
from PyQt4.QtCore import Qt, QRectF, QPointF
import numpy as np
from curve import Curve
from tools import Tools
from itertools import chain


class Canvas(QWidget):
    def __init__(self, context, signals, parent=None):
        QWidget.__init__(self, parent)

        self.curves = []
        self.curve = None
        self.high_light_points = []

        self.context = context
        self.signals = signals

        self.setBackgroundRole(QPalette.Dark)
        self.setAttribute(Qt.WA_TranslucentBackground)
        main_layout = QVBoxLayout()
        main_layout.addStretch(1)

        self.setLayout(main_layout)
        self.tracking = None

        self.signals.hull_selection.connect(self.update_curve)
        self.signals.update_color.connect(self.update_curve)
        self.signals.update_pencil_size.connect(self.update_curve)
        self.signals.update_tool.connect(self.update_cursor)
        self.signals.change_curve.connect(self.set_current_curve)
        self.signals.delete_curves.connect(self.delete_curves)

        self.update_cursor()

    def set_current_curve(self):
        if self.context.current_curve is not None:
            if len(self.curves) - 1 < self.context.current_curve:
                self.add_curve()
            self.curve = self.curves[self.context.current_curve]
            self.context.hull_selection = self.curve.hull_selection
            self.signals.hull_selection.emit(self.context.hull_selection)
            self.update()

    def add_curve(self):
        c = Curve(curve_color=self.context.curve_color, points_color=self.context.points_color,
                  hull_color=self.context.hull_color, size=self.context.pencil_size,
                  hull_selection=self.context.hull_selection)
        self.curves.append(c)

    def delete_curves(self):
        for idx in self.context.curves_to_remove:
            self.curves.pop(idx)
        self.context.curves_to_remove = []
        self.set_current_curve()

    @staticmethod
    def poly(pts):
        return QPolygonF(map(lambda p: QPointF(*p), pts))

    def paintEvent(self, event):
        def actions(curve, pen_size=1):
            # draw bezier curve
            painter.setPen(QPen(curve.curve_color, curve.size, Qt.DashDotDotLine))
            painter.drawPolyline(self.poly(curve.curve_points))

            # draw hull
            if curve.hull_selection:
                painter.setPen(QPen(curve.hull_color, 3, Qt.SolidLine))
                painter.drawPolyline(self.poly(curve.convex_hull()))

            # draw points
            painter.setBrush(QBrush(curve.points_color))
            painter.setPen(QPen(QColor(Qt.lightGray), pen_size))
            for x, y in curve.control_points:
                painter.drawEllipse(QRectF(x - 4, y - 4, 8, 8))
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing)

        for i, curve in enumerate(self.curves):
            if curve and i != self.context.current_curve:
                actions(curve, pen_size=1)
            elif curve and i == self.context.current_curve:
                actions(self.curve, pen_size=3)

        for curve_idx, point_idx, _ in self.high_light_points:
            painter.setBrush(QBrush(self.curves[curve_idx].points_color))
            painter.setPen(QPen(QColor(Qt.lightGray), 3))
            x, y = self.curves[curve_idx].control_points[point_idx]
            painter.drawEllipse(QRectF(x - 4, y - 4, 8, 8))

    def mousePressEvent(self, event):
        if not self.curve:
            return
        pos = [event.x(), event.y()]

        def move(p):
            dx, dy = pos[0] - p[0], pos[1] - p[1]
            self.curve.translate(dx, dy)
            pos[:] = p[:]

        if self.context.current_tool == Tools.Grab:
            self.tracking = move
        elif self.context.current_tool == Tools.Pencil:
            self.curve.append((event.x(), event.y()))
            self.update()
        elif self.context.current_tool == Tools.Selection:
            if not self.curve.control_points:
                return
            pp = np.array(self.curve.control_points)
            pp = ((pp[:, 0] - event.x())**2 + (pp[:, 1] - event.y())**2)
            if pp.min() < 200:
                self.tracking = lambda p: self.curve.change(pp.argmin(), p)
        elif self.context.current_tool == Tools.Eraser:
            pp = np.array(self.curve.control_points)
            pp = ((pp[:, 0] - event.x()) ** 2 + (pp[:, 1] - event.y()) ** 2)
            if pp.min() < 200:
                self.curve.pop(pp.argmin())
                self.update()
        elif self.context.current_tool == Tools.Slice:
            pp = self.curve.curve_points
            pp = ((pp[:, 0] - event.x()) ** 2 + (pp[:, 1] - event.y()) ** 2)
            if pp.min() < 100:
                new_curve = self.curve.split(pp.argmin())
                self.curves.append(new_curve)
                self.signals.add_curves.emit()
                self.update()
        elif self.context.current_tool == Tools.Copy:
            new_curve = self.curve.copy()
            new_curve.translate(10, 10)  # for visual effect
            self.curves.append(new_curve)
            self.signals.add_curves.emit()
            self.update()
        elif self.context.current_tool == Tools.Join:  # not working
            def high_light(p):
                move(p)
                curve_end_points = [self.curve.control_points[0], self.curve.control_points[-1]]
                pp = ((end_points[:, None, :] - curve_end_points).reshape((-1, 2)) ** 2).sum(axis=1)
                idx = pp.argmin()
                if pp[idx] < 400 and (idx//4) != self.context.current_curve:
                    curve_end = (idx % 2) * -1
                    matching_curve_end = ((idx % 4) // 2) * -1
                    idx = idx // 4
                    self.high_light_points = [(idx, matching_curve_end, curve_end)]
                    self.update()
                else:
                    self.high_light_points = []
                    self.update()
            end_points = np.array(list(chain.from_iterable((c.control_points[0], c.control_points[-1]) for c in self.curves)))
            self.tracking = high_light
        elif self.context.current_tool == Tools.Rotate:
            def rot(p):
                curr_pos_x, curr_pos_y = p - self.curve.center
                alpha = np.arctan2(curr_pos_y, curr_pos_x) - alpha0
                self.curve.rotate(alpha)

            pos0_x, pos0_y = pos - self.curve.center[1]
            alpha0 = np.arctan2(pos0_y, pos0_x)
            self.tracking = rot
        elif self.context.current_tool == Tools.Elevate:
            self.curve.degree_elevation()
            self.update()
        elif self.context.current_tool == Tools.Reduce:
            self.curve.degree_reduction()
            self.update()

    def mouseMoveEvent(self, event):
        if self.tracking:
            self.tracking((event.x(), event.y()))
            self.update()

    def mouseReleaseEvent(self, event):
        self.tracking = None
        if self.context.current_tool == Tools.Join and self.high_light_points:
            curve_idx, curve_end, head = self.high_light_points[-1]
            self.high_light_points = []
            v1 = self.curves[curve_idx].control_points[curve_end]
            v2 = self.curves[curve_idx].control_points[curve_end + 1 if curve_end == 0 else curve_end - 1]
            self.curve.join(head, v1, self.context.c1_join, v2)
            self.update()
        elif self.context.current_tool == Tools.Rotate:
            self.curve.update_tmp_points()

    def update(self):
        super(Canvas, self).update()

    def update_cursor(self):
        path = Tools.get_cursor_path(self.context.current_tool)
        if path:
            self.setCursor(QCursor(QPixmap(path), 2, 17))
        else:
            self.unsetCursor()

    def update_curve(self):
        if self.curve is not None:
            self.curve.size = self.context.pencil_size
            if self.context.selected_color == 'curve':
                self.curve.update_color(self.context.selected_color, self.context.curve_color)
            elif self.context.selected_color == 'points':
                self.curve.update_color(self.context.selected_color, self.context.points_color)
            elif self.context.selected_color == 'hull':
                self.curve.update_color(self.context.selected_color, self.context.hull_color)
            self.curve.hull_selection = self.context.hull_selection
            self.update()
