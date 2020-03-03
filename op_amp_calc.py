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

def expand_resistance(shorthand):
    if(len(shorthand) == 0):
        return -1
    mult = 1
    if shorthand[-1].lower() == 'm':
        mult = 1000000
        shorthand = shorthand[:-1]
    elif shorthand[-1].lower() == 'k':
        mult = 1000
        shorthand = shorthand[:-1]
    if not is_float(shorthand):
        return -1
    return float(shorthand)*mult

def get_float_or_nothing(message):
    i = input(message + '\n')
    while not is_float(i) and len(i) > 0:
        i = input('Invalid input. ' + message + '\n')
    if len(i) == 0:
        return None
    return float(i)

def get_nearest_gain_vals(vals, gain, inverting):
    nearest_gain = -1
    nearest_rf = -1
    nearest_rin = -1
    for rf in vals:
        for rin in vals:
            if inverting:
                this_gain = rf/rin
                if abs(this_gain - gain) < abs(gain - nearest_gain):
                    nearest_gain = this_gain
                    nearest_rf = rf
                    nearest_rin = rin
            else:
                this_gain = (1+rf/rin)
                if abs((this_gain) - gain) < abs(gain - nearest_gain):
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

    expanded_vals = list()
    for val in vals:
        expanded_val = expand_resistance(val)
        if(expanded_val == -1):
            print('Could not expand value and it will not be used:', val)
        else:
            expanded_vals.append(expanded_val)
    
    gain, rf, rin = get_nearest_gain_vals(expanded_vals, gain, inverting)
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
