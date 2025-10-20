#!/usr/bin/env python3
"""
Creative workflow example - Generative music composition
Demonstrates algorithmic music creation using ClaudeMCP Remote Script
"""

import socket
import json
import random
import time


def send_command(action, **params):
    """Send command to ClaudeMCP Remote Script"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(10)
    sock.connect(('127.0.0.1', 9004))

    command = {'action': action, **params}
    message = json.dumps(command) + '\n'
    sock.sendall(message.encode('utf-8'))

    response = b''
    while b'\n' not in response:
        chunk = sock.recv(4096)
        if not chunk:
            break
        response += chunk

    sock.close()
    return json.loads(response.decode('utf-8'))


def create_generative_bass(track_idx, scene_idx, scale_notes):
    """Generate random bass line following a musical scale"""
    notes = []
    time_pos = 0.0

    for i in range(16):  # 16 notes in 4 bars
        pitch = random.choice(scale_notes)
        duration = random.choice([0.25, 0.5, 0.75, 1.0])
        velocity = random.randint(80, 110)

        notes.append({
            "pitch": pitch,
            "start": time_pos,
            "duration": duration,
            "velocity": velocity
        })

        time_pos += 0.25

    send_command('add_notes',
                track_index=track_idx,
                scene_index=scene_idx,
                notes=notes)

    print(f"  Generated {len(notes)} bass notes")


def create_generative_melody(track_idx, scene_idx, scale_notes):
    """Generate random melody with rests"""
    notes = []
    time_pos = 0.0

    while time_pos < 4.0:  # 4 bars
        # Random rest probability
        if random.random() > 0.3:  # 70% chance of note
            pitch = random.choice(scale_notes) + 12  # Octave higher
            duration = random.choice([0.25, 0.5, 0.75])
            velocity = random.randint(60, 100)

            notes.append({
                "pitch": pitch,
                "start": time_pos,
                "duration": duration,
                "velocity": velocity
            })

        time_pos += 0.25

    send_command('add_notes',
                track_index=track_idx,
                scene_index=scene_idx,
                notes=notes)

    print(f"  Generated {len(notes)} melody notes")


def create_generative_drums(track_idx, scene_idx):
    """Generate simple drum pattern"""
    # Kick on beats 1 and 3
    kicks = [{"pitch": 36, "start": i, "duration": 0.5, "velocity": 100}
             for i in [0, 1, 2, 3]]

    # Snare on beats 2 and 4
    snares = [{"pitch": 38, "start": i, "duration": 0.5, "velocity": 90}
              for i in [1, 3]]

    # Hi-hats on every 8th note
    hihats = [{"pitch": 42, "start": i * 0.5, "duration": 0.25, "velocity": 70}
              for i in range(8)]

    all_notes = kicks + snares + hihats

    send_command('add_notes',
                track_index=track_idx,
                scene_index=scene_idx,
                notes=all_notes)

    print(f"  Generated {len(all_notes)} drum hits")


def main():
    print("=" * 80)
    print("ClaudeMCP - Generative Music Composition")
    print("=" * 80)
    print()

    # C Minor pentatonic scale (MIDI note numbers)
    c_minor_penta = [36, 39, 41, 43, 46]  # C, Eb, F, G, Bb

    # Setup session
    print("Session Setup")
    print("-" * 40)
    send_command('set_tempo', bpm=120)
    print("Set tempo to 120 BPM")

    send_command('set_time_signature', numerator=4, denominator=4)
    print("Set time signature to 4/4")
    print()

    # Create tracks
    print("Creating Tracks")
    print("-" * 40)

    result = send_command('create_midi_track', name='Drums')
    drums_idx = result['track_index']
    send_command('set_track_volume', track_index=drums_idx, volume=0.9)
    print(f"Created Drums track (index {drums_idx})")

    result = send_command('create_midi_track', name='Bass')
    bass_idx = result['track_index']
    send_command('set_track_volume', track_index=bass_idx, volume=0.8)
    send_command('set_track_pan', track_index=bass_idx, pan=-0.2)
    print(f"Created Bass track (index {bass_idx})")

    result = send_command('create_midi_track', name='Melody')
    melody_idx = result['track_index']
    send_command('set_track_volume', track_index=melody_idx, volume=0.7)
    send_command('set_track_pan', track_index=melody_idx, pan=0.3)
    print(f"Created Melody track (index {melody_idx})")
    print()

    # Create clips
    print("Creating Clips")
    print("-" * 40)

    for idx in [drums_idx, bass_idx, melody_idx]:
        send_command('create_midi_clip',
                    track_index=idx,
                    scene_index=0,
                    length=4.0)
        send_command('set_clip_looping',
                    track_index=idx,
                    scene_index=0,
                    looping=True)
    print("Created 4-bar looping clips on all tracks")
    print()

    # Generate content
    print("Generating Content")
    print("-" * 40)

    print("Drums:")
    create_generative_drums(drums_idx, 0)

    print("Bass:")
    create_generative_bass(bass_idx, 0, c_minor_penta)

    print("Melody:")
    create_generative_melody(melody_idx, 0, c_minor_penta)
    print()

    # Add effects
    print("Adding Effects")
    print("-" * 40)

    send_command('add_device', track_index=bass_idx, device_name='FilterDelay')
    print("Added FilterDelay to Bass")

    send_command('add_device', track_index=melody_idx, device_name='Reverb')
    print("Added Reverb to Melody")
    print()

    # Create scene
    print("Scene Management")
    print("-" * 40)
    result = send_command('create_scene', name='Generative Pattern 1')
    print(f"Created scene: {result['name']}")
    print()

    # Playback
    print("Playback")
    print("-" * 40)
    print("Launching scene...")
    send_command('launch_scene', scene_index=0)
    print("Playing for 8 seconds...")

    time.sleep(8)

    send_command('stop_all_clips')
    print("Stopped playback")
    print()

    # Summary
    print("=" * 80)
    print("Generative composition complete!")
    print()
    print("Created:")
    print("  - 3 MIDI tracks (Drums, Bass, Melody)")
    print("  - Algorithmic note generation in C Minor Pentatonic")
    print("  - Effects processing (FilterDelay, Reverb)")
    print("  - 4-bar looping patterns")
    print()
    print("Explore the session in Ableton Live to hear the results!")
    print("=" * 80)


if __name__ == '__main__':
    main()
