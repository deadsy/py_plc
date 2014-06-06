#! /opt/python3.4/bin/python3.4
#------------------------------------------------------------------------------

from pyeda.inter import *
import fsm

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

    for i in range(n):
        v = (bin_tuple(i, bits))
        sv = v[0:fsm.state_bits]
        iv = v[fsm.state_bits:]
        next_sv = fsm.fsm(sv, iv)
        f0.append('%d' % next_sv[0])
        f1.append('%d' % next_sv[1])
        print(sv, iv, next_sv)

    X = ttvars('x', bits)
    f0 = ''.join(f0)
    f1 = ''.join(f1)
    f0 = truthtable(X, f0)
    f1 = truthtable(X, f1)

    f0m, f1m = espresso_tts(f0, f1)

    print(f0m)
    print(f1m)






main()


#------------------------------------------------------------------------------
