#!/usr/bin/env python
# coding: utf-8


import mido
import time

# --- CONFIGURATION ---
BASE_NORM = 127
VIRTUAL_PORT_NAME = 'loopMIDI Port 1'  # Adjust this to match your loopMIDI port
CC_NUMBER = 74                      # knob/slider controller (can be any 0–127)
CC_VALUE = int(0.27 * BASE_NORM)    # Value to send (0–127)
print(CC_VALUE)
CHANNEL = 0                         # MIDI channel 1 (in MIDI, 0 = channel 1)

# --- LIST AVAILABLE OUTPUT PORTS ---
print("Available MIDI Output Ports:")
for name in mido.get_output_names():
    print(f" - {name}")

# --- SEND CONTROL CHANGE MESSAGE ---
with mido.open_output(VIRTUAL_PORT_NAME) as outport:
    msg = mido.Message('control_change', control=CC_NUMBER, value=CC_VALUE, channel=CHANNEL)
    outport.send(msg)
    print(f"Sent CC#{CC_NUMBER} with value {CC_VALUE} on channel {CHANNEL + 1}")

