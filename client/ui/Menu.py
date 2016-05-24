#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui


class Menu(QtGui.QMenuBar):
    def __init__(self):
        super(Menu, self).__init__()

        self.initialize()

    def initialize(self):
        # Definiere Menu Aktionen
        exitAction = QtGui.QAction(QtGui.QIcon('exit.png'), '&Verlassen', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Verlassen')
        exitAction.triggered.connect(QtGui.qApp.quit)

        saveAction = QtGui.QAction(QtGui.QIcon('save.png'), '&Speichern', self)
        saveAction.setShortcut('Ctrl+S')
        saveAction.setStatusTip('Aufzeichnung Speichern')
        # TODO: saveAction.triggered.connect()

        openAction = QtGui.QAction(QtGui.QIcon('open.png'), '&Öffnen', self)
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Aufzeichnung Öffnen')
        # TODO: saveAction.triggered.connect()

        testConnectionAction = QtGui.QAction(QtGui.QIcon('test.png'), '&Verbindung testen', self)
        testConnectionAction.setStatusTip('Verbindung zum Schüttgut testen')
        # TODO: testConnectionAction.triggered.connect()


        fileMenu = self.addMenu('&Datei')
        connMenu = self.addMenu('&Verbindung')

        fileMenu.addAction(saveAction)
        fileMenu.addAction(openAction)
        fileMenu.insertSeparator(None)
        fileMenu.addAction(exitAction)

        connMenu.addAction(testConnectionAction)
