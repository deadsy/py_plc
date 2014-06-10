#! /opt/python3.4/bin/python3.4
#------------------------------------------------------------------------------

from pyeda.inter import *

import wc1

#------------------------------------------------------------------------------

def bin_tuple(x, n):
    l = []
    for bit in range(n):
        l.append(x & 1)
        x >>= 1
    l.reverse()
    return tuple(l)

def main():

    fsm = wc1.wc1()
    bits = fsm.s.n + fsm.i.n

    s_tt = [[] for i in range(fsm.s.n)]
    o_tt = [[] for i in range(fsm.o.n)]

    # run the state machine for all state and input combinations
    for i in range(1 << bits):
        v = bin_tuple(i, bits)
        # generate the state and input vector
        sv = v[0:fsm.s.n]
        iv = v[fsm.s.n:]
        # get the next state and output vector
        next_sv, ov = fsm.fsm(sv, iv)
        # store the next state
        for i in range(fsm.s.n):
            s_tt[i].append('%d' % next_sv[i])
        # store the output
        for i in range(fsm.o.n):
            o_tt[i].append('%d' % ov[i])
        #print('%s %s -> %s %s' % (sv, iv, next_sv, tuple(ov)))

    # setup the truth tables
    xvars = ttvars('x', bits)
    for i in range(fsm.s.n):
        s_tt[i] = truthtable(xvars, s_tt[i])
    for i in range(fsm.o.n):
        o_tt[i] = truthtable(xvars, o_tt[i])

    # minimise
    s_func = [espresso_tts(s_tt[i]) for i in range(fsm.s.n)]
    s_func = [x for (x,) in s_func]
    o_func = [espresso_tts(o_tt[i]) for i in range(fsm.o.n)]
    o_func = [x for (x,) in o_func]

    # stringify the functions
    s_func = [str(x) for x in s_func]
    o_func = [str(x) for x in o_func]

    # work out the x to plc name mapping
    x2plc = []
    for i in range(fsm.s.n):
        x2plc.append('m%d' % (i + 1))
    for i in range(fsm.i.n):
        x2plc.append('i%d' % (i + 1))
    x2plc.reverse()

    # apply the mapping
    for i in range(len(x2plc)):
        s_func = [x.replace('x[%d]' % i, x2plc[i]) for x in s_func]
        o_func = [x.replace('x[%d]' % i, x2plc[i]) for x in o_func]

    # display the equations in plc form
    for i in range(fsm.s.n):
        print('m%d_next = %s' % (i + 1, s_func[i]))
    for i in range(fsm.o.n):
        print('q%d = %s' % (i + 1, o_func[i]))

main()


#------------------------------------------------------------------------------
