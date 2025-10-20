# Contributing to Ableton LiveAPI Tools

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Code of Conduct

This project adheres to a Code of Conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior by opening an issue.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates. When creating a bug report, include:

- Clear, descriptive title
- Exact steps to reproduce
- Expected vs actual behavior
- Ableton Live version and OS
- Error messages from Log.txt
- TCP socket connection test results

Use the bug report template when creating issues.

### Suggesting Features

Feature suggestions are welcome! Please:

- Use a clear, descriptive title
- Provide detailed description of the proposed feature
- Explain the use case and workflow benefits
- Indicate which LiveAPI areas it would affect
- Consider backwards compatibility

Use the feature request template when suggesting features.

### Pull Requests

1. **Fork the repository** and create your branch from `main`
2. **Follow the existing code style**:
   - Use 4-space indentation
   - Follow PEP 8 for Python code (where Python 2.7 compatible)
   - Add docstrings for new tools/functions
   - Keep lines under 100 characters when possible

3. **Test your changes**:
   - Test with Ableton Live (ideally both 11 and 12)
   - Verify TCP socket communication works
   - Ensure Python 2.7 compatibility (Ableton's Python version)
   - Test on your OS (note which OS in PR)

4. **Update documentation**:
   - Add/update docstrings
   - Update README.md if adding new tools
   - Update examples if relevant

5. **Commit messages**:
   - Use present tense ("Add feature" not "Added feature")
   - First line: brief summary (50 chars or less)
   - Blank line, then detailed description if needed
   - Reference issues: "Fixes #123" or "Related to #456"

6. **Submit the PR**:
   - Fill out the pull request template completely
   - Link related issues
   - Describe testing performed

## Development Setup

### Prerequisites

- Ableton Live 11 or 12
- Git
- Text editor (VS Code, Sublime, etc.)
- Basic Python knowledge

### Installation for Development

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/ableton-liveapi-tools.git
cd ableton-liveapi-tools

# Create a symlink to Ableton's Remote Scripts directory
# macOS
ln -s "$(pwd)/ClaudeMCP_Remote" "$HOME/Music/Ableton/User Library/Remote Scripts/ClaudeMCP_Remote"

# Windows (run as Administrator)
mklink /D "%USERPROFILE%\Documents\Ableton\User Library\Remote Scripts\ClaudeMCP_Remote" "%CD%\ClaudeMCP_Remote"

# Linux
ln -s "$(pwd)/ClaudeMCP_Remote" "$HOME/.ableton/User Library/Remote Scripts/ClaudeMCP_Remote"
```

### Testing Changes

1. **Restart Ableton Live** after making changes
2. **Check Log.txt** for errors:
   - macOS: `~/Library/Preferences/Ableton/Live <version>/Log.txt`
   - Windows: `%APPDATA%\Ableton\Live <version>\Preferences\Log.txt`
   - Linux: `~/.ableton/Live <version>/Preferences/Log.txt`

3. **Test TCP socket**:
   ```bash
   # Test connection
   nc localhost 9004

   # Test a tool
   {"tool": "get_tempo"}
   ```

4. **Run examples**:
   ```bash
   cd examples
   python test_connection.py
   ```

## Project Structure

```
ClaudeMCP_Remote/
├── __init__.py          # Main Remote Script entry point
└── liveapi_tools.py     # 196 LiveAPI tools implementation

docs/
├── ARCHITECTURE.md      # System architecture
└── MCP_INTEGRATION.md   # MCP integration guide

examples/
├── test_connection.py   # Basic connection test
├── basic_usage.py       # Simple tool examples
├── midi_editing.py      # MIDI note manipulation
└── advanced_workflow.py # Complex automation

install.sh              # Installation script
```

## Adding New Tools

To add a new LiveAPI tool:

1. **Add tool definition** to `tools_config.py`:
   ```python
   {
       "name": "tool_name",
       "description": "What the tool does",
       "input_schema": {
           "type": "object",
           "properties": {
               "param": {"type": "string", "description": "Parameter description"}
           },
           "required": ["param"]
       }
   }
   ```

2. **Implement tool handler** in `liveapi_tools.py`:
   ```python
   def handle_tool_name(self, params):
       """Tool description.

       Args:
           params: dict with required parameters

       Returns:
           dict with 'ok' and result data
       """
       try:
           # Implementation using Live.Song() API
           return {"ok": True, "result": data}
       except Exception as e:
           return {"ok": False, "error": str(e)}
   ```

3. **Add to tool routing** in `process_request`:
   ```python
   elif tool_name == "tool_name":
       return self.handle_tool_name(params)
   ```

4. **Document the tool** in README.md

5. **Add example usage** in relevant example file

## Python 2.7 Compatibility

Ableton Live uses Python 2.7, so ensure compatibility:

- No f-strings (use `.format()` or `%` formatting)
- No type hints
- No `asyncio` or modern async features
- No `pathlib` (use `os.path`)
- Test with Python 2.7 if possible

## LiveAPI Resources

- [LiveAPI Documentation](https://docs.cycling74.com/max8/vignettes/live_api_overview)
- [Ableton Remote Scripts](https://github.com/gluon/AbletonLive11_MIDIRemoteScripts)
- [Live Object Model](https://structure-void.com/PythonLiveAPI_documentation/)

## Questions?

- Open an issue for questions
- Check existing issues and documentation
- Join discussions tab (if enabled)

## Recognition

Contributors will be recognized in:
- GitHub contributors page
- Release notes for significant contributions
- README.md acknowledgments section

Thank you for contributing!
