# -*- coding: utf-8 -*-
from os.path import basename, splitext
import csv
import re

import numpy as np


temp = {"5-1" : 8.5e-2,"5-2" : 2.5e-2, "5-3" : 5.3e-2}

class Measurement:
    def __init__(self, path): 
        self.path = path.replace("\xf8", "")
        self.name = splitext(basename(self.path))[0]
        self.contact_dist = temp[re.match(".*(\d-\d)[_ ].*", self.name).groups()[0]]
        # 205
        #self.film_thickness = 1.2628e-5
        # 204
        self.film_thickness = 1.3043911e-5

        self.contact_length = 6e-1

        self.temp_celcius = self.get_temperature()
        self.temp_kelvin = self.temp_celcius + 273.15 
        # in V
        self.x = np.empty(0)
        # in mA
        self.y = np.empty(0)

        with open(path, "r") as handle:
            handle.next()
            handle.next()
            for row in csv.reader(handle, delimiter="\t"):
                self.x = np.append(self.x, row[0])
                self.y = np.append(self.y, row[1])

        self.x = self.x.astype(np.float)
        self.y = self.y.astype(np.float)

        self.resist = None
        self.contact_resist = None
        # in Ohm * cm
        self.film_resist = None

    def get_measured_values(self):
        return (self.x, self.y)

    def get_temperature(self):
        result = re.match(".*?(\d+\.\d+).*C", self.name)
        return float(result.groups()[0])

    def calc_film_resist(self):
        self.film_resist = ((self.resist - self.contact_resist) 
            * self.film_thickness * self.contact_length / self.contact_dist
            * 1000) # because kOhm -> Ohm

    def __repr__(self):
        return "{0}\t{1}\t{2}\t{3}".format(self.name, self.temp_celcius,
                                        self.contact_dist, self.resist)
