# Windows Install Notes

## Current Validated Behavior

- Validated on the ASUS machine with Ableton Live `12.3.6`.
- `ClaudeMCP_Remote` did not become selectable when copied only into the user-level Ableton library path.
- On this machine, Ableton discovered the script only after it was copied into:

```text
C:\ProgramData\Ableton\Live 12 Suite\Resources\MIDI Remote Scripts\ClaudeMCP_Remote
```

- After installation, the script still had to be selected manually in `Options > Preferences > Link, Tempo & MIDI`.
- The script then logged successful startup and exposed a TCP listener on `127.0.0.1:9004`.

## Recommended Install Procedure

1. Close Ableton Live.
2. Open PowerShell as Administrator if the `ProgramData` directory requires elevation.
3. From the repo root, run:

```powershell
.\scripts\windows\deploy_control_surface.ps1
```

4. Start Ableton Live.
5. Open `Options > Preferences > Link, Tempo & MIDI`.
6. Pick `ClaudeMCP_Remote` in an empty `Control Surface` slot.
7. Leave `Input` and `Output` unset unless another test explicitly requires them.

## Verify Startup

Check the Ableton log:

```powershell
Get-Content "$env:APPDATA\Ableton\Live 12.3.6\Preferences\Log.txt" -Tail 200
```

Expected startup lines include:

- `Socket server started successfully on port 9004`
- `ClaudeMCP Remote Script initialized (Queue-based, Thread-Safe)`
- `Socket server listening on port 9004`

## Verify Listener

```powershell
Get-NetTCPConnection -LocalPort 9004 -ErrorAction SilentlyContinue | Format-Table -AutoSize LocalAddress,LocalPort,State,OwningProcess
```

Expected result:

- `127.0.0.1 9004 Listen <pid>`

## Verify With Smoke Test

```powershell
.\scripts\windows\run_smoke_test.ps1
```

That wrapper runs the read-only smoke client and writes raw request/response output under `logs\`.

## Operational Notes

- On this machine, Windows-native runtime validation is more reliable than WSL for socket checks against Ableton.
- Treat WSL as the editing environment and Windows PowerShell as the runtime validation environment.
- Do not modify core Remote Script files for installation-only troubleshooting unless later evidence requires it.
