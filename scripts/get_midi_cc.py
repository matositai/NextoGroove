#!/usr/bin/env python
# coding: utf-8

import mido
import time

# --- CONFIGURATION ---
VIRTUAL_PORT_NAME = "fromLivePort 2"  # Adjust this to match your loopMIDI port
MINIMUM_ACCEPTED_VELOCITY = 0
MAXIMUM_NOTE_SET_LENGTH = 9
BREAK_WHEN = 'MAX' #MAX : for breaking when reaching max length
                   #OFF : for breaking when getting a note_off message

# --- LIST AVAILABLE OUTPUT PORTS ---
print("Available MIDI Output Ports:")
for name in mido.get_output_names():
    print(f" - {name}")

# --- OPEN PORT AND LISTEN ---
# Set to store active notes
active_notes = list()

print(f"\nListening for 9 MIDI notes from Ableton on port: {VIRTUAL_PORT_NAME}\n")

with mido.open_input() as inport:
    for msg in inport:
       # print(msg.type)
        if msg.type == "note_on" and msg.velocity > MINIMUM_ACCEPTED_VELOCITY:
            active_notes.append(msg.note)
            print(f"Note ON : {msg.note} | Total active notes: {len(active_notes)}")

            if len(active_notes) == MAXIMUM_NOTE_SET_LENGTH:
                print("Received Notes:", active_notes)
                if BREAK_WHEN == "MAX":
                    break
                #active_notes.clear()  #reset just in case for later
                
        if msg.type == "note_off" :
            print("Received Notes:", active_notes)
            if BREAK_WHEN == "OFF":
                break