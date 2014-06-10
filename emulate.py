#! /usr/bin/python
#------------------------------------------------------------------------------


#------------------------------------------------------------------------------

import pygame
from pygame.locals import *

import wc1

#------------------------------------------------------------------------------

_screen_x = 300
_screen_y = 300

_pushbutton = 0
_toggle = 1

#------------------------------------------------------------------------------

def inv(x):
    return ~x & 1

class plc:

    def __init__(self, fsm, key_map):
        pygame.init()
        self.screen = pygame.display.set_mode((_screen_x, _screen_y))
        pygame.display.set_caption('PLC')
        self.fsm = fsm
        self.key_map = key_map
        self.sv = fsm.s.isv
        self.iv = fsm.i.iiv
        self.ov = fsm.o.ov

    def __str__(self):
        return str(self.fsm)

    def get_inputs(self):
        """work out the current input vector"""
        for event in pygame.event.get():
            if event.type in (KEYDOWN, KEYUP):
                if self.key_map[event.key]:
                    (bit, switch) = self.key_map[event.key]
                    if event.type == KEYDOWN:
                        self.iv[bit] = inv(self.iv[bit])
                    elif event.type == KEYUP:
                        if switch == _pushbutton:
                            self.iv[bit] = inv(self.iv[bit])

    def run(self):
        self.get_inputs()
        # run the state machine
        self.sv, self.ov = self.fsm.fsm(self.sv, self.iv)

#------------------------------------------------------------------------------

def main():

    key_map = {
        K_f: (0, _pushbutton),
        K_w: (1, _pushbutton),
        K_s: (2, _pushbutton),
        K_x: (3, _toggle),
    }

    x = plc(wc1.wc1(), key_map)
    prev_state = None
    state_count = 0

    while True:
        state = str(x)
        if state != prev_state:
            prev_state = state
            state_count += 1
            print '%d: %s' % (state_count, state)
        x.run()

main()

#------------------------------------------------------------------------------

