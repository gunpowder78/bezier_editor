#!/usr/bin/env python
# coding: utf-8

import sys, os

from PyQt4 import QtGui

from main_window import MainWindow
from signals import Signals
from contex import Context


def readCSS(name):
    with open(name, 'r') as f:
        s = f.read()
    return s


if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)

    sys.setrecursionlimit(4096 * 4096)

    signals = Signals()
    context = Context(signals)

    mw = MainWindow(context, signals)
    mw.setStyleSheet(readCSS(os.path.join("themes", "algae", "style.css")))

    sys.exit(app.exec_())
