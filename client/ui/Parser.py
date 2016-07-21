#!/usr/bin/python
# -*- coding: utf-8 -*-

from Testfile import Testfile
import numpy as np
from os import remove
from os import walk
from os import path
import re


class Parser:
    def __init__(self):
        pass

    def parse(self, filename):
        test = Testfile(filename)

        f = open(filename, 'r')

        if f:
            # teile string in Tupel
            for line in f:
                stripped = line[line.find('{') + 1:line.rfind('}')]
            raw_data = stripped.split('},{')

            f.close()

            id_set = False
            for i in range(0, 6):
                test.data.append(list())

            # abfangen, wenn }/{ in Daten auftaucht
            for i in range(0, len(raw_data)):
                irreg = raw_data[i].find('{')
                if irreg == -1:
                    irreg = raw_data[i].find('}')
                    if irreg == -1:
                        tup = raw_data[i].split(',')
                    else:
                        tup = raw_data[i][:irreg].split(',')
                else:
                    tup = raw_data[i][irreg + 1:].split(',')

                if not id_set and len(tup) == 9:
                    ble_id = tup[-1]
                    id_set = True

                # nur komplette Datensätze verwenden
                if len(tup) == 9 and ble_id == tup[-1]:
                    # if len(tup) == 8:
                    for j in range(2, len(tup) - 1):
                        test.data[j - 2].append((int(tup[1]), np.float(tup[j])))

            # Statistikwerte hinzufuegen
            for i in range(0, len(test.data)):
                test.max_values[i] = max(test.data[i][1])
                test.min_values[i] = min(test.data[i][1])
            test.time = int(raw_data[-1].split(',')[1]) - int(raw_data[0].split(',')[1])

        return test

    def merge_files(self, directory_name):
        f = []
        for (dirpath, dirnames, filenames) in walk(directory_name):
            f.extend(filenames)
            break

        # alte testdateien loeschen, um verdopplung zu vermeiden
        for element in f:
            m = re.match(r'[0-9]*_data_test_[0-9]+\.txt', element)
            if m:
                remove(path.join(directory_name, element))

        # alphabetisch sortieren um zusammenfuegen zu vereinfachen
        f = sorted(f)

        run = 1
        for element in f:
            m = re.match(r'([0-9]*)_[0-9]*_data_([0-9]*)-([0-9]*)\.txt', element)
            if m and m.groups()[1] == '0':
                new_file_name = m.groups()[0] + '_data_test_' + str(run) + '.txt'
                new_path = path.join(directory_name, new_file_name)
                run += 1
            new_file = open(new_path, 'a')
            current_file = open(path.join(directory_name, element), 'r')
            for line in current_file:
                # unvollstaendige Datensaetze bereinigen
                data = line[line.find('{'):line.rfind('}') + 1]
                new_file.write(data)
            current_file.close()
            new_file.close()