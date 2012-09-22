import os

from Measurement import Measurement

class MeasurementManager:
    def __init__(self, path, geometry):
        self.path = path
        self.geometry = geometry
        self.measurements = list()
        self.get_measurements()

        self.temp_dict = dict()
        self.dist_dict = dict()
        self.contact_resist_dict = dict()
        self.arrhenius_dict = dict()

        self.temp_keys = None
        self.dist_keys = None

        self.update()

    def update(self):
        for meas in self.measurements:
            meas.contact_dist = self.geometry.contact_dists[
                                                meas.measuring_point]
                                                            
            self.add_by_key(self.temp_dict, meas, meas.temp_celcius)
            self.add_by_key(self.dist_dict, meas, meas.contact_dist)

        self.temp_keys = sorted(self.temp_dict.keys())
        self.dist_keys = sorted(self.dist_dict.keys())

    def add_by_key(self, add_to_dict, meas, key):
        if key in add_to_dict:
            add_to_dict[key].append(meas)
        else:
            add_to_dict[key] = list((meas, ))

    def get_by_temp(self, temp):
        return self.temp_dict[temp]

    def get_by_dist(self, dist):
        return self.dist_dict[dist]

    def get_all(self):
        return self.measurements
    
    def list_measurements(self):
        measurements = list()
        for entry in os.listdir(self.path):
            if entry.endswith(".dat"):
                measurements.append(os.path.join(self.path, entry))

        return measurements

    def get_measurements(self):
        for meas_path in self.list_measurements():
            self.measurements.append(Measurement(meas_path))
