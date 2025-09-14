#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MONO = ROOT.parent / "05_HIG_Pattern_selection_v1.json"
HIG_DIR = ROOT / "05_hig"
STORIES_DIR = HIG_DIR / "stories"


def read_json(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


def write_json(p: Path, data: dict):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    if not MONO.exists():
        print("No monolith found for HIG; skipping split.")
        return
    mono = read_json(MONO)

    # Create index.json with governing_rules and source_files
    index = {
        "$schema": "../_schemas/hig_candidates.schema.json",
        "version": "1.0.0",
        "governing_rules": mono.get("governing_rules", {}),
        "source_files": list(mono.get("source_files", {}).values()),
        "stories": {}
    }

    STORIES_DIR.mkdir(parents=True, exist_ok=True)

    # Split each story block into stories/us-*/candidates.json
    for story in mono.get("stories", []):
        sid = story.get("story_id")
        if not sid:
            raise ValueError("HIG story missing story_id")
        out = {
            "$schema": "../../_schemas/hig_story_candidates.schema.json",
            "story_id": sid,
            "title": story.get("title"),
            "role": story.get("role"),
            "value": story.get("value"),
            "core_actions": story.get("core_actions", []),
            "candidates": story.get("candidates", []),
            "recommendation": story.get("recommendation", {})
        }
        write_json(STORIES_DIR / sid / "candidates.json", out)
        index["stories"][sid] = {"path": f"stories/{sid}/candidates.json"}

    write_json(HIG_DIR / "index.json", index)
    print(f"Split HIG into {len(index['stories'])} per-story candidates and index.json.")


if __name__ == "__main__":
    main()
