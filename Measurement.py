# -*- coding: utf-8 -*-
from os.path import basename, splitext
import csv
import re

import numpy as np

class Measurement:
    def __init__(self, path): 
        # Avoid character \370 (octal) in file names
        self.path = path.replace("\xf8", "")

        self.name = splitext(basename(self.path))[0]
        self.measuring_point = re.match(".*(\d-\d)[_ ].*",
                                            self.name).groups()[0]
        # Has to be set somewhere where the Geometry object is in scope
        self.contact_dist = None
        self.temp_celcius = float(re.match(".*?(\d+\.\d+).*C",
                                            self.name).groups()[0])
        self.temp_kelvin = self.temp_celcius + 273.15 
        self.x = np.empty(0)    # in V
        self.y = np.empty(0)    # in mA

        with open(path, "r") as handle:
            handle.next()
            handle.next()
            for row in csv.reader(handle, delimiter="\t"):
                self.x = np.append(self.x, row[0])
                self.y = np.append(self.y, row[1])

        self.x = self.x.astype(np.float)
        self.y = self.y.astype(np.float)

        self.resist = None              # in kOhm
        self.contact_resist = None      # in kOhm
        self.film_resist = None         # in Ohm * cm

    def get_measured_values(self):
        return (self.x, self.y)

    def __repr__(self):
        return "{0}\t{1}\t{2}\t{3}".format(
            self.name, self.temp_celcius, self.measuring_point, self.resist)
