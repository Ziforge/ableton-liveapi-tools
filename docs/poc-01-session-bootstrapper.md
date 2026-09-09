# POC 01: Session Bootstrapper

## Objective

Establish a minimal, additive validation path that proves the `ClaudeMCP_Remote` Control Surface loads in Ableton Live, starts its localhost TCP server, and responds to at least one read-only request from an external client.

## Scope

- Install or verify the existing `ClaudeMCP_Remote` folder in Ableton's User Library Remote Scripts path on Windows.
- Select `ClaudeMCP_Remote` as an Ableton Control Surface.
- Confirm that Ableton listens on `127.0.0.1:9004`.
- Run `scripts/poc/smoke_test_client.py` using read-only actions only.
- Capture raw request and raw response output for review.

## Non-goals

- No bootstrapper logic beyond smoke validation.
- No live-performance workflow logic.
- No edits to `ClaudeMCP_Remote/__init__.py`.
- No edits to `ClaudeMCP_Remote/liveapi_tools.py`.
- No changes to the hard-coded action router.
- No attempt to validate all advertised tools.

## Inputs

- Local fork checkout on the ASUS machine.
- Ableton Live installed on Windows.
- Existing Remote Script source under `ClaudeMCP_Remote/`.
- Smoke client at `scripts/poc/smoke_test_client.py`.
- Ableton log file at `%APPDATA%\Ableton\Live x.x.x\Preferences\Log.txt`.

## Outputs

- Evidence that Ableton loaded the Control Surface without obvious startup errors.
- Evidence that `127.0.0.1:9004` is listening while Ableton is running.
- Raw request and raw response output from a read-only smoke test.
- A simple pass/fail result for this phase.

## Proposed Command Sequence

```powershell
cd C:\path\to\ableton-liveapi-tools-fork
python scripts\poc\smoke_test_client.py --host 127.0.0.1 --port 9004 --log-file logs\smoke-test-session.txt
```

Optional explicit single-action probe:

```powershell
python scripts\poc\smoke_test_client.py --action ping --log-file logs\smoke-test-ping.txt
```

Optional listener check before the client run:

```powershell
netstat -ano | findstr 9004
```

## Verification Steps

1. Confirm `ClaudeMCP_Remote` is present under the Ableton User Library Remote Scripts directory.
2. Launch Ableton Live and select `ClaudeMCP_Remote` in Preferences > Link, Tempo & MIDI > Control Surface.
3. Open the Ableton log and confirm there is no immediate `ClaudeMCP` startup exception.
4. Confirm a localhost listener exists on port `9004`.
5. Run the smoke client and verify that the first action is read-only.
6. Review the captured raw request and raw response output in the chosen log file.

## Risks

- Upstream install docs appear to overstate autoloading; manual Control Surface selection is likely required.
- The protocol is inferred from repo code and examples, not from a formal spec.
- Ableton can load the Control Surface but still fail to bind the socket if the port is already in use.
- `get_session_info` is read-only but still depends on the main-thread queue path being healthy.
- The Ableton log location varies by installed version string.

## Pass/Fail Criteria

Pass:

- Ableton loads `ClaudeMCP_Remote` without obvious startup failure.
- Port `9004` is listening on `127.0.0.1`.
- The smoke client sends a read-only request first.
- The smoke client receives valid JSON with `"ok": true`.
- Raw request/response output is saved for review.

Fail:

- Ableton cannot load or select the Control Surface.
- No listener appears on port `9004`.
- The client cannot connect or times out.
- The response is empty, malformed, or returns `"ok": false`.

## Rollback Approach

- Deselect `ClaudeMCP_Remote` in Ableton Preferences and switch the Control Surface slot back to `None`.
- Remove or rename the installed `ClaudeMCP_Remote` directory from the Ableton User Library Remote Scripts path if needed.
- Delete only the smoke-test log files created under `logs/`.
- Leave core repo files unchanged, since this phase is additive only.
