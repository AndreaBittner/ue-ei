#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui
from Plotter import Plotter


class MainWidget(QtGui.QWidget):
    def __init__(self):
        super(MainWidget, self).__init__()

        self.accel = Plotter('Beschleunigung', [0, 20])
        self.gyro = Plotter('Gyroskop', [0, 10], 'b')
        self.initialize()

    def initialize(self):
        vbox = QtGui.QVBoxLayout()
        vbox.setSpacing(20)
        vbox.setMargin(20)

        vbox.addWidget(self.accel)
        vbox.addStretch()
        vbox.addWidget(self.gyro)

        self.setLayout(vbox)

    def update_plots(self):
        self.accel.update()
        self.gyro.update()
