#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MONO = ROOT.parent / "03_Global_UX_Principles_v1.json"
UX_DIR = ROOT / "03_ux_principles"
PRINC_DIR = UX_DIR / "principles"


def read_json(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


def write_json(p: Path, data: dict):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    if not MONO.exists():
        print("No monolith found for principles; skipping split.")
        return
    mono = read_json(MONO)

    # Split principles
    principles = mono.get("principles", [])
    PRINC_DIR.mkdir(parents=True, exist_ok=True)
    for pr in principles:
        pid = pr.get("id")
        if not pid:
            raise ValueError("Principle without id in monolith")
        write_json(PRINC_DIR / f"{pid}.json", pr)

    # Antipatterns registry
    if "antipatterns_registry" in mono:
        write_json(UX_DIR / "antipatterns_registry.json", {"items": mono["antipatterns_registry"]})

    # Aliases
    if "aliases" in mono:
        write_json(UX_DIR / "aliases.json", {"aliases": mono["aliases"]})

    # Conflicts, open questions, acceptance checklist
    for key in ["conflicts", "open_questions", "acceptance_checklist"]:
        if key in mono:
            write_json(UX_DIR / f"{key}.json", mono[key])

    print(f"Split {len(principles)} principles and registries from monolith.")


if __name__ == "__main__":
    main()
