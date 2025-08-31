#!/usr/bin/python

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
    def do_POST(self):
        key = self.path.strip("/").split("/")[-1]

        if len(key) == 0:
            self.send_response(400)
            return

        length = int(self.headers["Content-Length"])
        data = self.rfile.read(length)

        os.makedirs(DATA_DIR, exist_ok=True)
        with open(f"{DATA_DIR}/{key}", "wb") as fout:
            fout.write(data)

        self.send_response(200)

    def do_GET(self):
        key = self.path.strip("/").split("/")[-1]

        if len(key) == 0:
            self.send_response(400)
            return

        try:
            data = open(f"{DATA_DIR}/{key}", "rb").read()
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(data)

        except FileNotFoundError:
            self.send_response(404)


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "config.json"), "r") as f:
        config = json.load(f)

    DATA_DIR = config.get("data_dir", "data")

    PORT = config.get("port", 8000)
    print(f"Starting server on port {PORT}")
    HTTPServer(("", PORT), Server).serve_forever()
