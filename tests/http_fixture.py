"""A generic, in-process HTTP memory fixture for testing HttpMemoryAdapter.

This is not a real memory store — it's a disposable stdlib HTTP server that
implements the add/search contract documented in zer0lint/http_adapter.py, so
adapter tests exercise real request/response plumbing (headers, JSON framing,
status codes) without ever contacting mem0, fidelis, or any other live service.

Each test gets its own server bound to an ephemeral localhost port and torn
down at the end of the `with` block — nothing persists between tests or
outside this process.
"""

from __future__ import annotations

import json
import threading
from contextlib import contextmanager
from http.server import BaseHTTPRequestHandler, HTTPServer


class _Handler(BaseHTTPRequestHandler):
    # Shared in-memory store, keyed by user_id -> list of {"text": ...}.
    store: dict[str, list[dict]] = {}
    response_shape = "mem0"  # which _normalize_results() shape to emit

    def log_message(self, *args) -> None:  # silence stdlib access logs
        pass

    def _read_json(self) -> dict:
        length = int(self.headers.get("Content-Length", 0))
        return json.loads(self.rfile.read(length) or b"{}")

    def _write_json(self, status: int, payload: object) -> None:
        body = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self) -> None:  # noqa: N802 (stdlib method name)
        payload = self._read_json()
        uid = payload.get("user_id", "default")

        if self.path == "/add":
            _Handler.store.setdefault(uid, []).append({"text": payload.get("text", "")})
            self._write_json(200, {"status": "ok"})
            return

        if self.path == "/search":
            items = [m["text"] for m in _Handler.store.get(uid, [])]
            shape = _Handler.response_shape
            if shape == "mem0":
                self._write_json(200, {"results": [{"memory": t} for t in items]})
            elif shape == "list":
                self._write_json(200, items)
            elif shape == "hits":
                self._write_json(200, {"hits": [{"text": t} for t in items]})
            else:
                raise ValueError(f"unknown response_shape: {shape}")
            return

        if self.path == "/error":
            self._write_json(500, {"error": "boom"})
            return

        self._write_json(404, {"error": "not found"})


@contextmanager
def generic_http_memory_fixture(response_shape: str = "mem0"):
    """
    Start a disposable local HTTP memory server for the duration of the `with` block.

    Yields (add_url, search_url). The server and its in-memory store are
    destroyed on exit — nothing is written outside this process.
    """
    _Handler.store = {}
    _Handler.response_shape = response_shape

    server = HTTPServer(("127.0.0.1", 0), _Handler)
    port = server.server_address[1]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        base = f"http://127.0.0.1:{port}"
        yield f"{base}/add", f"{base}/search"
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)
