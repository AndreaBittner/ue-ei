#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import functools
from PyQt4 import QtGui
from PyQt4 import QtCore
import pyqtgraph as pg
from Observer import Observer
from Presenter import Presenter
from Menu import Menu


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # self.observer = Observer()
        self.presenter = Presenter()

        self.central_widget = QtGui.QStackedWidget()
        self.central_widget.addWidget(self.presenter)

        self.menubar = Menu(self)
        self.initialize()

    def initialize(self):
        self.setMenuBar(self.menubar)

        self.setCentralWidget(self.central_widget)

        self.setGeometry(0, 0, 1000, 500)
        self.setMinimumWidth(1000)
        self.setMinimumHeight(710)
        self.setWindowTitle(u'Schüttgutbeobachter')
        self.show()


def update_plot(obj):
    if type(obj.central_widget.currentWidget()) is Observer:
        obj.central_widget.currentWidget().update_plots()


def main():
    app = QtGui.QApplication(sys.argv)

    ui = MainWindow()

    # time_out = functools.partial(update_plot, obj=ui)

    # timer = pg.QtCore.QTimer()
    # timer.timeout.connect(time_out)  # Signal, welches gesendet wird
    # timer.start(50)  # Frequenz mit der ein Timersignal gesendet werden soll

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
