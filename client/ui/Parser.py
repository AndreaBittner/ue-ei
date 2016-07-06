#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np


class Parser:

    def __init__(self):
        self.data = list()
        for i in range(0, 6):
            self.data.append(list())

    def parse(self, filename):
        f = open(filename, 'r')

        # teile string in Tupel
        for line in f:
            stripped = line.strip()
            if stripped[0] == "{":
                stripped = stripped[1:]
            if stripped[-1] == "}":
                stripped = stripped[:-1]
        raw_data = stripped.split("},{")

        f.close()

        id_set = False

        for i in range(0, len(raw_data)):
            irreg = raw_data[i].find("{")
            if irreg == -1:
                irreg = raw_data[i].find("}")
                if irreg == -1:
                    tup = raw_data[i].split(',')
                else:
                    tup = raw_data[i][:irreg].split(',')
            else:
                tup = raw_data[i][irreg + 1:].split(',')

            if not id_set and len(tup) == 8:
                ble_id = tup[-1]
                id_set = True

            # nur komplette Datensätze verwenden
            if len(tup) == 8 and ble_id == tup[-1]:
                for j in range(2, len(tup)):
                    self.data[j-2].append(np.float(tup[j]))

        return self.data
