#!/usr/bin/env python
"""
Example: Control CV Tools and Max for Live devices

This example demonstrates how to:
1. Detect Max for Live devices on tracks
2. Find CV Tools devices specifically
3. Control CV Tools parameters by name
4. Animate CV LFO parameters in real-time

Requirements:
- Ableton Live running with ClaudeMCP Remote Script installed
- CV Tools Pack installed (optional, but recommended)
- At least one track with a CV Tools device (e.g., CV LFO)
"""

import socket
import json
import time


class AbletonM4LController:
    """Helper class for controlling Max for Live and CV Tools devices"""

    def __init__(self, host='localhost', port=9004):
        self.host = host
        self.port = port

    def send(self, command):
        """Send command to Ableton via TCP socket"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.host, self.port))
        sock.sendall(json.dumps(command).encode() + b'\n')

        response = b''
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                break
            response += chunk
            if b'\n' in chunk:
                break

        sock.close()
        return json.loads(response.decode())

    def get_m4l_devices(self, track_index):
        """Get all Max for Live devices on track"""
        return self.send({
            "action": "get_m4l_devices",
            "track_index": track_index
        })

    def get_cv_tools_devices(self, track_index):
        """Get all CV Tools devices on track"""
        return self.send({
            "action": "get_cv_tools_devices",
            "track_index": track_index
        })

    def is_max_device(self, track_index, device_index):
        """Check if device is a Max for Live device"""
        return self.send({
            "action": "is_max_device",
            "track_index": track_index,
            "device_index": device_index
        })

    def set_device_param_by_name(self, track_index, device_index, param_name, value):
        """Set device parameter by name"""
        return self.send({
            "action": "set_device_param_by_name",
            "track_index": track_index,
            "device_index": device_index,
            "param_name": param_name,
            "value": value
        })

    def get_m4l_param_by_name(self, track_index, device_index, param_name):
        """Get M4L parameter value by name"""
        return self.send({
            "action": "get_m4l_param_by_name",
            "track_index": track_index,
            "device_index": device_index,
            "param_name": param_name
        })

    def get_device_parameters(self, track_index, device_index):
        """Get all parameters of a device"""
        return self.send({
            "action": "get_device_parameters",
            "track_index": track_index,
            "device_index": device_index
        })

    def find_device(self, track_index, device_name_contains):
        """Find device by partial name match"""
        result = self.send({
            "action": "get_track_devices",
            "track_index": track_index
        })

        if not result.get('ok'):
            return None

        for i, device in enumerate(result['devices']):
            if device_name_contains.lower() in device['name'].lower():
                return i
        return None


def main():
    """Main example execution"""
    print("CV Tools and Max for Live Control Example")
    print("=" * 50)

    controller = AbletonM4LController()

    # Test connection
    try:
        response = controller.send({"action": "ping"})
        if not response.get('ok'):
            print("ERROR: Could not connect to Ableton")
            return
        print("✓ Connected to Ableton Live\n")
    except Exception as e:
        print("ERROR: Could not connect to Ableton - is the Remote Script running?")
        print("Error:", str(e))
        return

    # Example 1: Find all M4L devices on track 0
    print("Example 1: Finding Max for Live devices on track 0...")
    m4l_result = controller.get_m4l_devices(0)

    if m4l_result.get('ok'):
        devices = m4l_result.get('devices', [])
        print("Found {} M4L device(s):".format(len(devices)))
        for device in devices:
            print("  - {} (type: {}, index: {})".format(
                device['name'],
                device['type'],
                device['index']
            ))
    else:
        print("Error:", m4l_result.get('error'))

    print()

    # Example 2: Find CV Tools devices specifically
    print("Example 2: Finding CV Tools devices on track 0...")
    cv_result = controller.get_cv_tools_devices(0)

    if cv_result.get('ok'):
        cv_devices = cv_result.get('cv_devices', [])
        if len(cv_devices) > 0:
            print("Found {} CV Tools device(s):".format(len(cv_devices)))
            for device in cv_devices:
                print("  - {} (index: {})".format(device['name'], device['index']))
        else:
            print("No CV Tools devices found on track 0")
            print("Tip: Add a CV LFO or other CV Tools device to track 0 to test this example")
    else:
        print("Error:", cv_result.get('error'))

    print()

    # Example 3: Control a CV LFO device (if present)
    print("Example 3: Controlling CV LFO device...")
    lfo_index = controller.find_device(0, "CV LFO")

    if lfo_index is not None:
        print("Found CV LFO at device index {}".format(lfo_index))

        # Verify it's a M4L device
        check = controller.is_max_device(0, lfo_index)
        if check.get('ok') and check.get('is_m4l'):
            print("✓ Confirmed as Max for Live device")
            print("  Class: {}".format(check.get('class_name')))

        # Get all parameters
        print("\nGetting LFO parameters...")
        params = controller.get_device_parameters(0, lfo_index)
        if params.get('ok'):
            print("LFO has {} parameters:".format(len(params.get('parameters', []))))
            for param in params.get('parameters', [])[:10]:  # Show first 10
                print("  - {}: {} (range: {} to {})".format(
                    param['name'],
                    param['value'],
                    param['min'],
                    param['max']
                ))

        # Animate LFO rate parameter
        print("\nAnimating LFO Rate parameter...")
        print("(Setting 10 different values over 5 seconds)")

        for i in range(10):
            rate = i / 10.0
            result = controller.set_device_param_by_name(0, lfo_index, "Rate", rate)

            if result.get('ok'):
                print("  Set Rate to {:.2f}".format(rate))
            else:
                # If "Rate" parameter doesn't exist, try other common LFO parameters
                print("  Note: 'Rate' parameter not found - trying 'Frequency'...")
                result = controller.set_device_param_by_name(0, lfo_index, "Frequency", rate)
                if result.get('ok'):
                    print("  Set Frequency to {:.2f}".format(rate))

            time.sleep(0.5)

        print("\n✓ Animation complete!")

    else:
        print("No CV LFO device found on track 0")
        print("Tip: Add a CV LFO device to track 0 to test parameter control")

    print()

    # Example 4: Get specific parameter by name
    print("Example 4: Get specific parameter value...")
    if lfo_index is not None:
        param_result = controller.get_m4l_param_by_name(0, lfo_index, "Rate")
        if param_result.get('ok'):
            print("Current Rate parameter:")
            print("  Value: {}".format(param_result.get('value')))
            print("  Range: {} to {}".format(param_result.get('min'), param_result.get('max')))
        else:
            print("Could not get Rate parameter:", param_result.get('error'))

    print("\n" + "=" * 50)
    print("Example complete!")
    print("\nTips for CV Tools:")
    print("- CV LFO: Control Rate, Shape, Depth parameters")
    print("- CV Shaper: Control Drive, Curve, Bias parameters")
    print("- CV Envelope Follower: Control Attack, Release, Gain")
    print("- Use set_device_param_by_name() for easy parameter access")


if __name__ == "__main__":
    main()
