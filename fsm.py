#------------------------------------------------------------------------------

def inv(x):
    return ~x & 1

#------------------------------------------------------------------------------

state_bits = 2

state = {
    'full': (0, 0),
    'fill_sj': (0, 1),
    'fill_well': (1, 0),
    'stopped': (1, 1),
}

def state_str(sv):
    for (name, vector) in state.items():
        if sv == vector:
            return name
    return None

#------------------------------------------------------------------------------

input_bits = 4

input_bit = {
    'not_full': 0,
    'start_well': 1,
    'start_sj': 2,
    'stop': 3,
}

# return 0/1 for the state of the named input in the input vector
def in1(iv, name):
    return iv[input_bit[name]] == 1

def in0(iv, name):
    return iv[input_bit[name]] == 0

def input_str(iv):
    s = []
    for (name, bit) in input_bit.items():
        s.append('%s:%d' % (name, iv[bit]))
    return ' '.join(s)

#------------------------------------------------------------------------------

output_bits = 3

output_bit = {
    'sj_pump': 0,
    'well_pump': 1,
    'chlorinator': 2,
}

def out0(ov, name):
    ov[output_bit[name]] = 0

def out1(ov, name):
    ov[output_bit[name]] = 1

def output_str(ov):
    s = []
    for (name, bit) in output_bit.items():
        s.append('%s:%d' % (name, ov[bit]))
    return ' '.join(s)

#------------------------------------------------------------------------------

def fsm(sv, iv):

    # defaults - everything off, no state chnage
    ov = [0,] * output_bits
    new_sv = sv

    # outputs
    if sv == state['fill_sj']:
        out1(ov, 'sj_pump')

    if sv == state['fill_well']:
        out1(ov, 'well_pump')
        out1(ov, 'chlorinator')

    # state changes

    if in1(iv, 'stop'):
        # stop has been pressed
        new_sv = state['stopped']

    elif sv == state['full']:
        if in1(iv, 'not_full'):
            # the tank is not full
            if in1(iv, 'start_well'):
                # manual well switch -> fill from well
                new_sv = state['fill_well']
            elif in1(iv, 'start_sj'):
                # manual sj switch -> fill from sj
                new_sv = state['fill_sj']

    elif sv == state['fill_sj']:
        if in0(iv, 'not_full'):
            # the tank is full
            new_sv = state['full']
        elif in1(iv, 'start_well'):
            # manual well switch -> fill from well
            new_sv = state['fill_well']

    elif sv == state['fill_well']:
        if in0(iv, 'not_full'):
            # the tank is full
            new_sv = state['full']
        elif in1(iv, 'start_sj'):
            # manual sj switch -> fill from sj
            new_sv = state['fill_sj']

    elif sv == state['stopped']:
        if in0(iv, 'stop'):
            # the tank is full
            new_sv = state['full']

    return new_sv, ov

#------------------------------------------------------------------------------
