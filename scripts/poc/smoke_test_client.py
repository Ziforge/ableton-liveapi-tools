#!/usr/bin/env python3
"""
Minimal smoke test client for the ClaudeMCP Remote Script TCP server.

Assumptions based on repo inspection:
- The Remote Script listens on 127.0.0.1:9004 by default.
- Requests are JSON objects terminated by a single newline.
- Responses are JSON objects terminated by a single newline.
- Safe read-only actions include: ping, health_check, get_session_info.
"""

import argparse
import json
import socket
import sys
from datetime import datetime


DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 9004
DEFAULT_TIMEOUT = 5.0
DEFAULT_ACTIONS = ("ping", "health_check", "get_session_info")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Send a small read-only smoke test sequence to the Ableton Remote Script."
    )
    parser.add_argument("--host", default=DEFAULT_HOST, help="TCP host to connect to")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help="TCP port to connect to")
    parser.add_argument(
        "--timeout",
        type=float,
        default=DEFAULT_TIMEOUT,
        help="Socket timeout in seconds",
    )
    parser.add_argument(
        "--action",
        action="append",
        dest="actions",
        help="Action to send. Repeat to override the default sequence.",
    )
    parser.add_argument(
        "--log-file",
        help="Optional path to append raw request/response output for review.",
    )
    return parser.parse_args()


def emit(text, log_file=None):
    print(text)
    if log_file:
        with open(log_file, "a", encoding="utf-8") as handle:
            handle.write(text + "\n")


def recv_line(sock):
    chunks = []
    while True:
        chunk = sock.recv(4096)
        if not chunk:
            break
        chunks.append(chunk)
        if b"\n" in chunk:
            break
    if not chunks:
        return b""
    return b"".join(chunks)


def send_action(sock, action, log_file=None):
    command = {"action": action}
    raw_request = json.dumps(command) + "\n"

    emit("", log_file=log_file)
    emit("----", log_file=log_file)
    emit("timestamp: {0}".format(datetime.now().isoformat(timespec="seconds")), log_file=log_file)
    emit("action: {0}".format(action), log_file=log_file)
    emit("raw request: {0}".format(raw_request.rstrip("\n")), log_file=log_file)

    sock.sendall(raw_request.encode("utf-8"))
    raw_response = recv_line(sock)
    if not raw_response:
        raise RuntimeError("No response received from server")

    decoded_response = raw_response.decode("utf-8", errors="replace").rstrip("\n")
    emit("raw response: {0}".format(decoded_response), log_file=log_file)

    try:
        parsed = json.loads(decoded_response)
    except ValueError as exc:
        raise RuntimeError("Response was not valid JSON: {0}".format(exc))

    return parsed


def main():
    args = parse_args()
    actions = tuple(args.actions) if args.actions else DEFAULT_ACTIONS

    if not actions:
        print("error: no actions specified", file=sys.stderr)
        return 2

    try:
        with socket.create_connection((args.host, args.port), timeout=args.timeout) as sock:
            sock.settimeout(args.timeout)
            emit(
                "Connecting to {0}:{1} with timeout {2}s".format(
                    args.host, args.port, args.timeout
                ),
                log_file=args.log_file,
            )

            for index, action in enumerate(actions):
                if index == 0 and action not in ("ping", "health_check", "get_session_info"):
                    raise RuntimeError(
                        "First action must be read-only for this smoke test: ping, health_check, or get_session_info"
                    )

                response = send_action(sock, action, log_file=args.log_file)
                if not response.get("ok"):
                    raise RuntimeError(
                        "Action '{0}' failed: {1}".format(
                            action, response.get("error", "unknown error")
                        )
                    )

            emit("", log_file=args.log_file)
            emit("Smoke test passed", log_file=args.log_file)
            return 0

    except ConnectionRefusedError:
        print(
            "error: connection refused on {0}:{1}; confirm Ableton is running and the Control Surface is selected".format(
                args.host, args.port
            ),
            file=sys.stderr,
        )
        return 1
    except socket.timeout:
        print(
            "error: timed out talking to {0}:{1}; Ableton may be busy or the script may not be loaded".format(
                args.host, args.port
            ),
            file=sys.stderr,
        )
        return 1
    except OSError as exc:
        print("error: socket failure: {0}".format(exc), file=sys.stderr)
        return 1
    except RuntimeError as exc:
        print("error: {0}".format(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
