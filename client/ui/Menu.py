#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
from Observer import Observer
from Presenter import Presenter
import os

class Menu(QtGui.QMenuBar):
    def __init__(self, parentWindow):
        super(Menu, self).__init__()

        self.parentWindow = parentWindow
        self.initialize()

    def initialize(self):

        # Definiere mögliche Aktionen
        exitAction = QtGui.QAction(QtGui.QIcon('exit.png'), '&Verlassen', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Verlassen')
        exitAction.triggered.connect(QtGui.qApp.quit)

        saveAction = QtGui.QAction(QtGui.QIcon('save.png'), '&Speichern', self)
        saveAction.setShortcut('Ctrl+S')
        saveAction.setStatusTip('Aufzeichnung Speichern')
        saveAction.triggered.connect(self.save_file)

        openAction = QtGui.QAction(QtGui.QIcon('open.png'), u'&Öffnen', self)
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip(u'Aufzeichnung öffnen')
        openAction.triggered.connect(self.open_file)

        testConnectionAction = QtGui.QAction(QtGui.QIcon('test.png'), '&Verbindung testen', self)
        testConnectionAction.setStatusTip(u'Verbindung zum Schüttgut testen')
        # TODO: testConnectionAction.triggered.connect()

        observeAction = QtGui.QAction(QtGui.QIcon('observe.png'), '&Verbindungsdaten beobachten', self)
        observeAction.setStatusTip('Darstellung der momentan empfangenen Daten')
        observeAction.triggered.connect(self.observe)

        recordStartAction = QtGui.QAction(QtGui.QIcon('start.png'), '&Aufzeichnung starten', self)
        recordStartAction.setStatusTip('Aufzeichnung der Sensordaten starten')
        recordStartAction.triggered.connect(self.start_record)

        recordStopAction = QtGui.QAction(QtGui.QIcon('stop.png'), '&Aufzeichnung stoppen', self)
        recordStopAction.setStatusTip('Aufzeichnung der Sensordaten stoppen')
        recordStopAction.triggered.connect(self.stop_record)

        # einzelne Menus zur Leiste hinzufügen
        fileMenu = self.addMenu('&Datei')
        connMenu = self.addMenu('&Verbindung')
        recMenu = self.addMenu('&Aufzeichnung')

        # Menus Aktionen zuweisen
        fileMenu.addAction(saveAction)
        fileMenu.addAction(openAction)
        fileMenu.insertSeparator(None)
        fileMenu.addAction(exitAction)

        connMenu.addAction(testConnectionAction)
        connMenu.addAction(observeAction)

        recMenu.addAction(recordStartAction)
        recMenu.addAction(recordStopAction)

    @QtCore.pyqtSlot()
    def start_record(self):
        if type(self.parentWindow.central_widget.currentWidget()) is Observer:
            self.parentWindow.central_widget.currentWidget().start_record()
        else:
            message = QtGui.QMessageBox()
            message.addButton(message.Ok)
            message.setText(QtCore.QString(u'Sie müssen im Beobachtungsmodus sein, um Daten aufzeichnen zu können.'))
            message.setWindowTitle(QtCore.QString('Warnung'))
            message.exec_()

    @QtCore.pyqtSlot()
    def stop_record(self):
        if type(self.parentWindow.central_widget.currentWidget()) is Observer:
            self.parentWindow.central_widget.currentWidget().stop_record()

    @QtCore.pyqtSlot()
    def open_file(self):
        fileDialog = QtGui.QFileDialog()
        fileDialog.setDirectory(QtCore.QString(os.getcwd()))
        fileDialog.setAcceptMode(fileDialog.AcceptOpen)
        fileDialog.setFileMode(fileDialog.ExistingFile)
        fileDialog.setViewMode(fileDialog.List)
        filename = fileDialog.getOpenFileName(filter=QtCore.QString('*.csv'))

        if filename:
            self.parentWindow.presenter.display(filename)

            # central_widget ändern
            self.parentWindow.central_widget.removeWidget(self.parentWindow.observer)
            self.parentWindow.central_widget.addWidget(self.parentWindow.presenter)

    @QtCore.pyqtSlot()
    def save_file(self):
        if type(self.parentWindow.central_widget.currentWidget()) is Observer:
            fileDialog = QtGui.QFileDialog()
            fileDialog.setDirectory(QtCore.QString(os.getcwd()))
            fileDialog.setAcceptMode(fileDialog.AcceptSave)
            fileDialog.setFileMode(fileDialog.AnyFile)
            fileDialog.setViewMode(fileDialog.List)
            fileDialog.setDefaultSuffix(QtCore.QString('csv'))  # funktioniert nicht
            filename = fileDialog.getSaveFileName(filter=QtCore.QString('*.csv'))

            if filename:
                # TODO: catch if file exists --> overwrite?
                # TODO: automatisch dateiendung setzen
                self.parentWindow.central_widget.currentWidget().save_file(filename)

    @QtCore.pyqtSlot()
    def observe(self):
        if type(self.parentWindow.central_widget.currentWidget()) is Presenter:
            self.parentWindow.central_widget.removeWidget(self.parentWindow.presenter)
            self.parentWindow.central_widget.addWidget(self.parentWindow.observer)