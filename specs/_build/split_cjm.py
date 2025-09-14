#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MONO = ROOT.parent / "01_CJM_v1.json"
CJM_DIR = ROOT / "01_cjm"
STAGES_DIR = CJM_DIR / "stages"


def read_json(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


def write_json(p: Path, data: dict):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    if not MONO.exists():
        print("No monolith found for CJM; skipping split.")
        return
    mono = read_json(MONO)

    stages = mono.get("cjm", [])
    order = []
    STAGES_DIR.mkdir(parents=True, exist_ok=True)
    for st in stages:
        sid = st.get("id")
        if not sid:
            raise ValueError("CJM stage without id")
        write_json(STAGES_DIR / f"{sid}.json", st)
        order.append(sid)

    index = {
        "$schema": "../_schemas/cjm.schema.json",
        "version": "1.0.0",
        "stages": order
    }
    write_json(CJM_DIR / "index.json", index)
    print(f"Split CJM into {len(order)} stages and updated index.json")


if __name__ == "__main__":
    main()
