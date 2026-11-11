"""Serve the static dashboard and refresh configured aggregate sources on localhost."""
import argparse
from datetime import datetime, timezone
from functools import partial
from http.client import HTTPException
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from importlib import import_module
import json
import os
from pathlib import Path
import re
from threading import Lock
from time import monotonic
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener

ROOT = Path(__file__).resolve().parents[1]
MAX_BYTES = 2_000_000
MAX_COUNT = 2**53 - 1
LOOPBACK = {"localhost", "127.0.0.1", "::1"}
funnel = import_module("skills.growth-funnel-diagnosis.scripts.analyze_registration_credit")
lookup = import_module("skills.growth-data-adapter.scripts.build_workspace")._lookup
MAPPED_FIELDS = {
    "provenance.extracted_at", "cohort.registration_start", "cohort.registration_end",
    "cohort.observation_cutoff", *funnel.STAGES,
}


def reject_constant(_):
    raise ValueError("JSON must contain finite values")


def parse_json(data):
    if len(data) > MAX_BYTES:
        raise ValueError("JSON exceeds the 2 MB limit")
    return json.loads(data.decode("utf-8"), object_pairs_hook=funnel._unique_object,
                      parse_constant=reject_constant)


def read_json(path):
    with path.open("rb") as stream:
        return parse_json(stream.read(MAX_BYTES + 1))


def encode_json(value):
    return json.dumps(value, ensure_ascii=False, allow_nan=False).encode("utf-8")


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def fetch_http(url, headers):
    deadline = monotonic() + 15
    opener = build_opener(NoRedirect())
    try:
        with opener.open(Request(url, headers={"Accept": "application/json", **headers}), timeout=5) as response:
            if response.headers.get_content_type() != "application/json":
                raise ValueError("HTTP source must return application/json")
            payload = bytearray()
            while len(payload) <= MAX_BYTES:
                if monotonic() >= deadline:
                    raise ValueError("HTTP source timed out")
                chunk = response.read1(min(65536, MAX_BYTES + 1 - len(payload)))
                if not chunk:
                    break
                payload.extend(chunk)
    except HTTPError as exc:
        raise ValueError(f"HTTP source returned status {exc.code}") from None
    except (URLError, TimeoutError, OSError, HTTPException):
        raise ValueError("HTTP source is unavailable or timed out") from None
    try:
        return parse_json(payload)
    except (ValueError, RecursionError):
        raise ValueError("HTTP source returned invalid JSON or exceeded 2 MB") from None


def source_headers(config):
    name = config.get("bearer_token_env")
    if not name:
        return {}
    token = os.environ.get(name)
    if not token or not re.fullmatch(r"[!-~]+", token):
        raise ValueError("Configured bearer token is missing or invalid")
    return {"Authorization": "Bearer " + token}


def load_sources(path):
    configs = read_json(path)
    if not isinstance(configs, dict) or not configs:
        raise ValueError("configuration must be a nonempty object keyed by source ID")
    for key, config in configs.items():
        if not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,63}", key):
            raise ValueError("source ID must use lowercase letters, digits or hyphens")
        if not isinstance(config, dict) or config.keys() - {
            "label", "transport", "url", "bearer_token_env", "payload_path", "mapping", "tool", "arguments"
        }:
            raise ValueError(f"{key}: unexpected source configuration fields")
        for field in ("label", "url"):
            funnel.require_text(config.get(field), f"{key}.{field}")
        transport = config.get("transport")
        if transport not in ("http", "mcp"):
            raise ValueError(f"{key}: transport must be http or mcp")
        if transport == "mcp":
            funnel.require_text(config.get("tool"), f"{key}.tool")
            if not isinstance(config.get("arguments", {}), dict):
                raise ValueError(f"{key}: MCP arguments must be an object")
        elif {"tool", "arguments"} & config.keys():
            raise ValueError(f"{key}: tool and arguments are for MCP sources")
        url = urlsplit(config["url"])
        if (not url.hostname or url.username is not None or url.password is not None
                or url.fragment or not (url.scheme == "https" or
                (url.scheme == "http" and url.hostname in LOOPBACK))):
            raise ValueError(f"{key}: use HTTPS or loopback HTTP without embedded credentials")
        if url.port == 0:
            raise ValueError(f"{key}: invalid endpoint port")
        if "bearer_token_env" in config and not (
            isinstance(config["bearer_token_env"], str)
            and re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", config["bearer_token_env"])
        ):
            raise ValueError(f"{key}: bearer_token_env must name an environment variable")
        if "payload_path" in config:
            funnel.require_text(config["payload_path"], f"{key}.payload_path")
        if "mapping" in config:
            funnel.require_text(config["mapping"], f"{key}.mapping")
            mapping_path = path.parent / config["mapping"]
            mapping = funnel.fields(read_json(mapping_path), "template field_map", f"{key}.mapping")
            funnel.require_text(mapping["template"], f"{key}.mapping.template")
            if not isinstance(mapping["field_map"], dict) or mapping["field_map"].keys() != MAPPED_FIELDS:
                raise ValueError(f"{key}: map each stage count, all three dates and extracted_at")
            for source_path in mapping["field_map"].values():
                funnel.require_text(source_path, f"{key}.mapping.field_map path")
            mapping["template"] = read_json(mapping_path.parent / mapping["template"])
            config["mapping"] = mapping
    return configs


