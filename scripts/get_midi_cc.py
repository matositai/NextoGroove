# coding: utf-8

import mido
import time
import sys

# --- CONFIGURATION ---
PORT_NAME_CONTAINS = 'Live'  # Must match MIDI port name from Ableton
MINIMUM_ACCEPTED_VELOCITY = 0
MAXIMUM_NOTE_SET_LENGTH = 9
BREAK_WHEN = 'MAX'  # 'MAX' or 'OFF'
TIMEOUT_SECONDS = 3  # Inactivity timeout
CLOCKS_PER_BEAT = 24  # MIDI Clock standard

# --- SEARCH FOR INPUT PORT ---
print("🔍 Searching for MIDI port containing:", PORT_NAME_CONTAINS)
input_ports = mido.get_input_names()

matching_ports = [p for p in input_ports if PORT_NAME_CONTAINS in p]

if not matching_ports:
    print(f"❌ No MIDI port found containing '{PORT_NAME_CONTAINS}'.")
    print("📋 Available ports:")
    for p in input_ports:
        print(f" - {p}")
    sys.exit(1)

# --- SELECT THE FIRST MATCHING PORT ---
VIRTUAL_PORT_NAME = matching_ports[0]
print(f"🎹 Listening on MIDI port: {VIRTUAL_PORT_NAME}")

# --- INIT NOTE AND CLOCK HANDLING ---
active_notes = list()
clock_count = 0
last_beat_time = time.time()
last_activity_time = time.time()

print(f"\n🎧 Waiting for MIDI notes and clock (will stop after {TIMEOUT_SECONDS} seconds of inactivity)...\n")

with mido.open_input(VIRTUAL_PORT_NAME) as inport:
    try:
        while True:
            # Timeout check
            if time.time() - last_activity_time > TIMEOUT_SECONDS:
                print(f"\n⏳ No input received in {TIMEOUT_SECONDS} seconds. Stopping...")
                print("✅ Collected notes:", active_notes)
                break

            msg = inport.poll()
            if msg:
                last_activity_time = time.time()

                # Handle MIDI Clock for BPM calculation
                if msg.type == 'clock':
                    clock_count += 1
                    if clock_count >= CLOCKS_PER_BEAT:
                        now = time.time()
                        elapsed = now - last_beat_time
                        bpm = int(60 / elapsed)
                        print(f"⏱️ BPM: {bpm}")
                        last_beat_time = now
                        clock_count = 0

                # Handle note input
                elif msg.type == "note_on" and msg.velocity > MINIMUM_ACCEPTED_VELOCITY:
                    active_notes.append(msg.note)
                    print(f"🎵 Note ON: {msg.note} (velocity: {msg.velocity}) | Total: {len(active_notes)}")

                elif msg.type == "note_off" and BREAK_WHEN == "OFF":
                    print(f"🛑 Note OFF: {msg.note}")
                    print("✅ Notes received before 'note_off':", active_notes)
                    break

            time.sleep(0.001)  # CPU-friendly polling

    except KeyboardInterrupt:
        print("\n⏹️ Listening stopped by user.")
