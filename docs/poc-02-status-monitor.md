# POC 02: Status Monitor

## Objective

Define a minimal, additive status-monitor layer that improves confidence in `ClaudeMCP_Remote` runtime health without modifying the core Remote Script, the 220-action router, or any live-performance behavior.

## Scope

- Build on the validated Windows smoke-test workflow from POC 01.
- Focus on read-only runtime signals already exposed by the repo and the host environment.
- Standardize how to confirm that the Control Surface loaded, the TCP server is listening, and basic session health can be queried safely.
- Capture evidence from both Ableton logs and TCP responses for later review.

## Non-goals

- No edits to `ClaudeMCP_Remote/__init__.py`.
- No edits to `ClaudeMCP_Remote/liveapi_tools.py`.
- No changes to the static action router.
- No event subscription or observer subsystem.
- No attempt to stream real-time session state.
- No live-performance automation, transport control, or write actions.

## Current Known Signals

From repo inspection and runtime validation, the following read-only signals already exist:

- Ableton log messages emitted through `c_instance.log_message(...)`.
- Startup log lines including:
  - `Socket server started successfully on port 9004`
  - `ClaudeMCP Remote Script initialized (Queue-based, Thread-Safe)`
  - `Socket server listening on port 9004`
  - `Client connected from ...`
- TCP listener on `127.0.0.1:9004`.
- Read-only TCP actions:
  - `ping`
  - `health_check`
  - `get_session_info`

## Proposed Monitor Surface

The status monitor for this phase should be a wrapper-level workflow, not a new core feature.

### Layer 1: Process and startup evidence

- Confirm Ableton Live is running.
- Confirm `ClaudeMCP_Remote` is selected as a Control Surface.
- Confirm recent Ableton log lines show successful script startup rather than an import or bind failure.

### Layer 2: Listener evidence

- Confirm Windows shows `127.0.0.1:9004` in `Listen` state.
- Record the owning process ID when available.

### Layer 3: Read-only protocol evidence

- Run `ping` to prove command/response flow works.
- Run `health_check` to capture:
  - `ok`
  - `message`
  - `tool_count`
  - `ableton_version`
  - `queue_size`
- Run `get_session_info` to capture:
  - playback state
  - tempo
  - time signature
  - track count
  - scene count
  - loop values

### Layer 4: Evidence capture

- Save raw request and raw response payloads.
- Save a short Ableton log extract around startup and the client connection event.
- Keep outputs timestamped for side-by-side review across runs.

## Proposed Artifacts

This phase does not require core-code changes. The likely additive outputs are:

- a small Windows-native wrapper script for repeated status checks
- a status log file under `logs/`
- a short runbook section or dedicated doc for interpreting the captured signals

The current repo already includes most of the needed pieces:

- `scripts/windows/run_smoke_test.ps1`
- `scripts/poc/smoke_test_client.py`
- `docs/smoke-test-runbook.md`

## Proposed Command Sequence

```powershell
.\scripts\windows\deploy_control_surface.ps1
```

Restart Ableton Live, select `ClaudeMCP_Remote`, then run:

```powershell
.\scripts\windows\run_smoke_test.ps1
```

Optional direct checks:

```powershell
Get-NetTCPConnection -LocalPort 9004 -ErrorAction SilentlyContinue | Format-Table -AutoSize LocalAddress,LocalPort,State,OwningProcess
Get-Content "$env:APPDATA\Ableton\Live 12.3.6\Preferences\Log.txt" -Tail 200
```

## Verification Steps

1. Confirm Ableton starts without obvious Control Surface load errors.
2. Confirm `127.0.0.1:9004` is in `Listen` state from Windows.
3. Run the smoke-test wrapper and confirm the first action remains read-only.
4. Confirm `ping`, `health_check`, and `get_session_info` all return valid JSON with `"ok": true`.
5. Review the raw request/response capture and the recent Ableton log tail together.
6. Confirm the captured `tool_count` and `ableton_version` remain plausible across repeated runs.

## Risks

- This repo still has no event-driven status feed, so the monitor is polling-based and coarse.
- `health_check` is useful but limited; it reports queue size and version, not full runtime internals.
- WSL-side socket visibility was unreliable on this machine, so status checks must be treated as Windows-native.
- The exact Ableton log path can vary by installed version.
- A successful listener check does not guarantee every action path is implemented correctly.

## Pass/Fail Criteria

Pass:

- Ableton startup evidence is present in the log.
- Windows shows `127.0.0.1:9004` listening.
- Read-only status requests succeed consistently.
- Raw request/response and log evidence are captured together.
- No core Remote Script changes are required for the monitor workflow.

Fail:

- The script does not load or does not stay loaded.
- The port is not listening.
- Read-only requests fail, time out, or return malformed JSON.
- The monitoring workflow depends on WSL-only checks that do not reflect the real Windows runtime.

## Rollback Approach

- Deselect `ClaudeMCP_Remote` in Ableton Preferences if needed.
- Remove the deployed control surface copy from the Ableton scripts directory if this POC must be backed out.
- Delete only additive logs and wrapper outputs.
- Leave core repo code unchanged.

## Recommendation

Proceed with POC 02 as a documentation-and-wrapper phase first. Do not introduce a new monitoring subsystem in the Remote Script until repeated Windows-native runs show a stable need for more granular observability.
