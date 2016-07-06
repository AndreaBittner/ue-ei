#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
from Plotter import Plotter
from Parser import Parser


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

        self.accel = Plotter('Beschleunigung', [-200, 200], 3, ['g', 'r', 'y'])
        self.gyro = Plotter('Gyroskop', [-20, 20], 3, ['g', 'r', 'y'])

        self.vbox.addWidget(self.accel)
        self.vbox.setAlignment(self.accel, QtCore.Qt.AlignTop)
        self.vbox.addWidget(self.gyro)
        self.vbox.setAlignment(self.gyro, QtCore.Qt.AlignTop)
        self.vbox.addStretch()

        self.widget.setLayout(self.vbox)

    def recalculate_width(self):
        # dynamische Anpassung der scrollArea Größe, damit der Graph schön dargestellt wird
        self.widget.setMinimumWidth(len(self.accel.data[0]) * 5 + 20)

    def display(self, filename):
        parser = Parser()
        data = parser.parse(filename)

        self.accel.set_data(data[0:3])
        self.gyro.set_data(data[3:6])

        self.recalculate_width()
