from k1Iteration import k1Iteration

import pandas as pd
from scipy import signal
from scipy.optimize import curve_fit
import matplotlib.pylab as plt
import numpy as np


initial_value = -4500
end_value = -4500*1.2
n_points  = 15
print('Simulating {0} k1 value points from {1} to {2}'.format(n_points, initial_value, end_value))
k1Iteration(initial_value, end_value, n_points)

k1_values = np.linspace(initial_value, end_value, n_points)
decay_rates = []

def exponential(x, a, b):
    return a * np.exp(-b * x)

for k1 in k1_values:
    filename = 'pulse_K1={0:.0f}.csv'.format(k1)
    print('Processing file {0}'.format(filename))
    data = pd.read_csv(filename)
    data = data[[' Oxs_TimeDriver::Simulation time (s)', ' Oxs_TimeDriver::mz']]
    data.columns = ['Time', 'mz']

    #data['Time'] = data['Time'].str.strip()
    #data['mz'] = data['mz'].str.strip()
    #data['Time'] = pd.to_numeric(data['Time'], errors='coerce')
    #data['mz'] = pd.to_numeric(data['mz'], errors='coerce')
    data = data.dropna()

    decayind = signal.find_peaks_cwt(data['mz'], np.arange(1,80))
    decay = []
    x_decay = []
    for index in decayind:
        x_decay.append(data['Time'][index])
        decay.append(data['mz'][index])

    popt, pcov = curve_fit(exponential, x_decay, decay)

    x = np.linspace(0, 2e-9, 1000)
    y = exponential(np.array(x), *popt)
    plt.plot(x, y)
    plt.plot(data['Time'], data['mz'])
    plt.show()
    decay_rates.append(popt[1])

plt.plot(k1_values, decay_rates)
plt.show()
