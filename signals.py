#!/usr/bin/env python
# coding: utf-8

from PyQt4 import QtCore


class Signals(QtCore.QObject):
    update_color = QtCore.pyqtSignal()

    update_tool = QtCore.pyqtSignal([int])

    update_pencil_size = QtCore.pyqtSignal([int])

    hull_selection = QtCore.pyqtSignal([bool])

    change_curve = QtCore.pyqtSignal()
    delete_curves = QtCore.pyqtSignal([list])
    add_curve_to_widget = QtCore.pyqtSignal()
    add_curve_to_backend = QtCore.pyqtSignal()

    new_point = QtCore.pyqtSignal()
    delete_point = QtCore.pyqtSignal([int])
    change_weight = QtCore.pyqtSignal([int, float])
    change_weights = QtCore.pyqtSignal([list])
