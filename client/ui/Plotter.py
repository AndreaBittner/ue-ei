#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
import pyqtgraph as pg
import numpy as np
from scipy.signal import savgol_filter
from scipy.interpolate import interp1d


class Plotter(pg.PlotWidget):
    def __init__(self, titel, value_range=[0, 20], lines=1, colour=['r']):
        super(Plotter, self).__init__()

        self.pointer = 0  # Pointer zum verschieben, der plots
        self.track = False  # zeigt an, ob die empfangenen Daten aufgezeichnet werden sollen

        self.getPlotItem().setTitle(titel)
        self.getPlotItem().setRange(yRange=value_range)
        self.getPlotItem().setMinimumWidth(950)
        self.getPlotItem().setMaximumHeight(320)
        self.getPlotItem().setMinimumHeight(320)
        self.setMinimumHeight(320)
        self.setMaximumHeight(320)
        self.showGrid(y=True)
        self.showGrid(x=True)
        self.lines = lines
        self.colour = colour

        # self.save = list()

        self.data = list()  # enthaelt 3 Listen von (x, y) Tupeln
        self.raw_data = list()  # damit man mehrmals Filter anwenden kann, ohne dass gefilterte Daten nochmal gefiltert werden

        # self.initialize(value_range)  # initialize wird nicht mehr benötigt, da keine random daten benötigt werden

    def initialize(self, value_range):
        # Random data zum Testen
        self.data = list()
        for i in range(0, self.lines):
            self.data.append(np.random.normal(value_range[-1] / 2, (value_range[-1] - value_range[0]) / 4, size=100))
            item = pg.PlotDataItem(self.data[i], pen=pg.mkPen(width=1.5, color=self.colour[i]))
            self.getPlotItem().addItem(item)

            # Listen für Speichern erstellen
            self.save.append(list())

    def set_height(self, value_range):
        self.getPlotItem().setRange(yRange=value_range)

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

    def save_data(self, filename):  # obsolete
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

    def set_data(self, data):
        del self.data[:]
        del self.raw_data[:]
        self.raw_data = list(data)
        self.data = list(data)

        self.redraw_plot()

    def redraw_plot(self):
        # alten Plot löschen
        for element in self.getPlotItem().listDataItems():
            self.getPlotItem().removeItem(element)

        # neue Daten in Plot eintragen
        for i in range(0, len(self.data)):
            print [x[0] for x in self.data[i]]
            print [y[1] for y in self.data[i]]
            item = pg.PlotDataItem(x=[x[0] for x in self.data[i]], y=[y[1] for y in self.data[i]], pen=pg.mkPen(width=1.5, color=self.colour[i]))
            self.getPlotItem().addItem(item)

    def no_filter(self):
        self.data = list(self.raw_data)

        self.redraw_plot()

    def savgol_filter(self, window=17, grade=5):
        data = list(self.raw_data)
        del self.data[:]

        for i in range(0, len(data)):  # sollten drei durchlaeufe sein
            x = np.arange(1.0, len(data[i]) + 1, 1.0)
            y = np.asarray([y[1] for y in data[i]])

            xx = np.linspace(x.min(), x.max(), len(data[i]))

            itp = interp1d(x, y, kind='linear')
            smoothed = savgol_filter(itp(xx), window, grade)
            # Um Filterung zu aendern muessen die hinteren beiden Zahlen angepasst werden
            # Savgol ist eine polynominale Regression; vorderer Wert ist Fenstergroesse, hinterer Grad des Polynoms
            # Je kleiner der vordere Wert und je groesser der hintere, desto naeher ist die Kurve am Original

            self.data.append(zip([x[0] for x in data[i]], smoothed))

        self.redraw_plot()

    def kalman_filter(self, q=1e-3, r=0.125):
        # sonst wird nur ein pointer zur selben liste erzeugt und data wird geloescht, wenn self.data geloescht wird
        data = list(self.raw_data)
        del self.data[:]

        for i in range(0, len(data)):
            n_iter = len(data[0])
            sz = (n_iter,)  # size of array
            z = [y[1] for y in data[i]]  # observed data

            # Ich weiss noch nicht genau, wie sich die aenderung der Parameter genau auf das resultierende Bild auswirkt
            # Die Parameter beeinflussen sich auch untereinander, das ist alles bisher sehr experimentell bei mir
            Q = q  # process noise  <-- Diese Variable kann angepasst werden um das Ergebnis zu aendern

            # allocate space for arrays
            x = np.zeros(sz)  # a posteri estimate of x
            p = np.zeros(sz)  # a posteri error estimate
            x_minus = np.zeros(sz)  # a priori estimate of x
            p_minus = np.zeros(sz)  # a priori error estimate
            k = np.zeros(sz)  # Kalman gain

            R = r  # estimate of measurement noise  <-- Diese Variable kann angepasst werden um das Ergebnis zu aendern

            # intial guesses
            x[0] = 0.0
            p[0] = 1.0  # estimated error

            for j in range(1, n_iter):
                # time update
                x_minus[j] = x[j - 1]
                p_minus[j] = p[j - 1] + Q

                # measurement update
                k[j] = p_minus[j] / (p_minus[j] + R)
                x[j] = x_minus[j] + k[j] * (z[j] - x_minus[j])
                p[j] = (1 - k[j]) * p_minus[j]

            self.data.append(zip([n[0] for n in data[i]], x))

        self.redraw_plot()
