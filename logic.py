#! /opt/python3.4/bin/python3.4
#------------------------------------------------------------------------------

from pyeda.inter import *
import fsm

#------------------------------------------------------------------------------

def bin_tuple(x, n):
    l = []
    for bit in range(n):
        l.append(x & 1)
        x >>= 1
    l.reverse()
    return tuple(l)

def main():

    bits = fsm.state_bits + fsm.input_bits
    n = 1 << bits

    f0 = []
    f1 = []

    # run the state machine for all state and input combinations
    for i in range(n):
        v = (bin_tuple(i, bits))
        sv = v[0:fsm.state_bits]
        iv = v[fsm.state_bits:]
        next_sv = fsm.fsm(sv, iv)
        f0.append('%d' % next_sv[0])
        f1.append('%d' % next_sv[1])
        print('%s %s -> %s' % (sv, iv, next_sv))

    # setup the function value strings
    f0 = ''.join(f0)
    f1 = ''.join(f1)

    # setup the truth tables
    X = ttvars('x', bits)
    f0 = truthtable(X, f0)
    f1 = truthtable(X, f1)

    # minimise
    f0m, f1m = espresso_tts(f0, f1)

    # dump the minimised function strings in plc variable form
    m1_next = str(f0m)
    m2_next = str(f1m)

    # do the x[] -> plc name replace
    x2plc = ('i4','i3','i2','i1','m2','m1')
    for i in range(len(x2plc)):
        m1_next = m1_next.replace('x[%d]' % i, x2plc[i])
        m2_next = m2_next.replace('x[%d]' % i, x2plc[i])

    print('m1_next = %s' % m1_next)
    print('m2_next = %s' % m2_next)

main()


#------------------------------------------------------------------------------
