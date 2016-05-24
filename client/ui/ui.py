#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import functools
from PyQt4 import QtGui
import pyqtgraph as pg
from MainWidget import MainWidget
from Menu import Menu


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.initialize()

    def initialize(self):
        menubar = Menu()
        self.mainWidget = MainWidget()
        self.setMenuBar(menubar)
        self.setCentralWidget(self.mainWidget)

        self.setGeometry(0, 0, 1000, 600)
        self.setWindowTitle('Tracker')
        self.show()


def update_plot(obj):
    obj.mainWidget.update_plots()


def main():
    app = QtGui.QApplication(sys.argv)

    ui = MainWindow()

    time_out = functools.partial(update_plot, obj=ui)

    timer = pg.QtCore.QTimer()
    timer.timeout.connect(time_out)  # Signal, welches gesendet wird
    timer.start(50)  # Frequenz mit der ein Timersignal gesendet werden soll

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
