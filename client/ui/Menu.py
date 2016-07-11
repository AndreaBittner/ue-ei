#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
from Observer import Observer
from Presenter import Presenter
import os

class Menu(QtGui.QMenuBar):
    def __init__(self, parent_window):
        super(Menu, self).__init__()

        self.parent_window = parent_window
        self.initialize()

    def initialize(self):

        # Definiere mögliche Aktionen
        exit_action = QtGui.QAction(QtGui.QIcon('exit.png'), '&Verlassen', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Verlassen')
        exit_action.triggered.connect(QtGui.qApp.quit)

        save_action = QtGui.QAction(QtGui.QIcon('save.png'), '&Speichern', self)
        save_action.setShortcut('Ctrl+S')
        save_action.setStatusTip('Aufzeichnung Speichern')
        save_action.triggered.connect(self.save_file)

        open_action = QtGui.QAction(QtGui.QIcon('open.png'), u'&Öffnen', self)
        open_action.setShortcut('Ctrl+O')
        open_action.setStatusTip(u'Aufzeichnung öffnen')
        open_action.triggered.connect(self.open_file)

        test_connection_action = QtGui.QAction(QtGui.QIcon('test.png'), '&Verbindung testen', self)
        test_connection_action.setStatusTip(u'Verbindung zum Schüttgut testen')
        # TODO: test_connection_action.triggered.connect()

        observe_action = QtGui.QAction(QtGui.QIcon('observe.png'), '&Verbindungsdaten beobachten', self)
        observe_action.setStatusTip('Darstellung der momentan empfangenen Daten')
        observe_action.triggered.connect(self.observe)

        record_start_action = QtGui.QAction(QtGui.QIcon('start.png'), '&Aufzeichnung starten', self)
        record_start_action.setStatusTip('Aufzeichnung der Sensordaten starten')
        record_start_action.triggered.connect(self.start_record)

        record_stop_action = QtGui.QAction(QtGui.QIcon('stop.png'), '&Aufzeichnung stoppen', self)
        record_stop_action.setStatusTip('Aufzeichnung der Sensordaten stoppen')
        record_stop_action.triggered.connect(self.stop_record)

        merge_action = QtGui.QAction(QtGui.QIcon('merge.png'), '&Dateien kombinieren', self)
        merge_action.setStatusTip('Geteilte Daten zu Rundendaten zusammenfügen')
        merge_action.triggered.connect(self.merge_files)

        stats_action = QtGui.QAction(QtGui.QIcon('stats.png'), '&Testlaufinformationen anzeigen', self)
        stats_action.setStatusTip('Zusätzliche Informationen zum Testlauf anzeigen')
        stats_action.triggered.connect(self.show_stats)

        # einzelne Menus zur Leiste hinzufügen
        file_menu = self.addMenu('&Datei')
        extra_menu = self.addMenu('&Extra')
        # conn_menu = self.addMenu('&Verbindung')
        # record_menu = self.addMenu('&Aufzeichnung')

        # Menus Aktionen zuweisen
        # file_menu.addAction(save_action)
        file_menu.addAction(open_action)
        file_menu.insertSeparator(None)
        file_menu.addAction(exit_action)

        extra_menu.addAction(merge_action)
        extra_menu.addAction(stats_action)

        # conn_menu.addAction(test_connection_action)
        # conn_menu.addAction(observe_action)

        # record_menu.addAction(record_start_action)
        # record_menu.addAction(record_stop_action)

    @QtCore.pyqtSlot()
    def start_record(self):
        if type(self.parent_window.central_widget.currentWidget()) is Observer:
            self.parent_window.central_widget.currentWidget().start_record()
        else:
            message = QtGui.QMessageBox()
            message.addButton(message.Ok)
            message.setText(QtCore.QString(u'Sie müssen im Beobachtungsmodus sein, um Daten aufzeichnen zu können.'))
            message.setWindowTitle(QtCore.QString('Warnung'))
            message.exec_()

    @QtCore.pyqtSlot()
    def stop_record(self):
        if type(self.parent_window.central_widget.currentWidget()) is Observer:
            self.parent_window.central_widget.currentWidget().stop_record()

    @QtCore.pyqtSlot()
    def open_file(self):
        file_dialog = QtGui.QFileDialog()
        file_dialog.setDirectory(QtCore.QString(os.getcwd()))
        file_dialog.setAcceptMode(file_dialog.AcceptOpen)
        file_dialog.setFileMode(file_dialog.ExistingFile)
        file_dialog.setViewMode(file_dialog.List)
        filename = file_dialog.getOpenFileName(filter=QtCore.QString('*.txt'))

        if filename:
            self.parent_window.presenter.display(filename)

            # central_widget ändern
            # self.parentWindow.central_widget.removeWidget(self.parentWindow.observer)
            # self.parentWindow.central_widget.addWidget(self.parentWindow.presenter)

    @QtCore.pyqtSlot()
    def save_file(self):
        if type(self.parent_window.central_widget.currentWidget()) is Observer:
            file_dialog = QtGui.QFileDialog()
            file_dialog.setDirectory(QtCore.QString(os.getcwd()))
            file_dialog.setAcceptMode(file_dialog.AcceptSave)
            file_dialog.setFileMode(file_dialog.AnyFile)
            file_dialog.setViewMode(file_dialog.List)
            file_dialog.setDefaultSuffix(QtCore.QString('.csv'))  # funktioniert nicht
            filename = file_dialog.getSaveFileName(filter=QtCore.QString('*.csv'))

            if filename:
                # TODO: catch if file exists --> overwrite?
                # TODO: automatisch dateiendung setzen
                self.parent_window.central_widget.currentWidget().save_file(filename)

    @QtCore.pyqtSlot()
    def observe(self):
        if type(self.parent_window.central_widget.currentWidget()) is Presenter:
            self.parent_window.central_widget.removeWidget(self.parent_window.presenter)
            self.parent_window.central_widget.addWidget(self.parent_window.observer)

    @QtCore.pyqtSlot()
    def merge_files(self):
        directory_name = str(QtGui.QFileDialog.getExistingDirectory(self, 'Select Directory'))
        self.parent_window.presenter.merge_files(directory_name)

    @QtCore.pyqtSlot()
    def show_stats(self):
        self.parent_window.presenter.show_stats()