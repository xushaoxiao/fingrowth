import json
import os
from importlib.util import find_spec
from pathlib import Path
import socket
import tempfile
from threading import Thread
from time import monotonic, sleep
import unittest
from unittest.mock import patch
from urllib.error import HTTPError
from urllib.request import Request, urlopen
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from examples.argentina.mock_aggregate import AggregateHandler
from scripts.serve_dashboard import create_server, load_sources

ROOT = Path(__file__).resolve().parents[1]
DEMO = ROOT / "examples/argentina"


def start(test, server):
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    test.addCleanup(server.server_close)
    test.addCleanup(server.shutdown)
    return f"http://127.0.0.1:{server.server_port}"


def request(url, method="GET", headers=None):
    try:
        response = urlopen(Request(url, method=method, headers=headers or {}), timeout=20)
    except HTTPError as exc:
        response = exc
    with response:
        return response.status, json.load(response)


class ConnectedFunnelTest(unittest.TestCase):
    def test_http_refresh_and_preservation_of_last_valid_snapshot(self):
        data = json.loads((DEMO / "aggregate.json").read_text())

        class Aggregate(BaseHTTPRequestHandler):
            def do_GET(self):
                if self.headers.get("Authorization") != "Bearer synthetic-test-token":
                    self.send_error(401)
                    return
                body = json.dumps(data).encode()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def log_message(self, *_):
                pass

        upstream = start(self, ThreadingHTTPServer(("127.0.0.1", 0), Aggregate))
        with tempfile.TemporaryDirectory() as temp, patch.dict(os.environ, {"FG_TEST_TOKEN": "synthetic-test-token"}):
            path = Path(temp) / "sources.json"
            config = json.loads((DEMO / "sources.json").read_text())["argentina-http"]
            config.update(url=upstream, bearer_token_env="FG_TEST_TOKEN")
            config["mapping"] = str(DEMO / "mapping.json")
            path.write_text(json.dumps({"argentina-http": config}))
            dashboard = start(self, create_server(load_sources(path), temp, 0))
            endpoint = dashboard + "/api/sources/argentina-http"
            status, sources = request(dashboard + "/api/sources")
            self.assertEqual((status, sources[0]["id"], sources[0]["transport"]), (200, "argentina-http", "http"))
            self.assertNotIn("url", sources[0])
            self.assertIsNone(request(endpoint)[1]["snapshot"])
            self.assertEqual(request(endpoint + "/refresh", "POST", {"Origin": "https://other.example"})[0], 403)
            status, result = request(endpoint + "/refresh", "POST")
            self.assertEqual(status, 200)
            report = result["snapshot"]["report"]
            self.assertEqual(list(report["counts"].values()), [1000, 700, 560, 280, 224])
            self.assertEqual(report["cumulative_conversion"]["credit_approved"], 0.224)
            self.assertEqual(report["cohort"]["observation_cutoff"], "2026-02-07")
            data["people"]["credit_decision_approved"] = 200
            status, updated = request(endpoint + "/refresh", "POST")
            self.assertEqual(status, 200)
            self.assertEqual(updated["snapshot"]["report"]["counts"]["credit_approved"], 200)
            data["people"]["credit_decision_approved"] = 999
            status, failed = request(endpoint + "/refresh", "POST")
            self.assertEqual(status, 502)
            self.assertIn("nested integer", failed["error"])
            self.assertEqual(failed["snapshot"], updated["snapshot"])
            self.assertEqual(request(endpoint), (200, failed))


    @unittest.skipUnless(find_spec("mcp"), "Install requirements-mcp.txt for Streamable HTTP acceptance")
    def test_mcp_matches_http_using_the_same_mapping(self):
        import uvicorn
        from examples.argentina.mock_mcp import server

        app = server.streamable_http_app(json_response=True, stateless_http=True)
        mcp = uvicorn.Server(uvicorn.Config(app, log_level="error"))
        listener = socket.socket()
        self.addCleanup(listener.close)
        listener.bind(("127.0.0.1", 0))
        port = listener.getsockname()[1]
        thread = Thread(target=mcp.run, kwargs={"sockets": [listener]}, daemon=True)

        def stop():
            mcp.should_exit = True
            thread.join(timeout=5)

        thread.start()
        self.addCleanup(stop)
        deadline = monotonic() + 5
        while not mcp.started and thread.is_alive() and monotonic() < deadline:
            sleep(0.02)
        self.assertTrue(mcp.started)
        http = start(self, ThreadingHTTPServer(("127.0.0.1", 0), AggregateHandler))
        configs = load_sources(DEMO / "sources.json")
        configs["argentina-http"]["url"] = http + "/registration-credit"
        configs["argentina-mcp"]["url"] = f"http://127.0.0.1:{port}/mcp"
        with tempfile.TemporaryDirectory() as temp:
            dashboard = start(self, create_server(configs, temp, 0))
            endpoint = dashboard + "/api/sources/argentina-"
            _, sources = request(dashboard + "/api/sources")
            self.assertEqual([source["transport"] for source in sources], ["http", "mcp"])
            snapshots = []
            for transport in ("http", "mcp"):
                status, result = request(endpoint + transport + "/refresh", "POST")
                self.assertEqual(status, 200, result)
                snapshots.append({k: v for k, v in result["snapshot"].items() if k != "refreshed_at"})
            self.assertEqual(snapshots[0], snapshots[1])
            stop()
            status, failed = request(endpoint + "mcp/refresh", "POST")
            self.assertEqual(status, 502)
            self.assertEqual(failed["snapshot"]["report"], snapshots[0]["report"])


if __name__ == "__main__":
    unittest.main()
