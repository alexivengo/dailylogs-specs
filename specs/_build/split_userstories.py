#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MONO = ROOT.parent / "04_UserStories_v1.json"
US_DIR = ROOT / "04_userstories"
US_ITEMS = US_DIR / "us"


def read_json(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


def write_json(p: Path, data: dict):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    if not MONO.exists():
        print("No monolith found for user stories; skipping split.")
        return
    mono = read_json(MONO)

    # Extract epics into index.json
    epics = mono.get("epics", [])
    idx = read_json(US_DIR / "index.json") if (US_DIR / "index.json").exists() else {
        "$schema": "../_schemas/user_story.schema.json",
        "version": "1.0.0",
        "epics": {},
        "stories": []
    }
    # normalize epics structure: map epic_id -> title
    idx_epics = {}
    for e in epics:
        eid = e.get("epic_id")
        if eid:
            idx_epics[eid] = {"title": e.get("title"), "desc": e.get("desc")}
    idx["epics"] = idx_epics

    # Split stories to us/us-*.json and fill index stories list
    stories = mono.get("stories", [])
    US_ITEMS.mkdir(parents=True, exist_ok=True)
    idx["stories"] = []
    for s in stories:
        sid = s.get("story_id")
        if not sid:
            raise ValueError("Story without story_id")
        write_json(US_ITEMS / f"{sid}.json", s)
        idx["stories"].append(sid)

    write_json(US_DIR / "index.json", idx)
    print(f"Split {len(stories)} stories and {len(epics)} epics into modules.")


if __name__ == "__main__":
    main()
