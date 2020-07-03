# Op Amp Calculator

Calculates the resistors that should be used to most closely match a desired gain, based on a list of resistor values. I use this with a list of the available resistor values I have on hand so I can easily get close to the desired gain. An optional minimum and maximum resistor value can be set so that you don't use values that are too high or low to otherwise cause issues with your design.

The list of resistors should be in a file called resistor_values.txt. There is a file example_resistor_values.txt in the repo so you can see how it should be formatted. The list of resistor values does not need to be in order.

Run with:
```bash
python op_amp_calc.py
```
or
```bash
python3 op_amp_calc.py
```
