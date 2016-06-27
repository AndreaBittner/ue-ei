#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
import pyqtgraph as pg
import numpy as np


class Plotter(pg.PlotWidget):
    def __init__(self, titel, valueRange=[0, 20], lines=1, colour=['r']):
        super(Plotter, self).__init__()

        self.pointer = 0  # Pointer zum verschieben, der plots
        self.track = False  # zeigt an, ob die empfangenen Daten aufgezeichnet werden sollen

        self.getPlotItem().setTitle(titel)
        self.getPlotItem().setRange(yRange=valueRange)
        self.getPlotItem().setMinimumWidth(950)
        self.getPlotItem().setMaximumHeight(200)
        self.getPlotItem().setMinimumHeight(200)
        self.setMinimumHeight(200)
        self.setMaximumHeight(200)
        self.showGrid(y=True)
        self.lines = lines
        self.colour = colour

        self.save = list()

        self.initialize(valueRange)

    def initialize(self, valueRange):
        # Random data zum Testen
        self.data = list()
        for i in range(0, self.lines):
            self.data.append(np.random.normal(valueRange[-1] / 2, (valueRange[-1] - valueRange[0]) / 4, size=100))
            item = pg.PlotDataItem(self.data[i], pen=pg.mkPen(width=1.5, color=self.colour[i]))
            self.getPlotItem().addItem(item)

            # Listen für Speichern erstellen
            self.save.append(list())

    def update(self):
        self.pointer += 1
        for i in range(0, self.lines):
            if self.track:
                self.save[i].append(str(self.data[i][0]))  # Elemente, die gespeichert werden sollen, save hinzufügen
            self.data[i] = np.roll(self.data[i], -1)

        # TODO: get data from external source and add to self.data (maybe push old data to saving array)

        number = 0
        for element in self.getPlotItem().listDataItems():
            element.setData(self.data[number])
            element.setPos(self.pointer, 0)
            number += 1

    def save_data(self, filename):
        if len(self.save[0]) > 0:  # falls es etwas zu speichern gibt
            f = open(filename, 'a')
            for i in range(0, self.lines):
                string = ','.join(self.save[i])
                string += '\n'
                f.write(string)
                # del self.save[i][:]
            f.close()

            # array leeren für neue Aufzeichnung
            for i in range(0, self.lines):
                del self.save[i][:]

        else:  # sonst gib Fehler aus
            message = QtGui.QMessageBox()
            message.addButton(message.Ok)
            message.setText(QtCore.QString(u'Es wurden keine aufgezeichneten Daten gefunden. Speichern abgebrochen'))
            message.setWindowTitle(QtCore.QString('Fehler'))
            message.exec_()

    def read_file_data(self, filename, lines):

        f = open(filename, 'r')

        # nur um sicherzugehen, dass alle alten Daten gelöscht sind
        del self.data[:]

        for i, line in enumerate(f):
            if i in lines:
                self.data.append(np.fromstring(line, dtype=float, sep=','))
        f.close()

        # alten Plot löschen
        for element in self.getPlotItem().listDataItems():
            self.getPlotItem().removeItem(element)

        # neue Daten in Plot eintragen
        for i in range(0, self.lines):
            item = pg.PlotDataItem(self.data[i], pen=pg.mkPen(width=1.5, color=self.colour[i]))
            self.getPlotItem().addItem(item)

