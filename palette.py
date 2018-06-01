#!/usr/bin/env python
# coding: utf-8

from PyQt4 import QtGui
from PyQt4.QtCore import Qt


class CurrentColor(QtGui.QLabel):

    def __init__(self, kind, context, signals, parent=None):

        super(CurrentColor, self).__init__()

        self.parent = parent
        self.context = context
        self.signals = signals
        self.signals.updateColor.connect(self.update)
        self.kind = kind

        if kind == 'curve':
            self.color = self.context.curve_color
            self.setObjectName("curve_color")
            self.setText('Curve')
        elif kind == 'points':
            self.color = self.context.points_color
            self.setObjectName("points_color")
            self.setText('Points')
        elif kind == 'hull':
            self.color = self.context.hull_color
            self.setObjectName("hull_color")
            self.setText('Hull')

        self.setStyleSheet("background-color: " + self.color.name() + ";")
        self.setFixedHeight(24)

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.RightButton:
            c = QtGui.QColorDialog.getColor(self.color)
            if c.isValid():
                if self.kind == 'curve':
                    self.context.change_curve_color(c)
                elif self.kind == 'points':
                    self.context.change_points_color(c)
                elif self.kind == 'hull':
                    self.context.change_hull_color(c)

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.setLineWidth(3)
            self.context.selected_color = self.kind
            self.signals.updateColor.emit()

    def update(self):
        if self.kind == 'curve':
            self.color = self.context.curve_color
        elif self.kind == 'points':
            self.color = self.context.points_color
        elif self.kind == 'hull':
            self.color = self.context.hull_color

        if self.kind == self.context.selected_color:
            self.setLineWidth(3)
        else:
            self.setLineWidth(0)
        self.setStyleSheet("background-color: " + self.color.name() + ";")

        super(CurrentColor, self).update()


class Color(QtGui.QFrame):
    def __init__(self, position, color, context, signals, parent=None):

        super(Color, self).__init__(parent)

        self.parent = parent
        self.context = context
        self.signals = signals

        self.position = position
        self.color = QtGui.QColor(color[0], color[1], color[2])

        self.setObjectName("Color")
        self.setFixedSize(12, 12)
        self.setStyleSheet("background-color: " + self.color.name() + ";")

        self.setAcceptDrops(True)

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            if self.context.selected_color == 'curve':
                self.context.change_curve_color(self.color)
            elif self.context.selected_color == 'points':
                self.context.change_points_color(self.color)
            elif self.context.selected_color == 'hull':
                self.context.change_hull_color(self.color)
        elif e.button() == Qt.MidButton:
            c = QtGui.QColorDialog.getColor(self.color)
            if c.isValid():
                self.change_color(c)

    def update(self):
        self.setStyleSheet("background-color: " + self.color.name() + ";")
        super(Color, self).update()

    def change_color(self, c):
        self.color = c
        self.context.palette[self.position] = [c.red(), c.green(), c.blue()]
        self.update()


class Palette(QtGui.QWidget):

    def __init__(self, context, signals, parent=None):

        super(Palette, self).__init__(parent)

        self.parent = parent
        self.context = context
        self.signals = signals
        self.setObjectName("Palette")

        palette = QtGui.QGridLayout()
        for i in range(5):
            for j in range(12):
                palette.addWidget(Color(i * 12 + j, self.context.palette[i * 12 + j], self.context, self.signals), i, j)

        palette.setSpacing(1)

        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(CurrentColor('curve', self.context, self.signals))
        hbox.addWidget(CurrentColor('points', self.context, self.signals))
        hbox.addWidget(CurrentColor('hull', self.context, self.signals))
        hbox.setSpacing(2)

        vbox = QtGui.QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addLayout(palette)
        vbox.setSpacing(2)

        self.setLayout(vbox)
        self.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)

        palette.setSpacing(1)
