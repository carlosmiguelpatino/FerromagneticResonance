from analysisFunctions import variableIteration, importData, createFourierTransform

import matplotlib.pylab as plt
import seaborn
import numpy as np

variableName = 'xsize'
initial_value = 200e-9
end_value = 1e-6
n_points  = 3
variableValues = np.linspace(initial_value, end_value, n_points)

print('Simulating {0} {1} value points from {2} to {3}'.format(n_points, variableName, initial_value, end_value))
variableIteration(variableName, variableValues)


for variableValue in variableValues:
    filename = './data/pulse_{0}={1:.0g}.csv'.format(variableName, variableValue)

    data = importData(filename)

    freq, mx_fft, my_fft, mz_fft = createFourierTransform(data)

    plt.plot(freq, mx_fft)
    plt.plot(freq, my_fft)
    plt.plot(freq, mz_fft)
    plt.show()
