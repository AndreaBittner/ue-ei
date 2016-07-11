#!/usr/bin/python
# -*- coding: utf-8 -*-


class Testfile:
    def __init__(self, filename, max_values=[0, 0, 0, 0, 0, 0], min_values=[0, 0, 0, 0, 0, 0], time=0, data=[]):
        self.name = filename
        self.max_values = max_values
        self.min_values = min_values
        self.time = time
        self.data = data
