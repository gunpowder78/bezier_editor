#!/usr/bin/env python
# coding: utf-8

from PyQt4 import QtGui, QtCore


class Context:

    def __init__(self, signals):

        self.signals = signals

        self.palette = [[14, 53, 75], [0, 76, 115], [18, 121, 174], [49, 162, 238], [136, 199, 234], [27, 52, 43],
                        [30, 85, 55], [69, 145, 26], [121, 191, 29], [190, 222, 44], [69, 18, 18], [113, 31, 31],
                        [184, 37, 53], [220, 81, 115], [255, 159, 182], [39, 20, 67], [105, 28, 99], [173, 81, 185],
                        [184, 152, 208], [53, 48, 36], [89, 66, 40], [140, 92, 77], [208, 128, 112], [229, 145, 49],
                        [247, 176, 114], [252, 215, 142], [0, 0, 0], [33, 33, 33], [79, 79, 79], [179, 179, 179],
                        [255, 255, 255], [37, 42, 46], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0],
                        [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0],
                        [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0],
                        [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0],
                        [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]

        self.currentTool = 1
        self.curves_to_remove = []
        self.current_curve = None

        self.clipboard = QtGui.QApplication.clipboard()

        self.pencil_cur = QtGui.QCursor(QtGui.QPixmap("images/cursors/penicon.png"), 2, 17)
        self.eraser_cur = QtGui.QCursor(QtGui.QPixmap("images/cursors/erasericon.png"), 2, 17)
        self.grab_cur = QtGui.QCursor(QtGui.QPixmap("images/cursors/grab.png"), 2, 17)

        self.loadDefaults()
        self.hull_selection = True

        self.curve_color = QtGui.QColor(QtCore.Qt.red)
        self.points_color = QtGui.QColor(QtCore.Qt.red)
        self.hull_color = QtGui.QColor(QtCore.Qt.red)

        self.selected_color = 'curve'  # curve, points, hull

        self.join_type = False

    def set_hull_selection(self, x):
        self.hull_selection = x
        self.signals.hull_selection.emit(x)

    def set_current_curve(self, x):
        if x is not None:
            self.current_curve = x.index
        else:
            self.current_curve = None
        self.signals.change_curve.emit()

    def setPencilSize(self, size):
        if size < 10 and size > 0:
            self.pencilSize = size
            self.signals.updatePencilSize.emit(self.pencilSize)

    def set_join_type(self, x):
        self.join_type = x

    def setEraserSize(self, size):
        if size < 10 and size > 0:
            self.eraserSize = size
            self.signals.updateEraserSize.emit(self.eraserSize)

    def change_curve_color(self, c):

        self.curve_color = c
        self.signals.updateColor.emit()

    def change_points_color(self, c):

        self.points_color = c
        self.signals.updateColor.emit()

    def change_hull_color(self, c):

        self.hull_color = c
        self.signals.updateColor.emit()

    def changeCurrentTool(self, index):
        self.currentTool = index
        self.signals.updateTool.emit(index)

    def loadDefaults(self):
        self.transparentSelection = True
        self.pencilSize = 3
        self.secondaryColorEraser = False
        self.eraserSize = 1
