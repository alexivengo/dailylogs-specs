#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MONO = ROOT.parent / "00_PRD_v1.json"
PRD_DIR = ROOT / "00_prd"
SECTIONS_DIR = PRD_DIR / "sections"


def read_json(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


def write_json(p: Path, data: dict):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    if not MONO.exists():
        print("No monolith found for PRD; skipping split.")
        return
    mono = read_json(MONO)

    # sections
    sections = mono.get("prd", [])
    order = []
    SECTIONS_DIR.mkdir(parents=True, exist_ok=True)
    for sec in sections:
        sid = sec.get("id")
        if not sid:
            raise ValueError("PRD section without id")
        write_json(SECTIONS_DIR / f"{sid}.json", sec)
        order.append(sid)

    # index
    index = {
        "$schema": "../_schemas/prd.schema.json",
        "version": "1.0.0",
        "sections": order
    }
    write_json(PRD_DIR / "index.json", index)
    print(f"Split PRD into {len(order)} sections and updated index.json")


if __name__ == "__main__":
    main()
