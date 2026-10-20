#!/usr/bin/env python3
"""Local static server + CORS proxy for the Chicago Food Rescue Coordinator Dispatch Console.

Serves `frontend/index.html` at http://127.0.0.1:8090 (loopback only) and proxies `/apps/*`, `/run`, `/run_sse`,
`/list-apps`, and `/health` to the deployed Cloud Run service (`A4I_BACKEND_URL`) so browser requests
succeed even when `A4I_ALLOW_ORIGINS` is not set on Cloud Run.

Usage:
    python3 frontend/serve.py
"""

import http.server
import json
import os
import pathlib
import urllib.error
import urllib.request

PORT = int(os.environ.get("PORT", "8090"))
BACKEND_URL = os.environ.get(
    "A4I_BACKEND_URL", "https://food-broker-817377390808.us-east1.run.app"
).rstrip("/")
FRONTEND_DIR = pathlib.Path(__file__).resolve().parent
PROXY_PREFIXES = ("/apps/", "/run", "/run_sse", "/list-apps", "/health")


class ConsoleHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(FRONTEND_DIR), **kwargs)

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(204)
        self.end_headers()

    def do_GET(self):
        if self.path.startswith(PROXY_PREFIXES):
            self._proxy("GET")
            return
        super().do_GET()

    def do_POST(self):
        if self.path.startswith(PROXY_PREFIXES):
            self._proxy("POST")
            return
        self.send_error(405, "Method Not Allowed")

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
