# ClaudeMCP Remote Script for Ableton Live

A comprehensive Python Remote Script for Ableton Live that exposes **120 LiveAPI tools** via a simple TCP socket interface. Control every aspect of your Ableton Live session programmatically - from playback and recording to tracks, clips, devices, and MIDI notes.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Ableton Live](https://img.shields.io/badge/Ableton%20Live-11%2F12-blue.svg)](https://www.ableton.com/)
[![Python](https://img.shields.io/badge/Python-2.7%2F3.x-green.svg)](https://www.python.org/)

## Features

- **120 LiveAPI Tools** - Complete control over Ableton Live
- **Thread-Safe Architecture** - Queue-based design for reliable communication
- **Simple TCP Interface** - Send JSON commands, receive JSON responses
- **Real-Time Control** - Low latency for live performance
- **MCP Compatible** - Works with Model Context Protocol servers
- **Well Documented** - Comprehensive examples and API reference

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

**Total: 120 Tools**

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
print(f"Tempo: {result['bpm']} BPM")

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
- **[API Reference](docs/API_REFERENCE.md)** - Complete list of all 120 tools
- **[Troubleshooting](docs/TROUBLESHOOTING.md)** - Common issues and solutions

## Examples

Check the `examples/` directory for:

- **`test_connection.py`** - Verify the Remote Script is working
- **`basic_usage.py`** - Simple examples of common operations
- **`creative_workflow.py`** - Generate music programmatically
- **`test_all_tools.py`** - Comprehensive test of all 120 tools

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
- **AI Music Production** - Control Ableton with Claude, GPT, or other LLMs
- **Live Coding** - Real-time music performance
- **Automation** - Batch processing and workflow automation
- **Integration** - Connect Ableton to other software/hardware
- **Custom Controllers** - Build your own MIDI/OSC controllers
- **Music Analysis** - Extract data from Ableton sessions

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
- Inspired by [ahujasid/ableton-mcp](https://github.com/ahujasid/ableton-mcp)
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
