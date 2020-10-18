import json
import numpy as np
import os
import pandas as pd
import random

CONFIG_PATH = "..\..\config"

""" for root, dirs, files in os.walk(CONFIG_PATH):
    print("root = ", root)
    print("dirs = ", dirs)
    print("files = ", files)
    print("Printing names in dirs")
    for name in dirs:
        print(name, " :: ", os.path.join(root, name))
    print("Printing names in files")
    for name in files:
        print(name, " :: ", os.path.join(root, name)) """

# INPUT:  clean [lat_deg, long_deg, speed, accel, bearing] in CSV format
# OUTPUT: noisy [lat_deg, long_deg, speed, accel, bearing] in CSV format
# Applies simple Gaussian noise < input.csv > output.csv
# TODO: derive mu and sigma values from config/filter/sim as input
#       use different mu/sigma values for each parameter
def gaussian_noise_simulator(mu, sigma):
    clean_signal = pd.read_csv("input.csv", header=None)
    noise = np.random.normal(mu, sigma, clean_signal.shape)
    signal = clean_signal + noise
    signal.to_csv("output.csv", index=False)

# INPUT:  [lat_deg, long_deg, speed, accel, bearing] with Gaussian noise in CSV format
# OUTPUT: [lat_deg, long_deg, speed, accel, bearing] with Gaussian noise & drift in CSV format
def drift_injection_simulator():
    # Convert meters to lat/long deg/min
    # Research questions:
    #   Does drift affect just lat/long readings, or speed/accel too?
    #   Is bearing impacted?
    print("Hello world")

def test():
    gaussian_noise_simulator([-100, 0, 100, 200, 300], [1, 1, 1, 1, 1])

test()
