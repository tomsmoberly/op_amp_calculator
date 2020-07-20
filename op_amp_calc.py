#!/usr/bin/env python3

# Copyright 2020 Thomas S Moberly

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files 
# (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, 
# publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, 
# subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF 
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE 
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN 
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

def get_forced_yn(question):
    question = question + ' Please enter [y/n] without brackets.\n'
    i = input(question)
    while (i.lower() != 'y' and i.lower() != 'n'):
        i = input('Invalid response. Please try again.\n' + question)
    if(i.lower() == 'y'):
        return True
    else:
        return False

def is_float(float_string):
    try:
        float(float_string)
        return True
    except ValueError:
        return False

def compress_resistance(expanded):
    if(expanded >= 1000000):
        return str(expanded/1000000) + 'M'
    elif(expanded >= 1000):
        return str(expanded/1000) + 'K'
    return str(expanded)

def expand_resistance(shorthand, r_min, r_max):
    if(len(shorthand) == 0):
        return -2
    mult = 1
    if shorthand[-1].lower() == 'm':
        mult = 1000000
        shorthand = shorthand[:-1]
    elif shorthand[-1].lower() == 'k':
        mult = 1000
        shorthand = shorthand[:-1]
    if not is_float(shorthand):
        return -1
    else:
        # print("Min, val, max: ",r_min,(float(shorthand)*mult),r_max)
        if(r_min != -2):
            if((float(shorthand)*mult) < r_min):
                return -2
        if(r_max != -2):
            if((float(shorthand)*mult) > r_max):
                return -2
    return float(shorthand)*mult

def get_float_or_nothing(message):
    i = input(message + '\n')
    while not is_float(i) and len(i) > 0:
        i = input('Invalid input. ' + message + '\n')
    if len(i) == 0:
        return None
    return float(i)

def get_nearest_gain_vals(vals, gain, inverting, undershoot, overshoot):
    nearest_gain = -1
    nearest_rf = -1
    nearest_rin = -1
    for rf in vals:
        for rin in vals:
            if inverting:
                this_gain = rf/rin
                if abs(this_gain - gain) < abs(gain - nearest_gain):
                    if (not overshoot or this_gain > gain) and (not undershoot or this_gain < gain):
                        nearest_gain = this_gain
                        nearest_rf = rf
                        nearest_rin = rin
            else:
                this_gain = (1+rf/rin)
                if abs((this_gain) - gain) < abs(gain - nearest_gain):
                    if (not overshoot or this_gain > gain) and (not undershoot or this_gain < gain):
                        nearest_gain = this_gain
                        nearest_rf = rf
                        nearest_rin = rin
    return (nearest_gain, nearest_rf, nearest_rin)

def op_amp_gain_calc():
    try:
        with open('resistor_values.txt') as fp:
            vals = fp.read().splitlines()
    except FileNotFoundError:
        print('File resistor_values.txt was not found. Aborting.')
        return False
    
    i = input('What is the desired gain?\n')
    while not is_float(i):
        i = input('What is the desired gain?\n')
    gain = float(i)

    i = input('Is the amp [i]nverting or [n]on-inverting?\n')
    while (i.lower() != 'i' and i.lower() != 'n'):
        i = input('Invalid response. Please enter one of the letters in brackets to choose.\nIs the amp [i]nverting or [n]on-inverting?\n')
    inverting = True if i.lower() == 'i' else False

    r_min = input('If you would like to limit the MINIMUM resistor value, enter the min value now (example: 2.2k). Else leave line blank.\n')
    r_max = input('If you would like to limit the MAXIMUM resistor value, enter the max value now (example: 680k). Else leave line blank.\n')
    r_min = expand_resistance(r_min, -2, -2)
    r_max = expand_resistance(r_max, -2, -2)
    expanded_vals = list()
    for val in vals:
        expanded_val = expand_resistance(val, r_min, r_max)
        if(expanded_val < 0):
            if(expanded_val == -1):
                print('Could not expand value and it will not be used:', val)
        else:
            expanded_vals.append(expanded_val)
    
    overshoot = get_forced_yn('If an exact match is not possible, does the gain need to be LARGER than the target?')
    if not overshoot:
        undershoot = get_forced_yn('If an exact match is not possible, does the gain need to be SMALLER than the target?')
    gain, rf, rin = get_nearest_gain_vals(expanded_vals, gain, inverting, undershoot, overshoot)
    print('Nearest R_f =', compress_resistance(rf))
    print('Nearest R_in =', compress_resistance(rin))
    print('Nearest gain =', gain)
    
    i = input('Enter an input voltage to calculate the output voltage with this gain. Leave blank to skip.\n')
    while (not is_float(i) and len(i) > 0):
        i = input('Invalid input. Enter an input voltage to calculate the output voltage with this nearest gain. Leave blank to skip.\n')
    if(len(i) == 0):
        return True
    input_voltage = float(i)
    print('Output voltage =', input_voltage*gain)
    return True

def main():
    op_amp_gain_calc()

if __name__ == '__main__':
    main()
