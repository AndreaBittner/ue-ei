#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
from Plotter import Plotter
from Parser import Parser
from Testfile import Testfile


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

        self.accel = Plotter('Beschleunigung', [-20, 20], 3, ['g', 'r', 'y'])
        self.gyro = Plotter('Gyroskop', [-360, 360], 3, ['g', 'r', 'y'])
        self.parser = Parser()
        self.current_file = Testfile('')

        self.vbox.addWidget(self.accel)
        self.vbox.setAlignment(self.accel, QtCore.Qt.AlignTop)
        self.vbox.addWidget(self.gyro)
        self.vbox.setAlignment(self.gyro, QtCore.Qt.AlignTop)
        self.vbox.addStretch()

        self.widget.setLayout(self.vbox)

    def recalculate_width(self):
        # dynamische Anpassung der scrollArea Größe, damit der Graph schön dargestellt wird
        self.widget.setMinimumWidth(len(self.accel.data[0]) * 8 + 20)

    def recalculate_height(self):
        accel_min = min(self.current_file.min_values[3:6])
        accel_max = max(self.current_file.max_values[3:6])
        gyro_min = min(self.current_file.min_values[0:3])
        gyro_max = max(self.current_file.max_values[0:3])
        self.accel.set_height([accel_min, accel_max])
        self.gyro.set_height([gyro_min, gyro_max])

    def display(self, filename):
        testfile = self.parser.parse(filename)
        self.current_file = testfile

        self.accel.set_data(testfile.data[3:6])
        self.gyro.set_data(testfile.data[0:3])

        self.recalculate_width()
        # self.recalculate_height()

    def merge_files(self, directory_name):
        self.parser.merge_files(directory_name)

    def show_stats(self):
        message = QtGui.QMessageBox()
        message.addButton(message.Ok)
        message.setText(QtCore.QString(
            u'Statistik für Datei {0}\t\t\t\n Laufzeit:\t{1}\t\t\nGyroskop:\n    roll:\t{2}, {3}\n    pitch:\t{4}, {5}\n    yaw:\t{6}, {7}\nBeschleunigung:\n    x:\t{8}, {9}\n    y:\t{10}, {11}\n    z:\t{12}, {13}'.format(
                unicode(self.current_file.name), unicode(self.current_file.time),
                unicode(self.current_file.min_values[0]), unicode(self.current_file.max_values[0]),
                unicode(self.current_file.min_values[1]), unicode(self.current_file.max_values[1]),
                unicode(self.current_file.min_values[2]), unicode(self.current_file.max_values[2]),
                unicode(self.current_file.min_values[3]), unicode(self.current_file.max_values[3]),
                unicode(self.current_file.min_values[4]), unicode(self.current_file.max_values[4]),
                unicode(self.current_file.min_values[5]), unicode(self.current_file.max_values[5]))))
        message.setWindowTitle(QtCore.QString('Statistik'))
        message.exec_()
