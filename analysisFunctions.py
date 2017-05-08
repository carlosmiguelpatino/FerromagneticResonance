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

    if(type(data1['Time'][0]) == str):
        data1['Time'] = data1['Time'].str.strip()
        data1['mx'] = data1['mx'].str.strip()
        data1['my'] = data1['my'].str.strip()
        data1['mz'] = data1['mz'].str.strip()
        data1['Time'] = pd.to_numeric(data1['Time'], errors='coerce')
        data1['mx'] = pd.to_numeric(data1['mx'], errors='coerce')
        data1['my'] = pd.to_numeric(data1['my'], errors='coerce')
        data1['mz'] = pd.to_numeric(data1['mz'], errors='coerce')
        data1 = data1.dropna()

    return data1

from scipy.fftpack import fft, fftfreq

def createFourierTransform(dataFrame):
    dt = dataFrame['Time'][1] - dataFrame['Time'][0]
    n = len(dataFrame['mz'])

    mx_fft = abs(fft(dataFrame['mx']))/n
    my_fft = abs(fft(dataFrame['my']))/n
    mz_fft = abs(fft(dataFrame['mz']))/n
    freq = fftfreq(n, dt)


    mask = freq > 0
    freq = freq[mask]
    mx_fft = mx_fft[mask]
    my_fft = my_fft[mask]
    mz_fft = mz_fft[mask]

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

import matplotlib.pylab as plt
plt.style.use('ggplot')

def plotFourierTransforms(frequencies, fourierTransforms, plottedAxis, showSave):
    fig = plt.figure()
    for key in frequencies:
        plt.plot(frequencies[key], fourierTransforms[key], label=key, alpha=0.5)
    plt.title('{} Fourier Transform'.format(plottedAxis))
    plt.xlabel('Frequencies')
    plt.ylabel('Fourier Transform')
    plt.legend()
    if(showSave == 'show'):
        plt.show()
    if(showSave == 'save'):
        fig.savefig('{}FourierTransform.png'.format(plottedAxis), dpi=fig.dpi)

def plotMagnetizations(dataFrames, plottedAxis, showSave):
    fig = plt.figure()
    for key, data in dataFrames.items():
        plt.plot(data['Time'], data[plottedAxis], label = key, alpha=0.5)
    plt.title('{} vs Time'.format(plottedAxis))
    plt.xlabel('Time (s)')
    plt.ylabel('{}'.format(plottedAxis))
    plt.legend()
    if(showSave == 'show'):
        plt.show()
    if(showSave == 'save'):
        fig.savefig('{}.png'.format(plottedAxis), dpi=fig.dpi)
