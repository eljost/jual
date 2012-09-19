# -*- coding: utf-8 -*-
import os
import logging
from math import floor, ceil, exp

from scipy import stats
from pylab import plot, title, show, legend
from numpy import log, array

from MeasurementManager import MeasurementManager
from Output import Output

logging.basicConfig(level=logging.INFO)

def linear_fit(x, y):
    (slope, intercept, r_val, p_val, std_err) = stats.linregress(x, y)
    logging.debug("Slope: {0} Intercept: {1} Std_error: {2}".format(
                                                slope, intercept, std_err))

    return (slope, intercept, std_err)

def arrhenius_fit(temps, rate_consts):
    # in eV/K
    boltzmann = 8.6173423e-5
    recipr_temps = 1 / temps
    ln_rate_consts = log(1 / array(rate_consts))
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
    path = "./1-22-204-5/"
    manager = MeasurementManager(path)
       
    for meas in manager.get_all(): 
        # Calculate the resist R from the U/I-Plot
        x, y = meas.get_measured_values()
        slope, intercept, std_err = linear_fit(x, y)
        meas.resist = 1 / slope
    
    for temp in manager.temp_keys:
        manager.contact_resist_dict[temp] = get_contact_resist(
                                            manager.get_by_temp(temp))
    
    for meas in manager.get_all():
        temp_key = meas.temp_celcius
        meas.contact_resist = manager.contact_resist_dict[temp_key]
        meas.calc_film_resist()
    
    for dist in manager.dist_keys:
        measurements = manager.get_by_dist(dist)
        film_resists = [meas.film_resist for meas in measurements]
        temps = array([meas.temp_kelvin for meas in measurements])
        actv_energy, sigma_0 = arrhenius_fit(temps, film_resists)
        manager.arrhenius_dict[dist] = (actv_energy, sigma_0)

    output = Output(path)
    output.summary(manager)
