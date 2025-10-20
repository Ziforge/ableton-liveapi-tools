# Max for Live Integration

## Overview

This document describes how to interact with Max for Live (M4L) devices, including CV Tools, through the ClaudeMCP Remote Script.

## Max for Live Device Detection

Max for Live devices are identified by their `class_name`:
- **M4L Audio Effects**: `class_name == "MxDeviceAudioEffect"`
- **M4L MIDI Effects**: `class_name == "MxDeviceMidiEffect"`
- **M4L Instruments**: `class_name == "MxDeviceInstrument"`

## Accessing M4L Device Parameters

All M4L device parameters are accessible through the standard device API:

### Example: Controlling CV Tools LFO

```python
import socket
import json

def send_command(command):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', 9004))
    sock.sendall(json.dumps(command).encode() + b'\n')
    response = sock.recv(4096).decode()
    sock.close()
    return json.loads(response)

# 1. Find CV Tools device on track
response = send_command({
    "tool": "get_track_devices",
    "track_index": 0
})

# Look for CV LFO device
for i, device in enumerate(response['devices']):
    if 'CV' in device['name'] and 'LFO' in device['name']:
        device_index = i
        break

# 2. Get all parameters of the CV LFO
response = send_command({
    "tool": "get_device_parameters",
    "track_index": 0,
    "device_index": device_index
})

# 3. Set LFO rate parameter (find parameter by name)
for i, param in enumerate(response['parameters']):
    if param['name'] == 'Rate':
        send_command({
            "tool": "set_device_param",
            "track_index": 0,
            "device_index": device_index,
            "param_index": i,
            "value": 0.5  # Set to middle value
        })
```

## CV Tools Specific Devices

Common CV Tools devices and their purposes:

| Device | Purpose | Key Parameters |
|--------|---------|----------------|
| CV LFO | Generate CV modulation | Rate, Shape, Depth |
| CV Shaper | Shape CV signals | Drive, Curve, Bias |
| CV Envelope Follower | Audio to CV | Attack, Release, Gain |
| CV Instrument | CV to MIDI | Range, Quantize |
| CV Triggers | Generate triggers | Rate, Probability |
| CV Utility | CV routing/mixing | Mix, Offset, Scale |

## Proposed New Tools for M4L

### 1. Detect Max for Live Devices

```json
{
  "tool": "get_m4l_devices",
  "track_index": 0
}
```

Response:
```json
{
  "ok": true,
  "devices": [
    {
      "index": 2,
      "name": "CV LFO",
      "class_name": "MxDeviceAudioEffect",
      "type": "audio_effect",
      "is_m4l": true
    }
  ]
}
```

### 2. Get M4L Device Parameter by Name

```json
{
  "tool": "get_m4l_param_by_name",
  "track_index": 0,
  "device_index": 2,
  "param_name": "Rate"
}
```

Response:
```json
{
  "ok": true,
  "param_index": 5,
  "name": "Rate",
  "value": 0.5,
  "min": 0.0,
  "max": 1.0
}
```

### 3. Set M4L Parameter by Name

```json
{
  "tool": "set_m4l_param_by_name",
  "track_index": 0,
  "device_index": 2,
  "param_name": "Rate",
  "value": 0.75
}
```

### 4. Get CV Mappings (Live 11.1+)

```json
{
  "tool": "get_cv_mappings",
  "track_index": 0
}
```

Response:
```json
{
  "ok": true,
  "mappings": [
    {
      "source_device": "CV LFO",
      "source_param": "Output",
      "destination_device": "Operator",
      "destination_param": "Filter Freq",
      "amount": 0.5
    }
  ]
}
```

## Current Workaround

Until M4L-specific tools are added, you can interact with M4L devices using existing tools:

1. **List devices**: Use `get_track_devices` to find M4L devices
2. **Get parameters**: Use `get_device_parameters` to list all params
3. **Set parameters**: Use `set_device_param` with param index
4. **Parameter by name**: Use `get_device_parameter_by_name` (if available)

## Example: Complete CV LFO Control

