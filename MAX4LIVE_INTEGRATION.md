# Max for Live Integration

## Overview

This document describes how to interact with Max for Live (M4L) devices, including CV Tools, through the ClaudeMCP Remote Script.

**The Remote Script includes 5 M4L-specific tools** that provide simplified access to Max for Live devices using parameter names instead of indices.

## How It Works: Dynamic Parameter Discovery

**Important:** The M4L implementation is **generic and future-proof** - it works with ANY Max for Live device without hardcoded parameter knowledge.

### No Hardcoded Device Database Required

The implementation uses **runtime introspection** to discover devices and parameters dynamically:

✅ **Works with ANY M4L device:**
- Built-in Ableton M4L devices (CV LFO, CV Shaper, Envelope Follower, etc.)
- Third-party M4L devices from Max for Live packs
- Custom user-created M4L devices
- Future M4L devices Ableton adds in updates

✅ **Only hardcoded knowledge:**
- 3 M4L device class names from LiveAPI spec:
  - `MxDeviceAudioEffect` - M4L audio effects
  - `MxDeviceMidiEffect` - M4L MIDI effects
  - `MxDeviceInstrument` - M4L instruments

✅ **Parameter discovery:**
- Uses `device.parameters` to enumerate all parameters at runtime
- User/client provides parameter names (e.g., "Rate", "Depth", "Attack")
- No maintenance needed when new M4L devices are released

### Example: How set_device_param_by_name Works

```python
def set_device_param_by_name(self, track_index, device_index, param_name, value):
    """Set device parameter by name (useful for M4L devices)"""
    device = track.devices[device_index]

    # Runtime discovery - iterate through ALL parameters
    for i, param in enumerate(device.parameters):
        if str(param.name) == param_name:  # User provides the name
            param.value = float(value)
            return {"ok": True, "param_name": param_name, "value": float(param.value)}

    return {"ok": False, "error": "Parameter not found"}
```

**Key insight:** No hardcoded parameter lists - discovers parameters dynamically using LiveAPI introspection.

## Max for Live Device Detection

Max for Live devices are identified by their `class_name`:
- **M4L Audio Effects**: `class_name == "MxDeviceAudioEffect"`
- **M4L MIDI Effects**: `class_name == "MxDeviceMidiEffect"`
- **M4L Instruments**: `class_name == "MxDeviceInstrument"`

## Quick Start Example

**Simple workflow using M4L-specific tools:**

```python
import socket
import json

def send_command(action, **params):
    """Send command to Ableton via port 9004"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('127.0.0.1', 9004))

    command = {'action': action, **params}
    message = json.dumps(command) + '\n'
    sock.sendall(message.encode('utf-8'))

    response = b''
    while b'\n' not in response:
        response += sock.recv(4096)

    sock.close()
    return json.loads(response.decode('utf-8'))

# 1. Find CV LFO device using CV Tools filter
cv_devices = send_command('get_cv_tools_devices', track_index=0)
lfo = cv_devices['cv_devices'][0]  # First CV device
device_index = lfo['index']

# 2. Set LFO rate by parameter name (no index lookup needed!)
send_command('set_device_param_by_name',
    track_index=0,
    device_index=device_index,
    param_name='Rate',
    value=0.5)

# 3. Get current rate value
rate = send_command('get_m4l_param_by_name',
    track_index=0,
    device_index=device_index,
    param_name='Rate')
print("LFO Rate:", rate['value'])
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

## Available M4L Tools (5 Tools)

### 1. is_max_device - Check if Device is M4L

```json
{
  "action": "is_max_device",
  "track_index": 0,
  "device_index": 2
}
```

Response:
```json
{
  "ok": true,
  "is_m4l": true,
  "class_name": "MxDeviceAudioEffect",
  "class_display_name": "Max Audio Effect",
  "device_name": "CV LFO"
}
```

### 2. get_m4l_devices - Get All M4L Devices on Track

```json
{
  "action": "get_m4l_devices",
  "track_index": 0
}
```

Response:
```json
{
  "ok": true,
  "track_index": 0,
  "track_name": "1 Audio",
  "devices": [
    {
      "index": 2,
      "name": "CV LFO",
      "class_name": "MxDeviceAudioEffect",
      "type": "audio_effect",
      "is_active": true,
      "num_parameters": 12
    }
  ],
  "count": 1
}
```

### 3. get_m4l_param_by_name - Get Parameter by Name

```json
{
  "action": "get_m4l_param_by_name",
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
  "max": 1.0,
  "is_enabled": true
}
```

### 4. set_device_param_by_name - Set Parameter by Name

**Works with ANY device, but especially useful for M4L devices:**

```json
{
  "action": "set_device_param_by_name",
  "track_index": 0,
  "device_index": 2,
  "param_name": "Rate",
  "value": 0.75
}
```

Response:
```json
{
  "ok": true,
  "track_index": 0,
  "device_index": 2,
  "param_name": "Rate",
  "param_index": 5,
  "value": 0.75
}
```

### 5. get_cv_tools_devices - Get CV Tools Devices

**Convenience filter for CV Tools pack devices:**

```json
{
  "action": "get_cv_tools_devices",
  "track_index": 0
}
```

Response:
```json
{
  "ok": true,
  "track_index": 0,
  "track_name": "1 Audio",
  "cv_devices": [
    {
      "index": 2,
      "name": "CV LFO",
      "class_name": "MxDeviceAudioEffect",
      "is_active": true,
      "num_parameters": 12
    },
    {
      "index": 3,
      "name": "CV Shaper",
      "class_name": "MxDeviceAudioEffect",
      "is_active": true,
      "num_parameters": 8
    }
  ],
  "count": 2
}
```

## Standard Device Tools (Work with M4L too)

You can also use standard device tools with M4L devices:

1. **List devices**: `get_track_devices` - Returns all devices including M4L
2. **Get parameters**: `get_device_parameters` - Lists all parameters with indices
3. **Set parameters**: `set_device_param` - Set by parameter index
4. **Get device info**: `get_device_info` - Get device details

## Example: Complete CV LFO Control

**Using M4L-specific tools for simplified access:**

```python
#!/usr/bin/env python
"""Control CV Tools LFO device using M4L-specific tools"""

