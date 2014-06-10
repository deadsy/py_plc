#------------------------------------------------------------------------------
"""

well controller 1

"""
#------------------------------------------------------------------------------

import fsm

#------------------------------------------------------------------------------

i_names = ('not_full', 'start_well', 'start_sj', 'stop')
o_names = ('sj_pump', 'well_pump', 'chlorinator')
s_names = ('full', 'fill_sj', 'fill_well', 'stopped')

class wc1:

    def __init__(self):
        self.i = fsm.inputs([0,0,0,1], i_names)
        self.s = fsm.state((1,1), s_names)
        self.o = fsm.outputs(o_names)

    def __str__(self):
        s = []
        s.append('state(%s)' % self.s)
        s.append('input(%s)' % self.i)
        s.append('output(%s)' % self.o)
        return ' '.join(s)

    def fsm(self, sv, iv):
        self.s.set_sv(sv)
        self.i.set_iv(iv)

        # defaults - everything off, no state change
        self.o.set_null()
        new_sv = sv

        # outputs
        if self.s.in_state('fill_sj'):
            self.o.set('sj_pump')

        if self.s.in_state('fill_well'):
            self.o.set('well_pump')
            self.o.set('chlorinator')

        # state changes
        if self.i.is_set('stop'):
            # stop has been pressed
            new_sv = self.s.state('stopped')

        elif self.s.in_state('full'):
            if self.i.is_set('not_full'):
                # the tank is not full
                if self.i.is_set('start_well'):
                    # manual well switch -> fill from well
                    new_sv = self.s.state('fill_well')
                elif self.i.is_set('start_sj'):
                    # manual sj switch -> fill from sj
                    new_sv = self.s.state('fill_sj')

        elif self.s.in_state('fill_sj'):
            if self.i.is_clr('not_full'):
                # the tank is full
                new_sv = self.s.state('full')
            elif self.i.is_set('start_well'):
                # manual well switch -> fill from well
                new_sv = self.s.state('fill_well')

        elif self.s.in_state('fill_well'):
            if self.i.is_clr('not_full'):
                # the tank is full
                new_sv = self.s.state('full')
            elif self.i.is_set('start_sj'):
                # manual sj switch -> fill from sj
                new_sv = self.s.state('fill_sj')

        elif self.s.in_state('stopped'):
            if self.i.is_clr('stop'):
                # the tank is full
                new_sv = self.s.state('full')

        return new_sv, self.o.ov

#------------------------------------------------------------------------------
