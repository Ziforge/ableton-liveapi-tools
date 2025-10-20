#Remote Script for Ableton Live

A comprehensive Python Remote Script for Ableton Live that exposes **220 LiveAPI tools** via a simple TCP socket interface. Control every aspect of your Ableton Live session programmatically - from playback and recording to tracks, clips, devices, MIDI notes, and Max for Live / CV Tools devices.

[![CI](https://github.com/Ziforge/ableton-liveapi-tools/workflows/CI/badge.svg)](https://github.com/Ziforge/ableton-liveapi-tools/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Ableton Live](https://img.shields.io/badge/Ableton%20Live-11%2F12-blue.svg)](https://www.ableton.com/)
[![Python](https://img.shields.io/badge/Python-2.7%2F3.x-green.svg)](https://www.python.org/)
[![Release](https://img.shields.io/github/v/release/Ziforge/ableton-liveapi-tools)](https://github.com/Ziforge/ableton-liveapi-tools/releases)

## Features

- **220 LiveAPI Tools** - Covers 44 functional categories of Ableton Live's Python API
- **Thread-Safe Architecture** - Queue-based design for reliable communication
- **Simple TCP Interface** - Send JSON commands, receive JSON responses
- **Real-Time Control** - Low latency for live performance
- **Live 12 Support** - Take lanes, display values, application info (Live 12+)
- **Live 11 Compatible** - Backward compatible with graceful feature detection
- **Max for Live Support** - Detect and control M4L devices by parameter name
- **CV Tools Integration** - Full support for Ableton's CV Tools pack
- **MCP Compatible** - Works with Model Context Protocol servers
- **Well Documented** - Comprehensive examples and API reference

## Coverage Methodology

This implementation provides **220 tools across 44 categories** based on:

- **Primary Source**: [Ableton Live API Documentation](https://docs.cycling74.com/max8/vignettes/live_api_overview) (Cycling '74)
- **Reference**: [Live API Doc Archive](https://nsuspray.github.io/Live_API_Doc/) (versions 9.7 - 11.0)
- **Live 12 Features**: Based on [Live 12 Release Notes](https://www.ableton.com/en/release-notes/live-12/)

**Coverage includes:**
- Session and arrangement control (14 tools)
- Track management (13 tools)
- Clip operations (18 tools)
- MIDI note editing (7 tools)
- Device control (12 tools)
- Live 12 exclusive features: Take lanes (8 tools), application info (4 tools)
- Max for Live integration (5 tools)
- 38 additional functional categories

**Known Limitations:**
- Consolidation and some arrangement operations have simplified implementations due to LiveAPI constraints
- Not all Live Object Model (LOM) properties may be exposed (continuous development)

## Tool Categories

| Category | Tools | Description |
|----------|-------|-------------|
| **Session Control** | 14 | Playback, recording, tempo, time signature, loop, metronome |
| **Track Management** | 13 | Create/delete tracks, volume, pan, solo, mute, arm, color |
| **Clip Operations** | 8 | Create, launch, stop, duplicate clips |
| **Clip Extras** | 10 | Looping, markers, gain, pitch, time signature |
| **MIDI Notes** | 7 | Add, get, remove, select MIDI notes |
| **Device Control** | 12 | Add devices, parameters, presets, randomize |
| **Scene Management** | 6 | Create, launch, duplicate scenes |
| **Automation** | 6 | Re-enable automation, capture MIDI |
| **Routing** | 8 | Input/output routing, sends, sub-routing |
| **Browser** | 4 | Browse devices/plugins, load from browser |
| **Transport** | 8 | Jump to time, nudge, arrangement overdub |
| **Groove/Quantize** | 5 | Groove amount, quantize clips/pitch |
| **Monitoring** | 4 | Monitoring state, available routing |
| **Loop/Locator** | 6 | Enable loop, create locators, jump by amount |
| **Project** | 6 | Project root, session record, cue points |
| **Max for Live** | 5 | Detect M4L devices, control by parameter name, CV Tools support |
| **Master Track** | 4 | Master volume, pan, devices, info |
| **Return Tracks** | 3 | Return track info, volume control |
| **Audio Clips** | 5 | Warp mode, warp markers, file paths, warping control |
| **Follow Actions** | 3 | Clip follow actions for live performance |
| **Crossfader** | 3 | DJ-style crossfader control and assignment |
| **Track Groups** | 4 | Group/ungroup tracks, group management |
| **View/Navigation** | 4 | Show views, focus tracks, scroll timeline |
| **Color Utilities** | 2 | Get clip/track colors |
| **Groove Pool** | 2 | Groove library access and assignment |
| **Rack/Chains** | 4 | Instrument/effect rack chain control |
| **Clip Automation** | 6 | Automation envelopes, steps, values |
| **Track Freeze/Flatten** | 3 | Freeze tracks for CPU, flatten to audio |
| **Clip Fades** | 4 | Fade in/out for audio clips |
| **Scene Color** | 2 | Get/set scene colors |
| **Track Annotations** | 2 | Track annotation text |
| **Clip Annotations** | 2 | Clip annotation text |
| **Track Delay** | 2 | Delay compensation in samples |
| **Arrangement Clips** | 3 | Get/duplicate/consolidate arrangement clips |
| **Plugin Windows** | 2 | Show/hide plugin windows |
| **Metronome** | 2 | Metronome volume control |
| **MIDI Messages** | 2 | Send MIDI CC and Program Change |
| **Sampler/Simpler** | 3 | Sample length and playback mode |
| **Clip RAM Mode** | 2 | RAM vs disk streaming |
| **Device Info** | 2 | Device class name and type |
| **Take Lanes** | 8 | Create/manage take lanes (Live 12+) |
| **Application Info** | 4 | Version, variant, build ID, message boxes |
| **Display Values** | 2 | Get parameter values as shown in UI |
| **Additional Properties** | 10 | Clip start time, track/scene states, signatures |

**Total: 220 Tools**

## Quick Start

### Installation

1. **Clone this repository:**
   ```bash
   git clone https://github.com/Ziforge/ableton-liveapi-tools.git
   cd ableton-liveapi-tools
   ```

2. **Run the installation script:**
   ```bash
   bash install.sh
   ```

   Or manually copy to Ableton's Remote Scripts folder:
   ```bash
   # macOS
   cp -r ClaudeMCP_Remote ~/Music/Ableton/User\ Library/Remote\ Scripts/

   # Windows
   # Copy to: %USERPROFILE%\Documents\Ableton\User Library\Remote Scripts\
   ```

3. **Restart Ableton Live**

4. **Verify installation:**
   ```bash
   python3 examples/test_connection.py
   ```

### Basic Usage

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

# Set tempo
result = send_command('set_tempo', bpm=128)
print("Tempo: " + str(result['bpm']) + " BPM")

# Create a MIDI track
result = send_command('create_midi_track', name='Bass')
track_index = result['track_index']

# Create a clip and add notes
send_command('create_midi_clip', track_index=track_index, scene_index=0, length=4.0)
notes = [
    {"pitch": 36, "start": 0.0, "duration": 0.5, "velocity": 100},
    {"pitch": 36, "start": 1.0, "duration": 0.5, "velocity": 100}
]
send_command('add_notes', track_index=track_index, scene_index=0, notes=notes)

# Launch the clip
send_command('launch_clip', track_index=track_index, scene_index=0)
```

## Documentation

- **[Installation Guide](docs/INSTALLATION.md)** - Detailed installation instructions
- **[API Reference](docs/API_REFERENCE.md)** - Complete list of all 220 tools
- **[Troubleshooting](docs/TROUBLESHOOTING.md)** - Common issues and solutions

## Examples

Check the `examples/` directory for:

- **`test_connection.py`** - Verify the Remote Script is working
- **`basic_usage.py`** - Simple examples of common operations
- **`creative_workflow.py`** - Generate music programmatically
- **`test_all_tools.py`** - Comprehensive test of all 220 tools

## Architecture

### Thread-Safe Design

The Remote Script uses a queue-based architecture to ensure thread safety:

1. **Socket Thread** - Receives commands via TCP (port 9004)
2. **Command Queue** - Stores commands waiting to be processed
3. **Main Thread** - Processes commands via `update_display()` callback
4. **Response Queue** - Returns results to socket thread
5. **Socket Thread** - Sends response back to client

This design ensures all LiveAPI calls happen on Ableton's main thread, preventing crashes and race conditions.

### Communication Protocol

**Request Format:**
```json
{
  "action": "set_tempo",
  "bpm": 128
}
```

**Response Format:**
```json
{
  "ok": true,
  "bpm": 128.0
}
```

## Requirements

- **Ableton Live** 11 or 12 (Suite, Standard, or Intro)
- **Python** 2.7+ (included with Ableton Live)
- **Operating System** macOS, Windows, or Linux

## Use Cases

- **Algorithmic Composition** - Generate music with code
- **AI Music Production** - Control Ableton with LLMs and AI agents
- **Live Coding** - Real-time music performance
- **Automation** - Batch processing and workflow automation
- **Integration** - Connect Ableton to other software/hardware
- **Custom Controllers** - Build your own MIDI/OSC controllers
- **Music Analysis** - Extract data from Ableton sessions
- **CV Tools Control** - Automate Max for Live CV modulation devices

## Max for Live & CV Tools Support

The Remote Script includes full support for Max for Live (M4L) devices, including Ableton's CV Tools pack:

### Detect M4L Devices
```python
# Get all Max for Live devices on track 0
response = send_command({"action": "get_m4l_devices", "track_index": 0})

# Get only CV Tools devices
cv_devices = send_command({"action": "get_cv_tools_devices", "track_index": 0})
```

### Control by Parameter Name
```python
# Set CV LFO rate by parameter name (easier than finding param index)
send_command({
    "action": "set_device_param_by_name",
    "track_index": 0,
    "device_index": 2,
    "param_name": "Rate",
    "value": 0.75
})

# Get parameter value by name
param = send_command({
    "action": "get_m4l_param_by_name",
    "track_index": 0,
    "device_index": 2,
    "param_name": "Rate"
})
```

### Supported M4L Device Types
- **CV LFO** - Control Rate, Shape, Depth
- **CV Shaper** - Control Drive, Curve, Bias
- **CV Envelope Follower** - Control Attack, Release, Gain
- **CV Instrument** - Control Range, Quantize
- **Any M4L Device** - Access parameters by name

See `examples/cv_tools_control.py` for a complete working example.

For detailed M4L integration documentation, see [MAX4LIVE_INTEGRATION.md](MAX4LIVE_INTEGRATION.md).

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [Ableton Live's Python Remote Script API](https://docs.cycling74.com/max8/vignettes/live_api_overview)
- Designed for use with [Model Context Protocol (MCP)](https://modelcontextprotocol.io/)
- Created by Claude Code

## Support

- **Issues:** [GitHub Issues](https://github.com/Ziforge/ableton-liveapi-tools/issues)
- **Discussions:** [GitHub Discussions](https://github.com/Ziforge/ableton-liveapi-tools/discussions)

## Roadmap

- [ ] Add WebSocket support alongside TCP
- [ ] Create high-level wrapper libraries (Python, JavaScript, etc.)
- [ ] Add recording and audio file management tools
- [ ] Create visual debugging/monitoring dashboard
- [ ] Add Max for Live integration examples

---

Made for the Ableton Live community