import socket
import json
import time

def send_command(action, **params):
    """Send command to Ableton via port 9004"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('127.0.0.1', 9004))

    command = {'action': action, **params}
    message = json.dumps(command) + '\n'
    sock.sendall(message.encode('utf-8'))

    response = b''
    while b'\n' not in response:
        response += sock.recv(4096)

    sock.close()
    return json.loads(response.decode('utf-8'))

# 1. Find all M4L devices on track 0
result = send_command('get_m4l_devices', track_index=0)
print("M4L devices on track 0:", result['devices'])

# 2. Find CV Tools devices specifically
cv_result = send_command('get_cv_tools_devices', track_index=0)
if cv_result['count'] > 0:
    lfo_device = cv_result['cv_devices'][0]
    device_index = lfo_device['index']
    print("Found CV LFO at device index:", device_index)

    # 3. Get current Rate parameter value
    rate_info = send_command('get_m4l_param_by_name',
        track_index=0,
        device_index=device_index,
        param_name='Rate')
    print("Current Rate:", rate_info)

    # 4. Animate LFO rate using parameter name (no index lookup needed!)
    for i in range(10):
        rate = i / 10.0
        result = send_command('set_device_param_by_name',
            track_index=0,
            device_index=device_index,
            param_name='Rate',
            value=rate)
        print("Set LFO rate to " + str(rate) + ": " + str(result['ok']))
        time.sleep(0.5)
else:
    print("No CV Tools devices found on track 0")
```

## Implementation Details

### How Device Detection Works (ClaudeMCP_Remote/liveapi_tools.py:2164-2318)

The implementation uses LiveAPI's device introspection:

```python
# M4L Device Detection
m4l_classes = ['MxDeviceAudioEffect', 'MxDeviceMidiEffect', 'MxDeviceInstrument']
is_m4l = device.class_name in m4l_classes

# Parameter Discovery (Runtime)
for i, param in enumerate(device.parameters):
    if str(param.name) == param_name:  # User-provided name
        param.value = float(value)  # Set value directly
```

**Key advantages:**
- No hardcoded parameter databases
- Works with all M4L devices (built-in, third-party, custom)
- No maintenance when new devices are added
- User/client provides parameter names from UI

## Resources

- [Live Object Model (LOM) Documentation](https://docs.cycling74.com/max8/vignettes/live_object_model)
- [Max for Live API Reference](https://docs.cycling74.com/max8/vignettes/live_api_overview)
- [CV Tools Documentation](https://www.ableton.com/en/packs/cv-tools/)

## Summary

The ClaudeMCP Remote Script provides **complete M4L support** through 5 specialized tools:

✅ **Implemented (5 tools):**
1. `is_max_device` - Check if device is M4L
2. `get_m4l_devices` - Get all M4L devices on track
3. `get_m4l_param_by_name` - Get parameter by name
4. `set_device_param_by_name` - Set parameter by name (works with ANY device)
5. `get_cv_tools_devices` - Get CV Tools pack devices

✅ **Generic implementation:**
- Works with ALL M4L devices (built-in, third-party, custom, future)
- No hardcoded parameter databases
- Runtime parameter discovery using LiveAPI introspection

## Potential Future Enhancements

- CV modulation mapping introspection (Live 11.1+ API if available)
- M4L device preset loading/saving
- M4L patch file (.amxd) metadata reading
- Additional CV Tools workflow examples
