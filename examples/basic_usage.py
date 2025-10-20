#!/usr/bin/env python3
"""
Basic usage examples for ClaudeMCP Remote Script
Demonstrates common operations with Ableton Live
"""

import socket
import json
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


def example_1_session_control():
    """Example 1: Control playback and tempo"""
    print("Example 1: Session Control")
    print("-" * 40)

    # Set tempo
    result = send_command('set_tempo', bpm=128)
    print(f"Set tempo to {result['bpm']} BPM")

    # Set time signature
    send_command('set_time_signature', numerator=4, denominator=4)
    print("Set time signature to 4/4")

    # Start playback
    send_command('start_playback')
    print("Started playback")

    time.sleep(2)

    # Stop playback
    send_command('stop_playback')
    print("Stopped playback")
    print()


def example_2_create_track():
    """Example 2: Create and configure a MIDI track"""
    print("Example 2: Track Management")
    print("-" * 40)

    # Create MIDI track
    result = send_command('create_midi_track', name='Bass')
    track_idx = result['track_index']
    print(f"Created track '{result['name']}' at index {track_idx}")

    # Set volume
    result = send_command('set_track_volume', track_index=track_idx, volume=0.8)
    print(f"Set volume to {result['volume']:.2f}")

    # Set pan
    result = send_command('set_track_pan', track_index=track_idx, pan=-0.3)
    print(f"Set pan to {result['pan']:.2f}")

    # Arm for recording
    send_command('arm_track', track_index=track_idx, armed=True)
    print("Armed track for recording")
    print()

    return track_idx


def example_3_create_clip(track_idx):
    """Example 3: Create MIDI clip and add notes"""
    print("Example 3: Clip Operations")
    print("-" * 40)

    # Create clip
    result = send_command('create_midi_clip',
                         track_index=track_idx,
                         scene_index=0,
                         length=4.0)
    print(f"Created {result['length']}-bar MIDI clip")

    # Add notes (simple kick drum pattern)
    notes = [
        {"pitch": 36, "start": 0.0, "duration": 0.5, "velocity": 100},
        {"pitch": 36, "start": 1.0, "duration": 0.5, "velocity": 90},
        {"pitch": 36, "start": 2.0, "duration": 0.5, "velocity": 100},
        {"pitch": 36, "start": 3.0, "duration": 0.5, "velocity": 90},
    ]
    send_command('add_notes',
                track_index=track_idx,
                scene_index=0,
                notes=notes)
    print(f"Added {len(notes)} notes (kick pattern)")

    # Set clip to loop
    send_command('set_clip_looping',
                track_index=track_idx,
                scene_index=0,
                looping=True)
    print("Enabled clip looping")

    # Launch clip
    send_command('launch_clip', track_index=track_idx, scene_index=0)
    print("Launched clip")
    print()


def example_4_device_control(track_idx):
    """Example 4: Add and control devices"""
    print("Example 4: Device Control")
    print("-" * 40)

    # Add device
    result = send_command('add_device',
                         track_index=track_idx,
                         device_name='Reverb')
    if result['ok']:
        print("Added Reverb device")

    # List devices
    result = send_command('get_track_devices', track_index=track_idx)
    print(f"Track has {result['count']} device(s):")
    for device in result['devices']:
        print(f"  - {device['name']}")
    print()


def example_5_scene_control():
    """Example 5: Scene management"""
    print("Example 5: Scene Operations")
    print("-" * 40)

    # Create scene
    result = send_command('create_scene', name='Verse')
    scene_idx = result['scene_index']
    print(f"Created scene '{result['name']}' at index {scene_idx}")

    # Launch scene
    send_command('launch_scene', scene_index=0)
    print("Launched scene 0")

    time.sleep(3)

    # Stop all clips
    send_command('stop_all_clips')
    print("Stopped all clips")
    print()


def main():
    print("=" * 80)
    print("ClaudeMCP Remote Script - Basic Usage Examples")
    print("=" * 80)
    print()

    try:
        # Run examples
        example_1_session_control()
        track_idx = example_2_create_track()
        example_3_create_clip(track_idx)
        example_4_device_control(track_idx)
        example_5_scene_control()

        print("=" * 80)
        print("All examples completed successfully")
        print("=" * 80)

    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
