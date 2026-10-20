#!/usr/bin/env python3
"""Local static server + CORS proxy for the Chicago Food Rescue Coordinator Dispatch Console.

Serves `frontend/index.html` at http://127.0.0.1:8090 (loopback only) and proxies `/apps/*`, `/run`, `/run_sse`,
`/list-apps`, and `/health` to the deployed Cloud Run service (`A4I_BACKEND_URL`) so browser requests
succeed even when `A4I_ALLOW_ORIGINS` is not set on Cloud Run.

Usage:
    python3 frontend/serve.py
"""

import http.server
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

    def _proxy(self, method: str):
        target = f"{BACKEND_URL}{self.path}"
        length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(length) if length > 0 else None
        headers = {"Accept": "application/json"}
        if self.headers.get("Content-Type"):
            headers["Content-Type"] = self.headers["Content-Type"]

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
    # Loopback only, so other machines on the network cannot use this as an open relay.
    server = http.server.ThreadingHTTPServer(("127.0.0.1", PORT), ConsoleHandler)
    print(f"Coordinator Dispatch Console running at http://127.0.0.1:{PORT}")
    print(f"Proxying ADK API calls to {BACKEND_URL}")
    server.serve_forever()