def normalize(payload, config):
    if "payload_path" in config:
        payload = lookup(payload, config["payload_path"])
    if "mapping" not in config:
        return payload
    mapping = config["mapping"]
    # The template supplies reviewed definitions. All observations come from the source.
    template = mapping["template"]
    paths = mapping["field_map"]
    if not isinstance(template, dict) or not isinstance(template.get("stages"), list):
        raise ValueError("invalid intake template")
    try:
        cohort = {**template["cohort"]}
        provenance = {**template["provenance"]}
        provenance["extracted_at"] = lookup(payload, paths["provenance.extracted_at"])
        for field in ("registration_start", "registration_end", "observation_cutoff"):
            cohort[field] = lookup(payload, paths[f"cohort.{field}"])
        stages = [{**stage, "unique_people": lookup(payload, paths[stage["id"]])}
                  for stage in template["stages"]]
    except (TypeError, KeyError):
        raise ValueError("invalid intake template") from None
    return {**template, "cohort": cohort, "provenance": provenance, "stages": stages}


def build_snapshot(config):
    headers = source_headers(config)
    if config["transport"] == "mcp":
        try:
            from .mcp_source import fetch_mcp
        except ImportError:
            raise ValueError("Install the MCP dependencies from requirements-mcp.txt") from None
        payload = fetch_mcp(config, headers)
        if len(encode_json(payload)) > MAX_BYTES:
            raise ValueError("MCP structured result exceeds 2 MB")
    else:
        payload = fetch_http(config["url"], headers)
    intake = normalize(payload, config)
    report = funnel.analyze_intake(intake)
    if report["counts"]["registered"] > MAX_COUNT:
        raise ValueError("registered count exceeds the dashboard integer limit")
    stages = [{"id": stage["id"], "definition": stage["proposed_definition"]}
              for stage in intake["stages"]]
    return {
        "report": report, "stages": stages, "source": intake["provenance"]["source"],
        "extracted_at": intake["provenance"]["extracted_at"],
        "refreshed_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }


class Sources:
    def __init__(self, configs):
        self.configs = configs
        self.state = {key: {"snapshot": None, "error": None} for key in configs}
        self.locks = {key: Lock() for key in configs}

    def list(self):
        return [{"id": key, "label": config["label"], "transport": config["transport"]}
                for key, config in self.configs.items()]

    def refresh(self, key):
        with self.locks[key]:
            try:
                snapshot = build_snapshot(self.configs[key])
                if len(encode_json(snapshot)) > MAX_BYTES:
                    raise ValueError("Validated snapshot exceeds 2 MB")
            except (ValueError, OverflowError, RecursionError) as exc:
                self.state[key] = {"snapshot": self.state[key]["snapshot"], "error": str(exc)}
                return 502, self.state[key]
            self.state[key] = {"snapshot": snapshot, "error": None}
            return 200, self.state[key]


class DashboardHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, sources, **kwargs):
        self.sources = sources
        super().__init__(*args, **kwargs)

    def list_directory(self, path):
        self.send_error(404)
        return None

    def send_json(self, status, value):
        body = encode_json(value)
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(body)

    def valid_host(self):
        port = self.server.server_port
        return self.headers.get("Host") in {f"127.0.0.1:{port}", f"localhost:{port}"}

    def do_GET(self):
        if not self.valid_host():
            self.send_error(403)
        elif self.path == "/api/sources":
            self.send_json(200, self.sources.list())
        elif self.path.startswith("/api/"):
            key = self.path.removeprefix("/api/sources/")
            if key in self.sources.state:
                self.send_json(200, self.sources.state[key])
            else:
                self.send_json(404, {"error": "Unknown source"})
        else:
            super().do_GET()

    def do_POST(self):
        origin = self.headers.get("Origin")
        if (not self.valid_host() or (origin is not None and origin != "http://" + self.headers["Host"])
                or self.headers.get("Content-Length", "0") != "0" or self.headers.get("Transfer-Encoding")):
            self.send_json(403, {"error": "Refresh requires a local request with no body"})
            return
        match = re.fullmatch(r"/api/sources/([a-z0-9-]+)/refresh", self.path)
        if not match or match[1] not in self.sources.configs:
            self.send_json(404, {"error": "Unknown source"})
            return
        self.send_json(*self.sources.refresh(match[1]))


def create_server(configs, directory, port):
    handler = partial(DashboardHandler, sources=Sources(configs), directory=directory)
    return ThreadingHTTPServer(("127.0.0.1", port), handler)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True, type=Path, help="local source configuration JSON")
    parser.add_argument("--port", type=int, default=4173)
    args = parser.parse_args()
    directory = ROOT / "dashboard/out"
    if not (directory / "index.html").is_file():
        parser.error("build the dashboard first with npm run build")
    try:
        with create_server(load_sources(args.config), directory, args.port) as server:
            print(f"FinGrowth listening on http://127.0.0.1:{server.server_port}", flush=True)
            server.serve_forever()
    except (ValueError, OSError, RecursionError) as exc:
        parser.error(str(exc))
    except KeyboardInterrupt:
        return


if __name__ == "__main__":
    main()
