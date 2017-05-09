from analysisFunctions import variableIteration, importData, createFourierTransform, plotFourierTransforms, plotMagnetizations, plotFrequencyDependence

import seaborn
import numpy as np
import subprocess

variableName = 'xsize'
initial_value = 200e-9
end_value = 1e-6
n_points  = 5
variableValues = np.linspace(initial_value, end_value, n_points)

performSimulation = input('Simulate processes? [y/n]: ')

if performSimulation == 'y':
    print('Simulating {0} {1} value points from {2} to {3}'.format(n_points, variableName, initial_value, end_value))
    variableIteration(variableName, variableValues)


dataFrames = {}
frequencies = {}
mx_transfroms = {}
my_transfroms = {}
mz_transfroms = {}


for variableValue in variableValues:
    filename = './data/pulse_{0}={1:.2g}.csv'.format(variableName, variableValue)

    data = importData(filename)
    dataFrames[variableValue] = data

    freq, mx_fft, my_fft, mz_fft = createFourierTransform(data)

    frequencies[variableValue] = freq
    mx_transfroms[variableValue] = mx_fft
    my_transfroms[variableValue] = my_fft
    mz_transfroms[variableValue] = mz_fft

showSave = input('Show or save plots [show/save]: ')
# plotMagnetizations(dataFrames, 'mx', showSave)
# plotMagnetizations(dataFrames, 'my', showSave)
# plotMagnetizations(dataFrames, 'mz', showSave)
#
# plotFourierTransforms(frequencies, mx_transfroms, 'mx', showSave)
# plotFourierTransforms(frequencies, my_transfroms, 'my', showSave)
# plotFourierTransforms(frequencies, mz_transfroms, 'mz', showSave)

plotFrequencyDependence(frequencies, mz_transfroms, variableName, showSave)
