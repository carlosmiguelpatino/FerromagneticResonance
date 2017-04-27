import subprocess
import os
import numpy as np

def variableIteration(variableName, variableValues):
    # define the path to your oommf install
    path_oommf = '/home/carlosmiguelpatino/Software/oommf/oommf.tcl'

    # the name of the mif file
    mif_file = os.path.abspath('/home/carlosmiguelpatino/Documents/FerromagneticResonance/pulse.mif')

    # make our list of sizes that we will loop through
    # in nm as our mif file converts to metres.

    for variableValue in variableValues:
        oommf_string = 'tclsh {0} boxsi -parameters "{1} {2:.2g}" {3}'.format(path_oommf, variableName, variableValue, mif_file)
        output_file_name = 'pulse_{0}={1:.2g}'.format(variableName, variableValue)
        odt_to_csv = 'tclsh {0} odtcols -t csv <./data/{1}.odt >./data/{1}.csv'.format(path_oommf, output_file_name)
        subprocess.call(oommf_string, shell=True)
        subprocess.call(odt_to_csv, shell=True)
        subprocess.call('rm ./data/*.odt', shell=True)

import pandas as pd

def importData(filename):
    print('Processing file {0}'.format(filename))
    data1 = pd.read_csv(filename)
    data1 = data1[[' Oxs_TimeDriver::Simulation time (s)', ' Oxs_TimeDriver::mx', ' Oxs_TimeDriver::my', ' Oxs_TimeDriver::mz']]
    data1.columns = ['Time', 'mx', 'my', 'mz']
    subprocess.call('rm ./data/*.odt', shell=True)

    return data1

from scipy.fftpack import fft, fftfreq

def createFourierTransform(dataFrame):
    dt = data1['Time'][1] - data1['Time'][0]
    n = len(data1['mz'])

    mx_fft = fft(data1['mx'])/n
    my_fft = fft(data1['my'])/n
    mz_fft = fft(data1['mz'])/n
    freq = fftfreq(n, dt)

    return freq, mx_fft, my_fft, mz_fft

from scipy import signal
from scipy.optimize import curve_fit

def exponential(x, a, b):
    return a * np.exp(-b * x)

def analyzeRelaxationTime(data, magnetizationAxis):
    relaxInd = signal.find_peaks_cwt(data['mz'], np.arange(1,80))
    relaxation = []
    x_relaxation = []

    for index in relaxInd:
        x_relaxation.append(data['Time'][index])
        relaxation.append(data[magnetizationAxis][index])

    popt, pcov = curve_fit(exponential, x_decay, decay)

    return popt[1]
