# FerromagneticResonance
Resopository of code to analyze the behaviour of samples under the influence of magnetic field microwaves.

## Script Execution

To execute the Python script type in a command prompt `python ferromagneticResonance.py`

The script will ask the user whether to perform the OOMMF simulations corresponding to the values specified or use existing data files from previous simulations that match the values that want to be analyzed.

## Changing simulated variables and values

To change the variable that is going to take multiple values, the user must first make the variable a parameter in the OOMMF script. This can be done by:

+ Initialazing the variable as `Parameter variableName defaultValue`

+ Add a `[subst ]` to the object where the parameter is used to let know the OOMMF script that some values inside the object will have the values replaced.

    ```
    Specify Object [subst{
          Object definition
    }]```

+ Call the variable inside the object definition with preceding dollar sign: `$variableName`

Once the variable is set as a parameter in the .mif file:

1. Open the ferromagneticResonance.py file
2. Change the `variableName` line in the file to the name defined in the .mif file.
3. Specify the initial and end values.
4. Specify how many are required in the simulations between the initial and end values.

Once these parameters are set, the script will simulate all the variables values specified using the command `tclsh oommf_path boxsi -parameters "parameterName parameterValue" oommfScript.mif` 
