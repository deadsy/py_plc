#! /usr/bin/python

import pygame
from pygame.locals import *
import sys

_screen_x = 640
_screen_y = 480

_pushbutton = 0
_toggle = 1

def inv(x):
    return ~x & 1

class plc:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((_screen_x, _screen_y))
        pygame.display.set_caption('PLC')

        # inputs
        self.not_full = 0
        self.from_well = 0
        self.from_sj = 0
        self.stop = 1

        # internal states
        self.m0 = 1
        self.m1 = 1
        self.m0_next = self.m0
        self.m1_next = self.m1

    def __str__(self):
        s = []
        s.append('(%s)' % ('full', 'fill_sj', 'fill_well', 'stopped')[(self.m0 * 2) + self.m1])
        s.append('inputs: not_full:%d from_well:%d from_sj:%d stop:%d' % (self.not_full, self.from_well, self.from_sj, self.stop))
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
                self.not_full = self.key_process(event, self.not_full, K_f, _pushbutton)
                self.from_well = self.key_process(event, self.from_well, K_w, _pushbutton)
                self.from_sj = self.key_process(event, self.from_sj, K_s, _pushbutton)
                self.stop = self.key_process(event, self.stop, K_x, _toggle)

        # PLC ladder logic

        # state = 00 = full
        if (inv(self.m0) & inv(self.m1)):
            if self.stop:
                self.m0_next = 1
                self.m1_next = 1
            if self.not_full:
                # the tank is not full
                if self.from_well:
                    # manual well switch -> fill from well
                    self.m0_next = 1
                    self.m1_next = 0
                elif self.from_sj:
                    # manual sj switch -> fill from sj
                    self.m0_next = 0
                    self.m1_next = 1

        # state = 01 = fill from sj
        if (inv(self.m0) & self.m1):
            if self.stop:
                self.m0_next = 1
                self.m1_next = 1
            elif inv(self.not_full):
                # the tank is full
                self.m0_next = 0
                self.m1_next = 0
            elif self.from_well:
                # manual well switch -> fill from well
                self.m0_next = 1
                self.m1_next = 0

        # state = 10 = fill from well
        if (self.m0 & inv(self.m1)):
            if self.stop:
                self.m0_next = 1
                self.m1_next = 1
            elif inv(self.not_full):
                # the tank is full
                self.m0_next = 0
                self.m1_next = 0
            elif self.from_sj:
                # manual sj switch -> fill from sj
                self.m0_next = 0
                self.m1_next = 1

        # state == 11 = stopped
        if (self.m0 & self.m1):
            if inv(self.stop):
                self.m0_next = 0
                self.m1_next = 0

        self.m0 = self.m0_next
        self.m1 = self.m1_next


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