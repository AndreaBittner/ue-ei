#!/usr/bin/python
# -*- coding: utf-8 -*-


class Testfile:
    def __init__(self, filename):
        self.name = filename
        self.max_values = [0, 0, 0, 0, 0, 0]
        self.min_values = [0, 0, 0, 0, 0, 0]
        self.time = 0
        self.data = []
