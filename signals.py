#!/usr/bin/env python
# coding: utf-8

from PyQt4 import QtCore


class Signals(QtCore.QObject):
    updateColor = QtCore.pyqtSignal()
    updateColorDeg = QtCore.pyqtSignal()

    updateTool = QtCore.pyqtSignal([int])
    autoUpdateTool = QtCore.pyqtSignal([int])

    transparentSelection = QtCore.pyqtSignal([bool])

    enterCanvas = QtCore.pyqtSignal()
    leaveCanvas = QtCore.pyqtSignal()
    overCanvas = QtCore.pyqtSignal([int, int])

    updatePencilSize = QtCore.pyqtSignal([int])
    updateEraserSize = QtCore.pyqtSignal([int])

    hull_selection = QtCore.pyqtSignal([bool])

    change_curve = QtCore.pyqtSignal()
    delete_curves = QtCore.pyqtSignal()
    add_curves = QtCore.pyqtSignal()

