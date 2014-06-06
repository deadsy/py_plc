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

    m1 = []
    m2 = []
    q1 = []
    q2 = []
    q3 = []

    # run the state machine for all state and input combinations
    for i in range(n):
        v = (bin_tuple(i, bits))
        sv = v[0:fsm.state_bits]
        iv = v[fsm.state_bits:]
        next_sv, ov = fsm.fsm(sv, iv)
        m1.append('%d' % next_sv[0])
        m2.append('%d' % next_sv[1])
        q1.append('%d' % ov[0])
        q2.append('%d' % ov[1])
        q3.append('%d' % ov[2])
        print('%s %s -> %s' % (sv, iv, next_sv))

    # setup the function value strings
    m1 = ''.join(m1)
    m2 = ''.join(m2)

    # setup the truth tables
    X = ttvars('x', bits)
    m1 = truthtable(X, m1)
    m2 = truthtable(X, m2)
    q1 = truthtable(X, q1)
    q2 = truthtable(X, q2)
    q3 = truthtable(X, q3)



    # minimise
    m1_func, m2_func = espresso_tts(m1, m2)
    q1_func, q2_func, q3_func = espresso_tts(q1, q2, q3)

    # dump the minimised function strings in plc variable form
    m1_next = str(m1_func)
    m2_next = str(m2_func)

    q1_out = str(q1_func)
    q2_out = str(q2_func)
    q3_out = str(q3_func)

    # do the x[] -> plc name replace
    x2plc = ('i4','i3','i2','i1','m2','m1')
    for i in range(len(x2plc)):
        m1_next = m1_next.replace('x[%d]' % i, x2plc[i])
        m2_next = m2_next.replace('x[%d]' % i, x2plc[i])
        q1_out = q1_out.replace('x[%d]' % i, x2plc[i])
        q2_out = q2_out.replace('x[%d]' % i, x2plc[i])
        q3_out = q3_out.replace('x[%d]' % i, x2plc[i])

    print('m1_next = %s' % m1_next)
    print('m2_next = %s' % m2_next)
    print('q1_out = %s' % q1_out)
    print('q2_out = %s' % q2_out)
    print('q3_out = %s' % q3_out)

main()


#------------------------------------------------------------------------------
