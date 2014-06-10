# py_plc

Python code to help with PLC ladder logic programming.

## Motivation

PLC programming is typically specified with "ladder logic"- a diagramatic form
for boolean sum of products (DNF) equations.

Specifying these directly is tedious and error prone.

The PLC industry has not really caught up with the idea of programming in high level languages.
Industrial electricians understand wires and relays but not programming languages.

The host based tools can emulate the PLCs offline but still don't provide a real programming language for
logic specification.

This is code to bridge the gap between a high level, name based specification of the FSM
and a low level bit oriented specification in the PLC.

## How to use

Write an FSM in high level python (E.g. wc1.py).

emulate.py:
1) run the state machine using the keyboard for real time input
2) validate correct operation

logic.py:
1) apply the complete set of state and input bit vectors to the FSM
2) record the next state and output values
3) work out the minimised logic functions
4) display the result

