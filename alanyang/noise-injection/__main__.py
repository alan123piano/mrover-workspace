import json
import math
import numpy as np
import os
import pandas as pd
import random

SIM_CONFIG_PATH = "../../config/filter/simConfig.json"

METERS_PER_EARTH_DEGREE = 111139 # 111,139 meters/degree

# TODO: Make everything into a class for easy export?
#       Check with proj lead to make sure make_sensor_drift is correct
#       Read in constants (ex. m/deg) from a config file

# REQUIRES: SIM_CONFIG_PATH leads to a valid .json with sigma values
# OUTPUT:   1d array corresponding to sigmas for [lat_deg, long_deg, speed, accel, bearing]
def read_sigma_array():
    with open(SIM_CONFIG_PATH) as f:
        data = json.load(f)
    return [data["gps_lat_stdev_meters"] / METERS_PER_EARTH_DEGREE,
            data["gps_long_stdev_meters"] / METERS_PER_EARTH_DEGREE,
            data["gps_vel_stdev_meters"],
            data["imu_accel_stdev_meters"],
            data["imu_bearing_stdev_degs"]]

# INPUT:    sigma_array - float array which has same length as a row of input
#               Each sigma_array value will apply Gaussian noise with that stdev
#               on its corresponding column of input
#           input_csv_path - points to .csv file
#               Contains clean measurements of [lat_deg, long_deg, speed, accel,
#               bearing]
#           output_csv_path - points to .csv file
# EFFECTS:  noisy [lat_deg, long_deg, speed, accel, bearing] written to file
#           pointed to by output_csv_path
def make_gaussian_noise(sigma_array, input_csv_path, output_csv_path):
    clean_signal = pd.read_csv(input_csv_path, header=None)
    noise = np.random.normal(0, sigma_array, clean_signal.shape)
    signal = clean_signal + noise
    signal.to_csv(output_csv_path, index=False, header=False)

# INPUT:    input_csv_path - points to .csv file with valid input
#               (should be a .csv with Gaussian noise already applied)
# EFFECTS:  output_csv_path written to with input_csv_path + drift injected
def make_sensor_drift(input_csv_path, output_csv_path):
    # Convert meters to lat/long deg/min
    # Research questions:
    #   Does drift affect just lat/long readings, or speed/accel too?
    #   Is bearing impacted?
    print("Hello world")

# This function will output stdev & mean of the Gaussian noise in output_csv_path relative
# to input_csv_path in order to verify that gaussian noise injection is working correctly.
# This function does not use Bessel's correction (https://en.wikipedia.org/wiki/Bessel%27s_correction)
# TODO: make code prettier (any Pythonic suggestions?)
def test_gaussian_stats(input_csv_path, output_csv_path):
    input = pd.read_csv(input_csv_path, header=None)
    output = pd.read_csv(output_csv_path, header=None)
    diff = output - input
    rows = diff.shape[0]
    cols = diff.shape[1]
    exp_mu_values = []
    exp_sigma_values = [] # experimental sigma values
    for col in range(0, cols):
        sum = 0
        for row in range(0, rows):
            sum += diff.at[row, col]
        avg = sum / rows
        sum_var = 0
        for row in range(0, rows):
            sum_var += pow(diff.at[row, col] - avg, 2)
        stdev = math.sqrt(sum_var / rows)
        exp_mu_values.append(avg)
        exp_sigma_values.append(stdev)
    return {"mu": exp_mu_values, "sigma": exp_sigma_values}

def test():
    sigma_array = read_sigma_array()
    print("Config sigma values:", sigma_array)
    make_gaussian_noise(sigma_array, "input.csv", "output.csv")
    test_stats = test_gaussian_stats("input.csv", "output.csv")
    print(test_stats["mu"])
    print(test_stats["sigma"])

test()