```python
#!/usr/bin/env python
"""Control CV Tools LFO device"""

import socket
import json
import time

class AbletonController:
    def __init__(self, host='localhost', port=9004):
        self.host = host
        self.port = port

    def send(self, command):
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

    def find_device(self, track_index, device_name_contains):
        """Find device by partial name match"""
        result = self.send({
            "tool": "get_track_devices",
            "track_index": track_index
        })

        if not result.get('ok'):
            return None

        for i, device in enumerate(result['devices']):
            if device_name_contains.lower() in device['name'].lower():
                return i
        return None

    def set_device_param_by_name(self, track_index, device_index, param_name, value):
        """Set device parameter by name"""
        # Get all parameters
        params = self.send({
            "tool": "get_device_parameters",
            "track_index": track_index,
            "device_index": device_index
        })

        if not params.get('ok'):
            return params

        # Find parameter by name
        for i, param in enumerate(params['parameters']):
            if param['name'] == param_name:
                return self.send({
                    "tool": "set_device_param",
                    "track_index": track_index,
                    "device_index": device_index,
                    "param_index": i,
                    "value": value
                })

        return {"ok": False, "error": f"Parameter '{param_name}' not found"}

# Example usage
controller = AbletonController()

# Find CV LFO on track 0
lfo_index = controller.find_device(0, "CV LFO")

if lfo_index is not None:
    print(f"Found CV LFO at device index {lfo_index}")

    # Animate LFO rate
    for i in range(10):
        rate = i / 10.0
        result = controller.set_device_param_by_name(0, lfo_index, "Rate", rate)
        print(f"Set LFO rate to {rate}: {result}")
        time.sleep(0.5)
else:
    print("CV LFO not found on track 0")
```

## Implementation Notes

### Adding M4L-Specific Tools

To add proper M4L support, we would extend `liveapi_tools.py` with:

```python
def is_max_device(self, track_index, device_index):
    """Check if device is a Max for Live device"""
    try:
        track = self.song.tracks[track_index]
        device = track.devices[device_index]

        is_m4l = device.class_name in [
            'MxDeviceAudioEffect',
            'MxDeviceMidiEffect',
            'MxDeviceInstrument'
        ]

        return {
            "ok": True,
            "is_m4l": is_m4l,
            "class_name": str(device.class_name),
            "class_display_name": str(device.class_display_name)
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}

def get_m4l_devices(self, track_index):
    """Get all Max for Live devices on track"""
    try:
        track = self.song.tracks[track_index]
        m4l_devices = []

        for i, device in enumerate(track.devices):
            if device.class_name in ['MxDeviceAudioEffect', 'MxDeviceMidiEffect', 'MxDeviceInstrument']:
                m4l_devices.append({
                    "index": i,
                    "name": str(device.name),
                    "class_name": str(device.class_name),
                    "type": self._get_m4l_type(device.class_name),
                    "is_active": device.is_active
                })

        return {
            "ok": True,
            "devices": m4l_devices,
            "count": len(m4l_devices)
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}

def _get_m4l_type(self, class_name):
    """Get M4L device type from class name"""
    type_map = {
        'MxDeviceAudioEffect': 'audio_effect',
        'MxDeviceMidiEffect': 'midi_effect',
        'MxDeviceInstrument': 'instrument'
    }
    return type_map.get(class_name, 'unknown')

def set_device_param_by_name(self, track_index, device_index, param_name, value):
    """Set device parameter by name (useful for M4L devices)"""
    try:
        track = self.song.tracks[track_index]
        device = track.devices[device_index]

        # Find parameter by name
        for param in device.parameters:
            if str(param.name) == param_name:
                param.value = float(value)
                return {
                    "ok": True,
                    "param_name": param_name,
                    "value": float(param.value)
                }

        return {"ok": False, "error": f"Parameter '{param_name}' not found"}
    except Exception as e:
        return {"ok": False, "error": str(e)}
```

## Resources

- [Live Object Model (LOM) Documentation](https://docs.cycling74.com/max8/vignettes/live_object_model)
- [Max for Live API Reference](https://docs.cycling74.com/max8/vignettes/live_api_overview)
- [CV Tools Documentation](https://www.ableton.com/en/packs/cv-tools/)

## Next Steps

To fully support CV Tools and M4L devices:

1. Add M4L device detection tools
2. Add parameter-by-name accessors
3. Add CV modulation mapping tools (Live 11.1+)
4. Create M4L-specific example scripts
5. Document common CV Tools workflows
