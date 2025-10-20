---
name: Bug report
about: Create a report to help us improve
title: '[BUG] '
labels: bug
assignees: ''
---

**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Start Ableton Live with ClaudeMCP Remote Script installed
2. Run command '...'
3. Send request '...'
4. See error

**Expected behavior**
A clear and concise description of what you expected to happen.

**Error Output**
If applicable, paste the error message or Log.txt output from the Remote Script.

```
Paste error output here
```

**Environment:**
- Ableton Live version: [e.g. Live 12.0.5]
- Operating System: [e.g. macOS 14.2, Windows 11]
- ClaudeMCP version: [e.g. v1.0.0]
- Python version: [if known]

**Additional context**
Add any other context about the problem here.

**TCP Socket Test**
Did you test the TCP socket connection?
```bash
# On macOS/Linux
nc localhost 9004

# On Windows
Test-NetConnection -ComputerName localhost -Port 9004
```

Result: [Working / Not working / Not tested]
