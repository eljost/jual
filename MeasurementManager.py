class MeasurementManager:
    def __init__(self):
        self.temp_dict = dict()
        self.dist_dict = dict()
        self.measurements = list()

        self.temp_keys = None
        self.dist_keys = None

    def add_measurement(self, meas):
        self.measurements.append(meas)

    def update(self):
        for meas in self.measurements:
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
