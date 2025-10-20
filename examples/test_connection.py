#!/usr/bin/env python3
"""
Test connection to ClaudeMCP Remote Script
Verifies the Remote Script is loaded and responsive
"""

import socket
import json
import sys


def send_command(action, timeout=5, **params):
    """
    Send command to ClaudeMCP Remote Script

    Args:
        action: Action name (e.g., 'health_check', 'ping')
        timeout: Socket timeout in seconds
        **params: Additional parameters for the action

    Returns:
        dict: JSON response from Remote Script
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
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

        if response:
            return json.loads(response.decode('utf-8'))
        else:
            return {'ok': False, 'error': 'No response from server'}

    except socket.timeout:
        return {'ok': False, 'error': 'Connection timeout'}
    except ConnectionRefusedError:
        return {'ok': False, 'error': 'Connection refused - is Ableton running?'}
    except Exception as e:
        return {'ok': False, 'error': str(e)}


def main():
    print("=" * 80)
    print("ClaudeMCP Remote Script - Connection Test")
    print("=" * 80)
    print()

    # Test 1: Ping
    print("Test 1: Ping")
    result = send_command('ping')
    if result.get('ok'):
        print(f"  Status: OK")
        print(f"  Message: {result.get('message')}")
        print(f"  Script: {result.get('script')}")
    else:
        print(f"  Status: FAILED")
        print(f"  Error: {result.get('error')}")
        print()
        print("Troubleshooting:")
        print("1. Ensure Ableton Live is running")
        print("2. Verify ClaudeMCP_Remote is installed in Remote Scripts folder")
        print("3. Check Ableton Live log for errors")
        sys.exit(1)

    print()

    # Test 2: Health Check
    print("Test 2: Health Check")
    result = send_command('health_check')
    if result.get('ok'):
        print(f"  Status: OK")
        print(f"  Tool Count: {result.get('tool_count')}")
        print(f"  Ableton Version: {result.get('ableton_version')}")
        print(f"  Queue Size: {result.get('queue_size')}")
    else:
        print(f"  Status: FAILED")
        print(f"  Error: {result.get('error')}")
        sys.exit(1)

    print()

    # Test 3: Get Session Info
    print("Test 3: Get Session Info")
    result = send_command('get_session_info')
    if result.get('ok'):
        print(f"  Status: OK")
        print(f"  Tempo: {result.get('tempo')} BPM")
        print(f"  Time Signature: {result.get('time_signature_numerator')}/{result.get('time_signature_denominator')}")
        print(f"  Tracks: {result.get('num_tracks')}")
        print(f"  Scenes: {result.get('num_scenes')}")
        print(f"  Playing: {result.get('is_playing')}")
    else:
        print(f"  Status: FAILED")
        print(f"  Error: {result.get('error')}")
        sys.exit(1)

    print()
    print("=" * 80)
    print("All tests passed - ClaudeMCP Remote Script is operational")
    print("=" * 80)


if __name__ == '__main__':
    main()
