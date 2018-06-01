#!/usr/bin/env python
# coding: utf-8

import os
from functools import partial
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt

from canvas import Canvas
from palette import Palette

from tools import Tools, ToolProperties, CurveProperties, CurveSelector


class MainWindow(QtGui.QMainWindow):

    def __init__(self, context, signals):

        super(MainWindow, self).__init__()

        self.signals = signals
        self.context = context

        self.resize(800, 480)
        self.setWindowTitle("Bezier Editor")

        self.tools = QtGui.QActionGroup(self)

        self.menuBar = self.create_menu_bar()
        self.toolBar = self.create_tool_bar()
        self.create_dock_widgets()

        self.mainWidget = Canvas(context, signals, self)
        self.setCentralWidget(self.mainWidget)

        self.imagePosLabel = QtGui.QLabel()
        self.imagePosLabel.setObjectName("ImagePosLabel")

        self.signals.autoUpdateTool.connect(self.set_current_tool)

        self.show()

    def create_tool_bar_actions(self):
        tool_bar_actions = []

        for tool, value, shortcut in Tools.get_fields():
            a = QtGui.QAction(QtGui.QIcon(os.path.join("images", "icons", tool + ".png")),
                              tool + " (" + shortcut + ")", self.tools)
            a.setCheckable(True)
            a.setShortcut(shortcut)
            a.toggled.connect(partial(self.context.changeCurrentTool, index=value))
            tool_bar_actions.append(a)

        tool_bar_actions[self.context.current_tool].setChecked(True)

        return tool_bar_actions

    def create_tool_bar(self):
        tool_bar = QtGui.QToolBar()
        for i in self.create_tool_bar_actions():
            tool_bar.addAction(i)

        tool_bar.setMovable(False)
        tool_bar.setOrientation(Qt.Vertical)
        self.addToolBar(Qt.LeftToolBarArea, tool_bar)

        return tool_bar

    def create_file_actions(self):

        names = ["new", "open", "save", "saveas", "exit"]
        icons = ["document-new.png", "document-open.png", "document-save.png", "document-save-as.png",
                 "application-exit.png"]
        shortcuts = ['Ctrl+N', 'Ctrl+O', 'Ctrl+S', 'Ctrl+Shift+S', 'Ctrl+Q']
        connects = [self.new_file, self.open_file, self.save_file, self.save_file_as, self.close]

        file_actions = []

        for name, icon, shortcut, conn in zip(names, icons, shortcuts, connects):
            a = QtGui.QAction(QtGui.QIcon("images/" + icon), name, self)
            a.setShortcut(shortcut)
            a.triggered.connect(self.restore_focus)
            if conn != 0:
                a.triggered.connect(conn)
            file_actions.append(a)

        file_actions.insert(4, 0)

        return file_actions

    def create_menu_bar(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu("file")
        file_actions = self.create_file_actions()

        for i in file_actions:
            if i == 0:
                file_menu.addSeparator()
            else:
                file_menu.addAction(i)

        return menubar

    def create_dock_widgets(self):
        # Palette widget
        palette = QtGui.QDockWidget("palette", self)
        palette.setAllowedAreas(Qt.RightDockWidgetArea)
        palette.setFeatures(QtGui.QDockWidget.NoDockWidgetFeatures)
        palette.setWidget(Palette(self.context, self.signals))
        palette.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        self.addDockWidget(Qt.RightDockWidgetArea, palette)

        # Global properties
        curve_properties = CurveProperties("curve properties", self.context, self.signals)
        curve_properties.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.addDockWidget(Qt.RightDockWidgetArea, curve_properties)

        # Tool Properties widget
        tool_properties = ToolProperties("tool properties", self.context, self.signals)
        tool_properties.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        self.addDockWidget(Qt.RightDockWidgetArea, tool_properties)

        # Curves
        curve_selector = CurveSelector("curve selector", self.context, self.signals, self)
        curve_selector.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        self.addDockWidget(Qt.RightDockWidgetArea, curve_selector)

    def set_current_tool(self, index):
        self.tools.actions()[index].setChecked(True)
        self.signals.updateTool.emit(0)

    def new_file(self):
        pass

    def open_file(self):
        pass

    def save_file(self):
        pass

    def save_file_as(self):
        pass

    def restore_focus(self):
        self.releaseMouse()
        self.releaseKeyboard()
        QtCore.QCoreApplication.instance().restoreOverrideCursor()
