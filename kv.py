#!/usr/bin/python3

"""
Self-hosted key-value store with a REST API.

Usage:
    python kv.py

Client-side:
    curl -X POST http://<host>/<key> -d "value"
    curl -X GET http://<host>/<key>
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import json

class Server(BaseHTTPRequestHandler):
    def _set_headers(self, status=200, content_type="text/plain"):
        """Helper to send basic headers + CORS."""
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_OPTIONS(self):
        """Handle CORS preflight requests."""
        self._set_headers(200)

    def do_POST(self):
        key = self.path.strip("/").split("/")[-1]
        if len(key) == 0:
            self._set_headers(400)
            self.wfile.write(b"Missing key")
            return

        length = int(self.headers.get("Content-Length", 0))
        data = self.rfile.read(length)

        os.makedirs(DATA_DIR, exist_ok=True)
        with open(f"{DATA_DIR}/{key}", "wb") as fout:
            fout.write(data)

        self._set_headers(200)
        self.wfile.write(b"OK")

    def do_GET(self):
        key = self.path.strip("/").split("/")[-1]
        if len(key) == 0:
            self._set_headers(400)
            self.wfile.write(b"Missing key")
            return

        try:
            with open(f"{DATA_DIR}/{key}", "rb") as f:
                data = f.read()
            self._set_headers(200)
            self.wfile.write(data)

        except FileNotFoundError:
            self._set_headers(404)
            self.wfile.write(b"Not found")


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "config.json"), "r") as f:
        config = json.load(f)

    DATA_DIR = config.get("data_dir", "data")
    PORT = config.get("port", 8000)

    print(f"Starting server on port {PORT}")
    HTTPServer(("", PORT), Server).serve_forever()
