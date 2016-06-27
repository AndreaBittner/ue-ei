#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
import pyqtgraph as pg
from Plotter import Plotter


class Presenter(QtGui.QScrollArea):
    def __init__(self):
        super(Presenter, self).__init__()
        self.initialize()

    def initialize(self):
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.setWidgetResizable(True)

        self.widget = QtGui.QWidget()
        self.setWidget(self.widget)

        self.vbox = QtGui.QVBoxLayout()
        self.vbox.setSpacing(15)

        self.accel = Plotter('Beschleunigung', [0, 20])
        self.gyro = Plotter('Gyroskop', [0, 10], 3, ['g', 'r', 'y'])

        self.vbox.addWidget(self.accel)
        self.vbox.setAlignment(self.accel, QtCore.Qt.AlignTop)
        self.vbox.addWidget(self.gyro)
        self.vbox.setAlignment(self.gyro, QtCore.Qt.AlignTop)
        self.vbox.addStretch()

        self.widget.setLayout(self.vbox)

    # TODO:
    def calculate_width(self):
        # dynamische Anpassung der scrollArea Größe, damit der Graph schön dargestellt wird
        pass

    def display(self, filename):
        self.accel.read_file_data(filename, [0])
        self.gyro.read_file_data(filename, [1, 2, 3])
