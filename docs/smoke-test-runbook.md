# Smoke Test Runbook

## Purpose

Run a minimal read-only validation of the existing `ClaudeMCP_Remote` Control Surface on Windows and capture raw TCP request/response output for review.

## Validated Environment Notes

- This ASUS runtime path was validated against Ableton Live `12.3.6` on Windows.
- On this machine, `ClaudeMCP_Remote` became selectable only after being copied into Ableton's built-in scripts directory under `C:\ProgramData\Ableton\Live 12 Suite\Resources\MIDI Remote Scripts`.
- WSL-side socket checks did not reliably see the Ableton listener even when the script was active.
- For this machine, treat Windows-native PowerShell or Command Prompt as the authoritative runtime validation environment.

## Install And Select The Control Surface On Windows

1. Close Ableton Live.
2. Copy the repo's `ClaudeMCP_Remote` folder into the built-in Ableton MIDI Remote Scripts directory:

```powershell
Copy-Item -Recurse -Force .\ClaudeMCP_Remote "C:\ProgramData\Ableton\Live 12 Suite\Resources\MIDI Remote Scripts\ClaudeMCP_Remote"
```

3. Start Ableton Live.
4. Open `Options > Preferences > Link, Tempo & MIDI`.
5. In an empty `Control Surface` slot, choose `ClaudeMCP_Remote`.
6. Leave the paired `Input` and `Output` fields unset unless a separate test requires them.

Note:

- Upstream docs suggest automatic loading after install, but current validated behavior on this machine still requires explicit Control Surface selection.
- The repo now includes [`scripts/windows/deploy_control_surface.ps1`](/home/jniplig/dev/AbletonAPI/ableton-liveapi-tools-fork/scripts/windows/deploy_control_surface.ps1) to make this copy step repeatable.

## Confirm The TCP Server Is Running

1. After selecting the Control Surface, wait a few seconds for Ableton to finish loading.
2. In PowerShell or Command Prompt, check for a listener on port `9004`:

```powershell
Get-NetTCPConnection -LocalPort 9004 -ErrorAction SilentlyContinue | Format-Table -AutoSize LocalAddress,LocalPort,State,OwningProcess
```

Expected shape:

- A line showing `127.0.0.1 9004 Listen <pid>`.

3. If needed, inspect the Ableton log for `ClaudeMCP` startup messages or exceptions:

```powershell
Get-Content "$env:APPDATA\Ableton\Live 12.3.6\Preferences\Log.txt" -Tail 200
```

If the exact version directory differs, adjust the `Live 12.3.6` segment to match the installed version.

## Run The Smoke Test

From the repo root:

```powershell
.\scripts\windows\run_smoke_test.ps1
```

Equivalent direct invocation:

```powershell
py -3 .\scripts\poc\smoke_test_client.py --host 127.0.0.1 --port 9004 --log-file .\logs\smoke-test-run.txt
```

Default action order:

1. `ping`
2. `health_check`
3. `get_session_info`

If a narrower first probe is preferred:

```powershell
python scripts\poc\smoke_test_client.py --action ping --log-file logs\smoke-test-ping.txt
```

## Capture Logs

Client-side capture:

- Use `--log-file logs\smoke-test-run.txt` to append raw request and raw response lines.

Ableton-side capture:

```powershell
Get-Content "$env:APPDATA\Ableton\Live 12.3.6\Preferences\Log.txt" -Tail 200
```

Optional transcript capture in PowerShell:

```powershell
Start-Transcript -Path .\logs\powershell-session.txt
.\scripts\windows\run_smoke_test.ps1
Stop-Transcript
```

## What Success Looks Like

- Ableton remains running after the Control Surface is selected.
- `netstat` shows a listener on port `9004`.
- The smoke client prints the raw JSON request and raw JSON response for each action.
- The first action is read-only.
- At least one response is valid JSON and includes `"ok": true`.
- The log file under `logs\` contains the captured raw request/response output.

## Common Failure Cases

Control Surface does not appear in Ableton:

- Confirm the installed folder name is exactly `ClaudeMCP_Remote`.
- Confirm the folder contains both `__init__.py` and `liveapi_tools.py`.
- Confirm the script was copied into the built-in `C:\ProgramData\Ableton\Live 12 Suite\Resources\MIDI Remote Scripts` directory on this machine.
- Restart Ableton after copying the files.

Connection refused:

- Ableton is not running.
- `ClaudeMCP_Remote` is not selected as a Control Surface.
- The script failed during startup before opening the socket.

Port `9004` is already in use:

- Another process is already bound to the port.
- An earlier Ableton instance did not exit cleanly.

Client times out:

- Ableton loaded but the main-thread queue is blocked.
- The socket accepted the connection but the script did not produce a response within the timeout window.

Malformed or unexpected response:

- Protocol details are inferred from repo code and examples and may differ from external guidance.
- Review the raw response and the Ableton log before assuming the client is wrong.

Ableton log path not found:

- The installed Live version directory differs from the example path.
- Search under `%APPDATA%\Ableton\` for the active `Live x.x.x\Preferences\Log.txt`.

WSL cannot see the listener:

- On this machine, that is expected.
- Use Windows-native PowerShell or Command Prompt for runtime validation instead of WSL socket checks.
