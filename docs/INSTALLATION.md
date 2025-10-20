# Installation Guide

## System Requirements

### Required Software
- Ableton Live 11.0+ or 12.0+ (Suite, Standard, or Intro editions)
- Python 2.7+ (bundled with Ableton Live)

### Supported Platforms
- macOS 10.13+
- Windows 10/11
- Linux (experimental)

## Installation Methods

### Method 1: Automated Installation (Recommended)

```bash
git clone https://github.com/Ziforge/ableton-liveapi-tools.git
cd ableton-liveapi-tools
bash install.sh
```

The installation script performs the following operations:
1. Detects operating system and determines correct installation path
2. Backs up existing installation if present
3. Copies `ClaudeMCP_Remote` directory to Ableton's Remote Scripts folder
4. Verifies file integrity

### Method 2: Manual Installation

#### macOS

```bash
cp -r ClaudeMCP_Remote ~/Music/Ableton/User\ Library/Remote\ Scripts/
```

#### Windows

Copy the `ClaudeMCP_Remote` directory to:
```
%USERPROFILE%\Documents\Ableton\User Library\Remote Scripts\
```

#### Linux

```bash
cp -r ClaudeMCP_Remote ~/Music/Ableton/User\ Library/Remote\ Scripts/
```

## Post-Installation

### Verification

1. Restart Ableton Live completely (Quit and relaunch)

2. Verify TCP socket is listening on port 9004:

```bash
# macOS/Linux
lsof -i :9004

# Windows
netstat -an | findstr :9004
```

Expected output should show Ableton Live process listening on port 9004.

3. Run connection test:

```bash
python3 examples/test_connection.py
```

Expected output:
```
Connection successful
Tool count: 125
Ableton version: 12
```

### Troubleshooting

If the Remote Script does not load:

1. **Check file permissions**
   ```bash
   # macOS/Linux - ensure files are readable
   chmod -R 755 ~/Music/Ableton/User\ Library/Remote\ Scripts/ClaudeMCP_Remote
   ```

2. **Verify file structure**
   ```
   ClaudeMCP_Remote/
   ├── __init__.py
   └── liveapi_tools.py
   ```

3. **Check Ableton Live log**
   - macOS: `~/Library/Preferences/Ableton/Live */Log.txt`
   - Windows: `%APPDATA%\Ableton\Live *\Preferences\Log.txt`

   Search for "ClaudeMCP" or errors related to Remote Scripts.

4. **Python compatibility**
   - Ableton Live 11/12 uses Python 2.7
   - Ensure no Python 3-specific syntax in modifications

## Network Configuration

### Firewall Settings

The Remote Script binds to `127.0.0.1:9004` (localhost only by default). For remote access:

1. Modify `__init__.py` line ~80:
   ```python
   self.server_socket.bind(('0.0.0.0', 9004))  # Allow external connections
   ```

2. Configure firewall to allow TCP port 9004

**Security Warning:** Exposing port 9004 to external networks allows remote control of Ableton Live. Implement authentication if enabling remote access.

### Port Configuration

To change the default port (9004):

1. Edit `__init__.py` line ~80:
   ```python
   self.server_socket.bind(('127.0.0.1', YOUR_PORT))
   ```

2. Update client code to connect to new port

## Uninstallation

### macOS/Linux
```bash
rm -rf ~/Music/Ableton/User\ Library/Remote\ Scripts/ClaudeMCP_Remote
```

### Windows
Delete the directory:
```
%USERPROFILE%\Documents\Ableton\User Library\Remote Scripts\ClaudeMCP_Remote
```

## Upgrade Procedure

1. Backup existing installation:
   ```bash
   cp -r ~/Music/Ableton/User\ Library/Remote\ Scripts/ClaudeMCP_Remote \
         ~/Music/Ableton/User\ Library/Remote\ Scripts/ClaudeMCP_Remote.backup
   ```

2. Pull latest changes:
   ```bash
   git pull origin main
   ```

3. Run installation script:
   ```bash
   bash install.sh
   ```

4. Restart Ableton Live

## Development Installation

For development and debugging:

1. Clone repository:
   ```bash
   git clone https://github.com/Ziforge/ableton-liveapi-tools.git
   cd ableton-liveapi-tools
   ```

2. Create symlink to Remote Scripts directory:
   ```bash
   # macOS/Linux
   ln -s $(pwd)/ClaudeMCP_Remote \
         ~/Music/Ableton/User\ Library/Remote\ Scripts/ClaudeMCP_Remote
   ```

3. Edit files in repository, changes take effect after Ableton restart

## Platform-Specific Notes

### macOS
- Gatekeeper may block execution initially
- Remote Scripts directory created on first Ableton launch
- Check Console.app for system-level errors

### Windows
- Some antivirus software may flag socket connections
- Ensure Windows Defender allows Python.exe network access
- Use absolute paths (avoid `~` shorthand)

### Linux
- WINE/Ableton Live compatibility varies
- May require manual MIDI/Audio driver configuration
- Remote Scripts path may differ based on installation method
