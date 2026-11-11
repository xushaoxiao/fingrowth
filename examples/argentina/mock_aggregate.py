"""Serve an invented Argentina registration-to-credit aggregate over HTTP."""
import argparse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def aggregate():
    return json.loads((HERE / "aggregate.json").read_text(encoding="utf-8"))


class AggregateHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != "/registration-credit":
            self.send_error(404)
            return
        body = json.dumps(aggregate(), ensure_ascii=False).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=4181)
    args = parser.parse_args()
    with ThreadingHTTPServer(("127.0.0.1", args.port), AggregateHandler) as server:
        print(f"Mock Argentina HTTP source on port {server.server_port}", flush=True)
        server.serve_forever()
