# -*- coding: utf-8 -*-

from scipy import stats
from numpy import log, array, exp

from MeasurementManager import MeasurementManager
from Output import Output
from Geometry import Geometry

def linear_fit(x, y):
    (slope, intercept, r_val, p_val, std_err) = stats.linregress(x, y)

    return (slope, intercept, std_err)

def arrhenius_fit(temps, film_resists):
    # Boltzmann constant in eV/K
    boltzmann = 8.6173423e-5
    recipr_temps = 1 / temps
    ln_conducts = log(1 / array(film_resists))
    slope, intercept, std_err = linear_fit(recipr_temps, ln_conducts)
    actv_energy = -slope * boltzmann
    rate_const_0 = exp(intercept)

    return actv_energy, rate_const_0

def get_contact_resist(meas_list):
    x = [entry.contact_dist * 10 for entry in meas_list]
    y = [entry.resist for entry in meas_list]
    # The intercept is the resist at a contact distance = 0 
    slope, intercept, std_err = linear_fit(x, y)
    
    return intercept

def get_film_resist(meas, geometry):
    # in Ohm * cm
    return ((meas.resist - meas.contact_resist)
            * geometry.film_thickness * geometry.contact_length
            / meas.contact_dist * 1000) # because kOhm -> Ohm

def run(path, film_thickness):
    manager = MeasurementManager(path, Geometry(film_thickness))
       
    # Calculate the resist R from the U/I-Plot
    for meas in manager.get_all(): 
        x, y = meas.get_measured_values()
        slope, intercept, std_err = linear_fit(x, y)
        meas.resist = 1 / slope
    
    # Calculate the contact resists
    for temp in manager.temp_keys:
        manager.contact_resist_dict[temp] = get_contact_resist(
                                                manager.get_by_temp(temp))
    
    # Correct the resists with the contact resist and the geometry
    for meas in manager.get_all():
        temp_key = meas.temp_celcius
        meas.contact_resist = manager.contact_resist_dict[temp_key]
        meas.film_resist = get_film_resist(meas, manager.geometry)
    
    # Get activation energy and sigma_0 from an linearized Arrhenius plot
    for dist in manager.dist_keys:
        measurements = manager.get_by_dist(dist)
        film_resists = [meas.film_resist for meas in measurements]
        temps = array([meas.temp_kelvin for meas in measurements])
        actv_energy, sigma_0 = arrhenius_fit(temps, film_resists)
        manager.arrhenius_dict[dist] = (actv_energy, sigma_0)

    output = Output(path)
    output.summary(manager)

if __name__ == "__main__":
    path = raw_input("Enter path: ")
    film_thickness = raw_input("Enter film thickness: ")
    path = "./1-22-204-5/"
    film_thickness = 1.3043911743e-5
    run(path, film_thickness)
