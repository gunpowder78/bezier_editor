#!/usr/bin/env python
# coding: utf-8

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt


class _Tools(object):
    fields = [('Grab', 0, 'g'),
              ('Pencil', 1, 'p'),
              ('Eraser', 2, 'e'),
              ('Selection', 3, 's'),
              ('Slice', 4, 'k'),
              ('Join', 5, 'j'),
              ('Copy', 6, 'c'),
              ('Rotate', 7, 'r')]

    def __init__(self):
        for name, val, _ in self.fields:
            setattr(self, name, val)

    @classmethod
    def get_names(cls):
        return [name for name, _, _ in cls.fields]

    @classmethod
    def get_values(cls):
        return [val for _, val, _ in cls.fields]

    @classmethod
    def get_shortcuts(cls):
        return [shortcut for _, _, shortcut in cls.fields]

    @classmethod
    def get_fields(cls):
        return cls.fields


Tools = _Tools()


class SizeLabel(QtGui.QLabel):

    def set_value(self, value):
        self.setText(str(value))


class ToolProperties(QtGui.QDockWidget):

    def __init__(self, title, context, signals, parent=None):

        super(ToolProperties, self).__init__(title, parent)

        self.context = context
        self.signals = signals
        self.parent = parent
        self.setAllowedAreas(Qt.RightDockWidgetArea)
        self.setFeatures(QtGui.QDockWidget.NoDockWidgetFeatures)

        self.widgets = self.create_widgets()
        self.signals.updateTool.connect(self.update_widget)

        self.update_widget()

    def create_widgets(self):
        return [QtGui.QWidget(),
                self.create_pencil_widget(),
                QtGui.QWidget(),
                QtGui.QWidget(),
                QtGui.QWidget(),
                self.create_join_widget(),
                QtGui.QWidget(),
                QtGui.QWidget()]

    def create_size_widget(self, context, signal, slider_value=1):
        widget = QtGui.QWidget()
        widget.setObjectName("ToolProperties")
        widget.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)

        vbox = QtGui.QVBoxLayout()
        hbox = QtGui.QHBoxLayout()

        size_label = QtGui.QLabel("size")

        size_widget = SizeLabel(str(slider_value))

        slider = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        slider.setMaximum(9)
        slider.setMinimum(1)
        slider.setPageStep(1)
        slider.setValue(slider_value)
        slider.valueChanged.connect(context)  # self.context.setPencilSize)
        slider.valueChanged.connect(size_widget.set_value)

        signal.connect(slider.setValue)  # self.signals.updatePencilSize

        hbox.addWidget(size_label)
        hbox.addWidget(slider)
        hbox.addWidget(size_widget)
        vbox.setAlignment(QtCore.Qt.AlignTop)
        vbox.addLayout(hbox)
        widget.setLayout(vbox)

        return widget

    def create_pencil_widget(self):
        return self.create_size_widget(self.context.setPencilSize,
                                       self.signals.updatePencilSize,
                                       self.context.pencil_size)

    def create_join_widget(self):
        widget = QtGui.QWidget()
        widget.setObjectName("ToolProperties")
        widget.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)

        vbox = QtGui.QVBoxLayout()

        c1 = QtGui.QCheckBox("C1 continuity", self)
        c1.setChecked(self.context.join_type)
        c1.toggled.connect(self.context.set_join_type)

        vbox.setAlignment(QtCore.Qt.AlignTop)
        vbox.addWidget(c1)
        widget.setLayout(vbox)

        return widget

    def update_widget(self):
        self.setWidget(self.widgets[self.context.current_tool])


class CurveProperties(QtGui.QDockWidget):

    def __init__(self, title, context, signals, parent=None):

        super(CurveProperties, self).__init__(title, parent)

        self.context = context
        self.signals = signals
        self.parent = parent
        self.setAllowedAreas(Qt.RightDockWidgetArea)
        self.setFeatures(QtGui.QDockWidget.NoDockWidgetFeatures)

        self.setWidget(self.create_global_widget())

    def create_global_widget(self):

        widget = QtGui.QWidget()
        widget.setObjectName("Curve Properties")
        widget.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        vbox = QtGui.QVBoxLayout()

        hull = QtGui.QCheckBox("enable hull", self)
        hull.setChecked(self.context.hull_selection)
        hull.toggled.connect(self.context.set_hull_selection)
        self.signals.hull_selection.connect(hull.setChecked)

        vbox.setAlignment(QtCore.Qt.AlignTop)
        vbox.addWidget(hull)
        widget.setLayout(vbox)
        return widget


class CurveSelector(QtGui.QDockWidget):

    def __init__(self, title, context, signals, parent=None):

        super(CurveSelector, self).__init__(title, parent)

        self.context = context
        self.signals = signals
        self.parent = parent
        self.setAllowedAreas(Qt.RightDockWidgetArea)
        self.setFeatures(QtGui.QDockWidget.NoDockWidgetFeatures)
        self.max = 0
        self.setWidget(self.create_list_widget())

    def create_list_widget(self):
        widget = QtGui.QWidget()
        widget.setObjectName("curve selector")
        widget.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)

        vbox = QtGui.QVBoxLayout()
        hbox = QtGui.QHBoxLayout()

        curve_list = CurveList(self.context, self.signals)
        curve_list.itemClicked.connect(self.context.set_current_curve)
        self.signals.add_curves.connect(curve_list.add_item)

        button_add = QtGui.QPushButton('Add', self)
        button_add.clicked.connect(curve_list.add_item)

        button_rm = QtGui.QPushButton('Del', self)
        button_rm.clicked.connect(curve_list.remove_item)

        hbox.addWidget(button_add)
        hbox.addWidget(button_rm)
        vbox.addLayout(hbox)
        vbox.addWidget(curve_list)

        vbox.setAlignment(QtCore.Qt.AlignTop)
        widget.setLayout(vbox)
        return widget


class CurveList(QtGui.QListWidget):
    def __init__(self, context, signals):
        super(CurveList, self).__init__()
        self.context = context
        self.signals = signals
        self.add_item()
        self.signals.delete_curves.connect(self.delete_curve)

    def add_item(self):
        self.addItem(ListItem('curve {}'.format(len(self)), len(self)))

    def remove_item(self):
        for selected_item in self.selectedItems():
            self.takeItem(self.row(selected_item))
            self.context.curves_to_remove.append(selected_item.index)
        for i in range(self.count()):
            item = self.item(i)
            item.index = i
        if self.selectedItems():
            self.context.set_current_curve(self.selectedItems()[0])
            self.signals.delete_curves.emit()

    def delete_curve(self):
        for curve_idx in self.context.curves_to_remove:
            self.takeItem(curve_idx)


class ListItem(QtGui.QListWidgetItem):
    def __init__(self, name, index):
        super(ListItem, self).__init__(name)
        self.index = index
