import subprocess
import os
import numpy as np
# define the path to your oommf install
path_oommf = '/home/carlosmiguelpatino/Software/oommf/oommf.tcl'

# the name of the mif file
mif_file = os.path.abspath('/home/carlosmiguelpatino/Documents/FerromagneticResonance/pulse.mif')

# make our list of sizes that we will loop through
# in nm as our mif file converts to metres.
k1_values = [100, 200]

for k1 in k1_values:
    oommf_string = 'tclsh' + ' ' + path_oommf + \
    ' boxsi -parameters "K1_iter %s" %s' % \
     (k1, mif_file)
    print(oommf_string)
    output_file_name = 'pulse_K1='+str(k1)
    odt_to_csv = 'tclsh '+ path_oommf + ' odtcols -t csv <'+ output_file_name+ '.odt >' + output_file_name+ '.csv'
    subprocess.call(oommf_string, shell=True)
    subprocess.call(odt_to_csv, shell=True)
