#------------------------------------------------------------------------------
"""

general classes for finite state machines

"""
#------------------------------------------------------------------------------

def bin_tuple(x, n):
    l = []
    for bit in range(n):
        l.append(x & 1)
        x >>= 1
    l.reverse()
    return tuple(l)

#------------------------------------------------------------------------------

class inputs:
    """map input names to an input bit vector"""

    def __init__(self, iiv, names):
        assert (len(iiv) == len(names)), 'initial vector length != names length'
        self.iiv = iiv
        self.iv = iiv
        self.names = names
        self.n = len(iiv)
        self.name2bit = dict(zip(names, range(self.n)))

    def set_iv(self, iv):
        self.iv = iv

    def set(self, iv, name):
        self.iv[self.name2bit[name]] = 1

    def clr(self, name):
        self.iv[self.name2bit[name]] = 0

    def is_set(self, name):
        return self.iv[self.name2bit[name]] != 0

    def is_clr(self, name):
        return self.iv[self.name2bit[name]] == 0

    def __str__(self):
        s = ['%s:%d' % (n, (0,1)[self.is_set(n)]) for n in self.names]
        return ' '.join(s)

#------------------------------------------------------------------------------

class outputs:
    """map output names to an output bit vector"""

    def __init__(self, names):
        self.names = names
        self.n = len(names)
        self.name2bit = dict(zip(names, range(self.n)))
        self.set_null()

    def set_null(self):
        self.ov = [0,] * self.n

    def set(self, name):
        self.ov[self.name2bit[name]] = 1

    def clr(self, name):
        self.ov[self.name2bit[name]] = 0

    def is_set(self, name):
        return self.ov[self.name2bit[name]] != 0

    def __str__(self):
        s = ['%s:%d' % (n, (0,1)[self.is_set(n)]) for n in self.names]
        return ' '.join(s)

#------------------------------------------------------------------------------

class state:
    """map state names to the state vector"""

    def __init__(self, isv, names):
        assert (len(names) <= (1 << len(isv))), 'not enough bits in the state vector'
        self.isv = isv
        self.sv = self.isv
        self.names = names
        self.n = len(isv)
        vset = [bin_tuple(i, self.n) for i in range(len(names))]
        self.name2vector = dict(zip(names, vset))
        self.vector2name = dict(zip(vset, names))

    def set_sv(self, sv):
        self.sv = sv

    def in_state(self, name):
        """return True if we are in the named state"""
        return self.vector2name[self.sv] == name

    def state(self, name):
        """return the bit vector for this state"""
        return self.name2vector[name]

    def __str__(self):
        return self.vector2name[self.sv]

#------------------------------------------------------------------------------
