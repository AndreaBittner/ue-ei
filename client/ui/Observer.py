#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
from Plotter import Plotter


class Observer(QtGui.QWidget):
    def __init__(self):
        super(Observer, self).__init__()

        self.accel = Plotter('Beschleunigung', [0, 20])
        self.gyro = Plotter('Gyroskop', [0, 10], 3, ['b', 'r', 'y'])
        self.initialize()

    def initialize(self):
        vbox = QtGui.QVBoxLayout()
        vbox.setSpacing(15)

        vbox.addWidget(self.accel)
        vbox.setAlignment(self.accel, QtCore.Qt.AlignTop)
        vbox.addWidget(self.gyro)
        vbox.setAlignment(self.gyro, QtCore.Qt.AlignTop)
        vbox.addStretch()

        self.setLayout(vbox)

    def update_plots(self):
        self.accel.update()
        self.gyro.update()

    def start_record(self):
        self.accel.track = True
        self.gyro.track = True

    def stop_record(self):
        self.accel.track = False
        self.gyro.track = False

    def save_file(self, filename):
        self.accel.save_data(filename)
        self.gyro.save_data(filename)
