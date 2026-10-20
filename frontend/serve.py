#!/usr/bin/env python3
"""Local static server + CORS proxy for the Chicago Food Rescue Coordinator Dispatch Console.

Serves `frontend/index.html` at http://127.0.0.1:8090 (loopback only) and proxies `/apps/*`, `/run`, `/run_sse`,
`/list-apps`, and `/health` to the deployed Cloud Run service (`A4I_BACKEND_URL`) so browser requests
succeed even when `A4I_ALLOW_ORIGINS` is not set on Cloud Run.

Usage:
    python3 frontend/serve.py
"""

import datetime
import http.server
import json
import os
import pathlib
import threading
import urllib.error
import urllib.request

PORT = int(os.environ.get("PORT", "8090"))
BACKEND_URL = os.environ.get(
    "A4I_BACKEND_URL", "https://food-broker-817377390808.us-east1.run.app"
).rstrip("/")
FRONTEND_DIR = pathlib.Path(__file__).resolve().parent
STATE_FILE = FRONTEND_DIR / ".broker_state.json"
STATE_LOCK = threading.Lock()
PROXY_PREFIXES = ("/apps/", "/run", "/run_sse", "/list-apps", "/health")
ALLOWED_FILES = {
    "/": "index.html",
    "/index.html": "index.html",
    "/recipients_data.js": "recipients_data.js",
}


def _default_state() -> dict:
    return {
        "reservations": [],
        "claimed_pallets_by_org": {},
        "declined_by_posting": {},
        "onboarded_pantries": {},
        "posting_locks": {},
    }


def _load_state() -> dict:
    if not STATE_FILE.exists():
        return _default_state()
    try:
        data = json.loads(STATE_FILE.read_text(encoding="utf-8"))
        base = _default_state()
        base.update(data)
        return base
    except Exception:
        return _default_state()


def _save_state(state: dict) -> None:
    try:
        STATE_FILE.write_text(json.dumps(state, indent=2), encoding="utf-8")
    except Exception:
        pass


class ConsoleHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(FRONTEND_DIR), **kwargs)

    def end_headers(self):
        origin = self.headers.get("Origin", "")
        if origin in (f"http://127.0.0.1:{PORT}", f"http://localhost:{PORT}"):
            self.send_header("Access-Control-Allow-Origin", origin)
        else:
            self.send_header("Access-Control-Allow-Origin", f"http://127.0.0.1:{PORT}")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        super().end_headers()

    def _send_json(self, status: int, payload: dict):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self.end_headers()

    def do_GET(self):
        path = self.path.split("?", 1)[0]
        if path == "/api/state":
            with STATE_LOCK:
                self._send_json(200, _load_state())
            return
        if path.startswith(PROXY_PREFIXES):
            self._proxy("GET")
            return
        if path not in ALLOWED_FILES:
            self.send_error(404, "Not Found")
            return
        self.path = "/" + ALLOWED_FILES[path]
        super().do_GET()

    def do_POST(self):
        path = self.path.split("?", 1)[0]
        if path.startswith("/api/state/"):
            self._handle_state_post(path)
            return
        if self.path.startswith(PROXY_PREFIXES):
            self._proxy("POST")
            return
        self.send_error(405, "Method Not Allowed")

    def _handle_state_post(self, path: str):
        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length) if length > 0 else b"{}"
        try:
            payload = json.loads(raw.decode("utf-8"))
        except Exception:
            self._send_json(400, {"error": "invalid_json"})
            return

        action = path.removeprefix("/api/state/")
        now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()

        with STATE_LOCK:
            state = _load_state()

            if action == "claim":
                posting_id = str(payload.get("posting_id") or "").strip()
                org_name = str(payload.get("org_name") or "").strip()
                pallets = float(payload.get("pallets") or 0.0)
                max_pallets = float(payload.get("max_pallets") or 0.0)
                session_id = str(payload.get("session_id") or "local-coord")
                force_split = bool(payload.get("allow_split", False))
                enforce_conflict = bool(payload.get("enforce_conflict", False))

                if not posting_id or not org_name or pallets <= 0:
                    self._send_json(400, {"error": "posting_id, org_name, and pallets > 0 required"})
                    return

                existing_lock = state["posting_locks"].get(posting_id)
                if enforce_conflict and existing_lock and not force_split:
                    if existing_lock.get("session_id") != session_id or existing_lock.get("org_name") != org_name:
                        self._send_json(
                            409,
                            {
                                "error": "LOCK_CONFLICT",
                                "message": (
                                    f"Posting '{posting_id}' is already locked by session "
                                    f"'{existing_lock.get('session_id')}' for '{existing_lock.get('org_name')}' "
                                    f"({existing_lock.get('pallets')}p at {existing_lock.get('locked_at')})."
                                ),
                                "existing_lock": existing_lock,
                                "state": state,
                            },
                        )
                        return

                already_claimed = float(state["claimed_pallets_by_org"].get(org_name, 0.0))
                if enforce_conflict and max_pallets > 0 and (already_claimed + pallets) > max_pallets + 1e-6:
                    self._send_json(
                        409,
                        {
                            "error": "CAPACITY_EXCEEDED",
                            "message": (
                                f"Cannot lock {pallets:g} pallets at '{org_name}': "
                                f"{already_claimed:g} of {max_pallets:g} pallets already reserved today."
                            ),
                            "state": state,
                        },
                    )
                    return

                lock_entry = {
                    "lock_id": f"LOCK-{len(state['reservations']) + 1:03d}",
                    "posting_id": posting_id,
                    "posting_title": str(payload.get("posting_title") or posting_id),
                    "org_name": org_name,
                    "pallets": round(pallets, 2),
                    "session_id": session_id,
                    "locked_at": now_iso,
                }
                state["reservations"].append(lock_entry)
                state["claimed_pallets_by_org"][org_name] = round(already_claimed + pallets, 2)
                state["posting_locks"][posting_id] = lock_entry
                _save_state(state)
                self._send_json(200, {"ok": True, "lock": lock_entry, "state": state})
                return

            if action == "decline":
                posting_id = str(payload.get("posting_id") or "global").strip()
                org_name = str(payload.get("org_name") or "").strip()
                reason = str(payload.get("reason") or "They said no / unavailable").strip()
                session_id = str(payload.get("session_id") or "local-coord")
                if not org_name:
                    self._send_json(400, {"error": "org_name required"})
                    return
                declined_list = state["declined_by_posting"].setdefault(posting_id, [])
                if not any(d.get("org_name") == org_name for d in declined_list):
                    declined_list.append(
                        {
                            "org_name": org_name,
                            "reason": reason,
                            "session_id": session_id,
                            "timestamp": now_iso,
                        }
                    )
                _save_state(state)
                self._send_json(200, {"ok": True, "state": state})
                return

            if action == "release":
                lock_id = payload.get("lock_id")
                posting_id = payload.get("posting_id")
                if payload.get("reset_all"):
                    state = _default_state()
                else:
                    remaining = []
                    for r in state["reservations"]:
                        if (lock_id and r.get("lock_id") == lock_id) or (
                            posting_id and r.get("posting_id") == posting_id
                        ):
                            org = r.get("org_name")
                            p = float(r.get("pallets") or 0.0)
                            cur = float(state["claimed_pallets_by_org"].get(org, 0.0))
                            new_val = round(max(0.0, cur - p), 2)
                            if new_val <= 0:
                                state["claimed_pallets_by_org"].pop(org, None)
                            else:
                                state["claimed_pallets_by_org"][org] = new_val
                            state["posting_locks"].pop(r.get("posting_id"), None)
                        else:
                            remaining.append(r)
                    state["reservations"] = remaining
                _save_state(state)
                self._send_json(200, {"ok": True, "state": state})
                return

            if action == "onboard":
                name = str(payload.get("name") or "").strip()
                profile = payload.get("profile") or {}
                if name:
                    state["onboarded_pantries"][name] = {
                        **profile,
                        "onboarded_at": now_iso,
                    }
                    _save_state(state)
                self._send_json(200, {"ok": True, "state": state})
                return

        self._send_json(400, {"error": "unknown_action"})

    def _ensure_session_from_run_body(self, body: bytes | None, headers: dict):
        if not body:
            return
        try:
            payload = json.loads(body.decode("utf-8"))
            app_name = payload.get("appName", "food_broker")
            user_id = payload.get("userId", "coordinator")
            session_id = payload.get("sessionId")
            if not session_id:
                return
            sess_url = f"{BACKEND_URL}/apps/{app_name}/users/{user_id}/sessions/{session_id}"
            sess_req = urllib.request.Request(
                sess_url, data=b"{}", headers=headers, method="POST"
            )
            with urllib.request.urlopen(sess_req, timeout=15) as _:
                pass
        except Exception:
            pass

    def _proxy(self, method: str):
        target = f"{BACKEND_URL}{self.path}"
        length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(length) if length > 0 else None
        headers = {"Accept": "application/json"}
        if self.headers.get("Content-Type"):
            headers["Content-Type"] = self.headers["Content-Type"]

        # If calling /run, proactively ensure the ADK session exists on Cloud Run
        if method == "POST" and self.path.startswith("/run"):
            self._ensure_session_from_run_body(body, headers)

        req = urllib.request.Request(target, data=body, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                data = resp.read()
                self.send_response(resp.status)
                self.send_header(
                    "Content-Type",
                    resp.headers.get("Content-Type", "application/json"),
                )
                self.end_headers()
                self.wfile.write(data)
        except urllib.error.HTTPError as exc:
            # If Cloud Run routed /run to an instance without the in-memory session (404), recreate and retry once
            if exc.code == 404 and method == "POST" and self.path.startswith("/run"):
                self._ensure_session_from_run_body(body, headers)
                try:
                    retry_req = urllib.request.Request(
                        target, data=body, headers=headers, method=method
                    )
                    with urllib.request.urlopen(retry_req, timeout=120) as resp2:
                        data2 = resp2.read()
                        self.send_response(resp2.status)
                        self.send_header(
                            "Content-Type",
                            resp2.headers.get("Content-Type", "application/json"),
                        )
                        self.end_headers()
                        self.wfile.write(data2)
                        return
                except Exception:
                    pass
            err_body = exc.read()
            self.send_response(exc.code)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(err_body)
        except Exception as exc:  # noqa: BLE001
            self.send_response(502)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            msg = f'{{"error": {{"code": "proxy_error", "message": "{exc}"}}}}'
            self.wfile.write(msg.encode("utf-8"))


if __name__ == "__main__":
    # Bind to 0.0.0.0 when running on Cloud Run (K_SERVICE set) or when HOST is specified; default to 127.0.0.1 locally.
    default_host = "0.0.0.0" if os.environ.get("K_SERVICE") else "127.0.0.1"
    host = os.environ.get("HOST", default_host)
    server = http.server.ThreadingHTTPServer((host, PORT), ConsoleHandler)
    print(f"Coordinator Dispatch Console running at http://{host}:{PORT}")
    print(f"Proxying ADK API calls to {BACKEND_URL}")
    server.serve_forever()
