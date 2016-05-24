#!/usr/bin/python
# -*- coding: utf-8 -*-

import pyqtgraph as pg
import numpy as np


class Plotter(pg.PlotWidget):
    def __init__(self, titel, values=[0, 20], colour='r'):
        super(Plotter, self).__init__()

        self.pointer = 0

        self.getPlotItem().setTitle(titel)
        self.getPlotItem().setRange(yRange=values)
        self.showGrid(y=True)

        self.initialize(values, colour)

    def initialize(self, valueRange, colour):
        # Random data zum Testen

        self.data = np.random.normal(valueRange[-1] / 2, (valueRange[-1] - valueRange[0]) / 4, size=100)
        self.curve = self.plot(self.data, pen=pg.mkPen(cosmetic=False, width=0.5, color=colour))

    def update(self):
        self.pointer += 1
        self.data = np.roll(self.data, -1)  # Roll data  Hack zum testen, ob er plottet

        # TODO: get data from external source and add to self.data (maybe push old data to saving array)

        self.curve.setData(self.data)
        self.curve.setPos(self.pointer, 0)
