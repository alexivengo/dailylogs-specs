#!/usr/bin/env python3
import json
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parents[1]
MONO = ROOT.parent / "02_UserFlow_v1.json"
UF_DIR = ROOT / "02_userflow"
NODES_DIR = UF_DIR / "nodes"
EDGES_DIR = UF_DIR / "edges"
ANALYTICS_FILE = UF_DIR / "analytics" / "events.json"
DATA_DICT_FILE = UF_DIR / "data_dictionary.json"

# Map node id prefixes to domain files
DOMAIN_MAP = [
    ("project", "projects.json"),
    ("app", "app.json"),
    ("daily", "daily.json"),
    ("day-", "daily.json"),
    ("weather", "weather.json"),
    ("fetch-weather", "weather.json"),
    ("manual-weather", "weather.json"),
    ("entry", "entries.json"),
    ("save-entry", "entries.json"),
    ("error-entry", "entries.json"),
    ("report", "export.json"),
    ("export", "export.json"),
    ("lock-day", "export.json"),
    ("documents", "documents.json"),
    ("gallery", "gallery.json"),
    ("camera", "gallery.json"),
    ("capture-photo", "gallery.json"),
    ("cancel-out", "app.json"),
    ("success-done", "app.json"),
]


def choose_domain(node_id: str) -> str:
    for prefix, fname in DOMAIN_MAP:
        if node_id.startswith(prefix):
            return fname
    return "misc.json"


def load_monolith():
    with MONO.open("r", encoding="utf-8") as f:
        return json.load(f)


def ensure_dirs():
    (UF_DIR / "analytics").mkdir(parents=True, exist_ok=True)
    NODES_DIR.mkdir(parents=True, exist_ok=True)
    EDGES_DIR.mkdir(parents=True, exist_ok=True)


def collect(mod):
    nodes_by_file = defaultdict(list)
    events = set()
    io_keys = set()

    for node in mod.get("user_flow", []):
        node_id = node.get("id", "")
        # Collect analytics events
        for key in ("analytics",):
            for ev in node.get(key, []) or []:
                if isinstance(ev, str):
                    events.add(ev)
        # inputs/outputs
        for k in node.get("inputs", []) or []:
            if isinstance(k, str):
                io_keys.add(k)
        for k in node.get("outputs", []) or []:
            if isinstance(k, str):
                io_keys.add(k)
        # Edges: collect analytics too
        for e in node.get("edges", []) or []:
            for ev in e.get("analytics", []) or []:
                if isinstance(ev, str):
                    events.add(ev)
        # Group by domain file
        dom_file = choose_domain(node_id)
        nodes_by_file[dom_file].append(node)

    return nodes_by_file, sorted(events), sorted(io_keys)


def write_nodes(nodes_by_file):
    for fname, items in nodes_by_file.items():
        out = NODES_DIR / fname
        data = {
            "version": "1.1.0",
            "domain": fname.replace(".json", ""),
            "nodes": items,
        }
        out.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def merge_events(new_events):
    # If events.json exists, merge and sort unique
    prev = {"version": "1.1.0", "events": []}
    if ANALYTICS_FILE.exists():
        try:
            prev = json.loads(ANALYTICS_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    merged = sorted(set(prev.get("events", [])) | set(new_events))
    ANALYTICS_FILE.write_text(json.dumps({"version": "1.1.0", "events": merged}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_data_dictionary(io_keys):
    # Keep existing structure if present; otherwise write a flat extracted view
    if DATA_DICT_FILE.exists():
        try:
            existing = json.loads(DATA_DICT_FILE.read_text(encoding="utf-8"))
        except Exception:
            existing = {"version": "1.1.0", "entities": {}}
    else:
        existing = {"version": "1.1.0", "entities": {}}
    existing["extracted_keys"] = sorted(io_keys)
    DATA_DICT_FILE.write_text(json.dumps(existing, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    ensure_dirs()
    mod = load_monolith()
    nodes_by_file, events, io_keys = collect(mod)
    write_nodes(nodes_by_file)
    merge_events(events)
    write_data_dictionary(io_keys)
    print(f"Split nodes into {len(nodes_by_file)} domain files; events: {len(events)}; io keys: {len(io_keys)}")


if __name__ == "__main__":
    main()
