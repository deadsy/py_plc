#! /usr/bin/python
#------------------------------------------------------------------------------


#------------------------------------------------------------------------------

import pygame
from pygame.locals import *
import fsm

#------------------------------------------------------------------------------

_screen_x = 640
_screen_y = 480

_pushbutton = 0
_toggle = 1

#------------------------------------------------------------------------------

def inv(x):
    return ~x & 1

class plc:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((_screen_x, _screen_y))
        pygame.display.set_caption('PLC')

        self.sv = (1,1)
        self.iv = [0,0,0,1]
        self.ov = (0,0,0)

    def __str__(self):
        s = []
        s.append('(%s)' % fsm.state_str(self.sv))
        s.append('inputs: %s' % fsm.input_str(self.iv))
        s.append('outputs: %s' % fsm.output_str(self.ov))
        return ' '.join(s)

    def key_process(self, event, state, key, switch):
        if event.key != key:
            return state
        if event.type == KEYDOWN:
            return inv(state)
        elif event.type == KEYUP:
            if switch == _pushbutton:
                return inv(state)
            else:
                return state

    def run(self):

        for event in pygame.event.get():
            if event.type in (KEYDOWN, KEYUP):
                self.iv[0] = self.key_process(event, self.iv[0], K_f, _pushbutton)
                self.iv[1] = self.key_process(event, self.iv[1], K_w, _pushbutton)
                self.iv[2] = self.key_process(event, self.iv[2], K_s, _pushbutton)
                self.iv[3] = self.key_process(event, self.iv[3], K_x, _toggle)

        # PLC ladder logic
        self.sv, self.ov = fsm.fsm(self.sv, self.iv)

#------------------------------------------------------------------------------

def main():
    x = plc()
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

