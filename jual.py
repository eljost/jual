# -*- coding: utf-8 -*-
import os
import logging
from math import floor, ceil, exp

from scipy import stats
from pylab import plot, title, show, legend
from numpy import log, array

from Measurement import Measurement
from MeasurementManager import MeasurementManager

logging.basicConfig(level=logging.INFO)

def list_measurements(path):
    measurements = list()
    for entry in os.listdir(path):
        if entry.endswith(".dat"):
            measurements.append(os.path.join(path, entry))
            logging.debug("List measurement: {0}".format(entry))

    return measurements

def get_measurements(path):
    meas_list = list()
    for meas_path in list_measurements(path):
        meas = Measurement(meas_path)
        # Calculate the resist R from the U/I-Plot
        x, y = meas.get_measured_values()
        slope, intercept, std_err = linear_fit(x, y)
        meas.resist = 1 / slope
        meas_list.append(meas)

    meas_list = sorted(meas_list, cmp=sort_by_temperature)
    return meas_list

def linear_fit(x, y):
    (slope, intercept, r_val, p_val, std_err) = stats.linregress(x, y)
    logging.debug("Slope: {0} Intercept: {1} Std_error: {2}".format(
                                                slope, intercept, std_err))

    return (slope, intercept, std_err)

def arrhenius_fit(temps, rate_consts):
    # in eV/K
    boltzmann = 8.6173423e-5
    recipr_temps = 1 / temps
    ln_rate_consts = 1 / log(rate_consts)
    slope, intercept, std_err = linear_fit(recipr_temps, ln_rate_consts)
    actv_energy = -slope * boltzmann
    rate_const_0 = exp(intercept)

    return actv_energy, rate_const_0

def split_by_temperature(meas_list):
    temp_dict = dict()
    for meas in meas_list:
        key = meas.temp_celcius
        if key in temp_dict:
            temp_dict[key].append(meas)
        else:
            temp_dict[key] = list((meas, ))
    
    return temp_dict

def sort_by_temperature(x, y):
    temp_diff = x.temp_celcius - y.temp_celcius
    if temp_diff < 0:
        return -1
    elif temp_diff > 0:
        return 1
    else:
        return 0

def get_contact_resist(meas_list):
    x = [entry.contact_dist * 10 for entry in meas_list]
    y = [entry.resist for entry in meas_list]
    # The intercept is the resist at a contact distance = 0 
    slope, intercept, std_err = linear_fit(x, y)
    
    return intercept

if __name__ == "__main__":
    path = "./data/"
    path = raw_input("Enter data path: ")
    #path = "./1-22-204-5/"
    meas_list = get_measurements(path)
    manager = MeasurementManager()
    print "Berechnung der Widerstände"
    for meas in meas_list:
        manager.add_measurement(meas)
        print meas
    manager.update()
    temp_dict = split_by_temperature(meas_list)
    contact_resist_dict = dict()
    
    print "Berechnung der Kontaktwiderstände"
    for temp in manager.temp_keys:
        contact_resist_dict[temp] = get_contact_resist(
                                            manager.get_by_temp(temp))
        print "{0} °C\t{1}".format(temp, contact_resist_dict[temp])

    
    print "Berechnung der Schichtwiderstände in Ohm * cm"
    for meas in manager.get_all():
        temp_key = meas.temp_celcius
        meas.contact_resist = contact_resist_dict[temp_key]
        meas.calc_film_resist()
        print "{0}\t{1} °C\t{2}".format(meas.name, meas.temp_celcius,
                                            meas.film_resist)
    
    print "Arrhenius-Plots"
    for dist in manager.dist_keys:
        print "Contact distance: {0}".format(dist)
        # Ordered from lowest to highes temperature
        measurements = manager.get_by_dist(dist)
        film_resists = [meas.film_resist for meas in measurements]
        temps = array([meas.temp_kelvin for meas in measurements])
        actv_energy, sigma_0 = arrhenius_fit(temps, film_resists)
        print "Activation engery: {0}".format(actv_energy)
        print "Sigma_0: {0}".format(sigma_0)






