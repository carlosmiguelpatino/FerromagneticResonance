import subprocess
import os
import numpy as np

def k1Iteration(initial_value, end_value, n_points):
    # define the path to your oommf install
    path_oommf = '/home/carlosmiguelpatino/Software/oommf/oommf.tcl'

    # the name of the mif file
    mif_file = os.path.abspath('/home/carlosmiguelpatino/Documents/FerromagneticResonance/pulse.mif')

    # make our list of sizes that we will loop through
    # in nm as our mif file converts to metres.
    k1_values = np.linspace(initial_value, end_value, n_points)

    for k1 in k1_values:
        oommf_string = 'tclsh {0} boxsi -parameters "K1_iter {1:.0f}" {2}'.format(path_oommf, k1, mif_file)
        output_file_name = 'pulse_K1={0:.0f}'.format(k1)
        odt_to_csv = 'tclsh {0} odtcols -t csv <./data/{1}.odt >./data/{1}.csv'.format(path_oommf, output_file_name)
        subprocess.call(oommf_string, shell=True)
        subprocess.call(odt_to_csv, shell=True)
        subprocess.call('rm ./data/*.odt', shell=True)
