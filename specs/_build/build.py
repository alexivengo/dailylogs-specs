#!/usr/bin/env python3
import json
import shutil
from pathlib import Path
from typing import Dict, List, Set, Tuple
import re

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "_build"

# No legacy pass-through: specs/_build is the only artifact location
LEGACY_SOURCES: list = []


def ensure_out():
    OUT.mkdir(parents=True, exist_ok=True)


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def copy_legacy():
    # Deprecated: kept as a no-op to avoid breaking logs; returns empty list
    return []


# --------------------------
# IDs LOCK (machine-readable)
# --------------------------
def read_ids_lock() -> dict:
    lock_json = ROOT.parent / "IDs_LOCK.json"
    if lock_json.exists():
        return read_json(lock_json)
    # fallback: empty structure
    return {
        "policy": {"append_only": True},
        "ids": {
            "prd": {"sections": []},
            "cjm": {"stages": []},
            "userflow": {"nodes": [], "edges": [], "events": []},
            "ctxux": {"screens": []},
            "ux": {"principles": []}
        },
        "status": {}
    }


def ensure_in_ids(lock: dict, category: str, kind: str, _id: str):
    lock.setdefault("ids", {}).setdefault(category, {}).setdefault(kind, [])
    if _id not in lock["ids"][category][kind]:
        lock["ids"][category][kind].append(_id)
    # Track status per ID (append-only policy); namespaced key prevents collisions
    status_key = f"{category}:{kind}:{_id}"
    lock.setdefault("status", {})
    if status_key not in lock["status"]:
        lock["status"][status_key] = {"status": "active"}


def write_ids_lock(lock: dict):
    path = ROOT.parent / "IDs_LOCK.json"
    write_json(path, lock)


# --------------------------
# Basic Validators (schema-like)
# --------------------------
KEBAB = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SNAKE = re.compile(r"^[a-z0-9]+(?:_[a-z0-9]+)*$")


def require(cond: bool, msg: str):
    if not cond:
        raise ValueError(msg)


def validate_userflow_nodes_pack(pack: dict, fname: str):
    require(isinstance(pack.get("version"), str), f"userflow nodes pack {fname} missing version")
    require(isinstance(pack.get("domain"), str), f"userflow nodes pack {fname} missing domain")
    for n in pack.get("nodes", []) or []:
        nid = n.get("id")
        require(bool(nid) and KEBAB.match(nid), f"node id must be kebab-case in {fname}")
        ntype = n.get("type")
        require(ntype in {"screen", "system", "decision", "error", "terminator"}, f"node type invalid for {nid}")
        for ev in n.get("analytics", []) or []:
            require(SNAKE.match(ev), f"node {nid} analytics event not snake_case: {ev}")
        for e in n.get("edges", []) or []:
            eid = e.get("id")
            require(bool(eid) and KEBAB.match(eid), f"edge id must be kebab-case in node {nid}")
            for ev in e.get("analytics", []) or []:
                require(SNAKE.match(ev), f"edge {eid} analytics event not snake_case: {ev}")


def validate_userflow_events(reg: dict):
    require(isinstance(reg.get("version"), str), "analytics/events.json missing version")
    for ev in reg.get("events", []) or []:
        require(SNAKE.match(ev), f"event not snake_case: {ev}")


def validate_ctxux_screen(scr: dict, sid_hint: str):
    sid = scr.get("id") or sid_hint
    require(bool(sid) and KEBAB.match(sid), f"ctxux screen id invalid: {sid}")
    require(bool(scr.get("title")), f"ctxux screen {sid} missing title")
    for lp in scr.get("local_principles", []) or []:
        for ev in lp.get("telemetry", []) or []:
            require(SNAKE.match(ev), f"ctxux {sid} telemetry not snake_case: {ev}")


def validate_prd_section(sec: dict, sid: str):
    require(sec.get("id") == sid, f"PRD section id mismatch: {sid}")
    require(bool(sec.get("title")), f"PRD section {sid} missing title")


def validate_cjm_stage(st: dict, sid: str):
    require(st.get("id") == sid, f"CJM stage id mismatch: {sid}")
    require(bool(st.get("title")), f"CJM stage {sid} missing title")


# --------------------------
# 02 UserFlow assembly
# --------------------------
def assemble_userflow(lock: dict) -> dict:
    idx = read_json(ROOT / "02_userflow" / "index.json")
    # Load registry files
    events_reg = read_json(ROOT / "02_userflow" / "analytics" / "events.json")
    validate_userflow_events(events_reg)
    data_dict = read_json(ROOT / "02_userflow" / "data_dictionary.json")
    nodes_dir = ROOT / "02_userflow" / "nodes"

    # Collect nodes from domain files
    node_objs: List[dict] = []
    for path in sorted(nodes_dir.glob("*.json")):
        dom_pack = read_json(path)
        validate_userflow_nodes_pack(dom_pack, path.name)
        for n in dom_pack.get("nodes", []):
            node_objs.append(n)

    # Validations
    node_ids: Set[str] = set()
    edge_ids: Set[str] = set()
    events_set: Set[str] = set(events_reg.get("events", []))

    def dd_has(key: str) -> bool:
        if not key:
            return False
        # simplistic: search in entity properties across dictionary
        entities = data_dict.get("entities", {})
        for ent in entities.values():
            props = ent.get("properties", {})
            if key in props.keys():
                return True
        # also allow top-level extracted_keys for now
        if key in data_dict.get("extracted_keys", []):
            return True
        return False

    # Coverage: ensure every declared io key (extracted_keys) appears at least once in outputs across nodes
    all_outputs: Set[str] = set()

    # Collect PRD/CJM ids from IDs lock for cross-refs
    prd_ids = set(lock.get("ids", {}).get("prd", {}).get("sections", []))
    cjm_ids = set(lock.get("ids", {}).get("cjm", {}).get("stages", []))

    # Node uniqueness and collect
    for n in node_objs:
        nid = n.get("id")
        if not nid:
            raise ValueError("userflow node missing id")
        if nid in node_ids:
            raise ValueError(f"duplicate userflow node id: {nid}")
        node_ids.add(nid)
        ensure_in_ids(lock, "userflow", "nodes", nid)

    # Edges validation embedded in nodes; derive from = current node id
    for n in node_objs:
        src = n.get("id")
        for e in n.get("edges", []) or []:
            eid = e.get("id")
            if not eid:
                raise ValueError(f"edge without id in node {src}")
            if eid in edge_ids:
                raise ValueError(f"duplicate edge id: {eid}")
            edge_ids.add(eid)
            ensure_in_ids(lock, "userflow", "edges", eid)
            # target must exist
            tgt = e.get("target")
            if tgt not in node_ids:
                raise ValueError(f"edge {eid} targets unknown node: {tgt}")
            # analytics events must be registered
            for ev in e.get("analytics", []) or []:
                if ev not in events_set:
                    raise ValueError(f"edge {eid} uses unknown analytics event: {ev}")

        # node-level analytics
        for ev in n.get("analytics", []) or []:
            if ev not in events_set:
                raise ValueError(f"node {src} uses unknown analytics event: {ev}")

        # outputs should be described in data dictionary, if defined
        for outk in n.get("outputs", []) or []:
            if isinstance(outk, str) and not dd_has(outk):
                # soft-warn via exception message for now
                # raise ValueError(f"node {src} output not in data dictionary: {outk}")
                pass
            if isinstance(outk, str):
                all_outputs.add(outk)

        # cross-ref: PRD/CJM references inside refs[] like "PRD:#4_2", "CJM:#daily-logging"
        for ref in n.get("refs", []) or []:
            if isinstance(ref, str) and ref.startswith("PRD:#"):
                rid = ref.split("PRD:#", 1)[1]
                if rid not in prd_ids:
                    raise ValueError(f"node {src} references unknown PRD section: {rid}")
            if isinstance(ref, str) and ref.startswith("CJM:#"):
                cid = ref.split("CJM:#", 1)[1]
                if cid not in cjm_ids:
                    raise ValueError(f"node {src} references unknown CJM stage: {cid}")

    # data dictionary coverage hard check: each REQUIRED io key from extracted_keys should appear in outputs somewhere
    required_dd_keys: Set[str] = set()
    for item in data_dict.get("extracted_keys", []) or []:
        if isinstance(item, dict):
            name = item.get("name")
            cov = (item.get("coverage") or "required").lower()
            if name and cov == "required":
                required_dd_keys.add(name)
        elif isinstance(item, str):
            required_dd_keys.add(item)
    unused = sorted([k for k in required_dd_keys if k not in all_outputs])
    if unused:
        raise ValueError(f"data_dictionary keys not used in any node outputs: {', '.join(unused)}")

    # Build monolith structure
    # Prefer meta from index; fall back to legacy monolith to keep output stable
    meta = idx.get("meta")
    if not meta:
        legacy = ROOT.parent / "02_UserFlow_v1.json"
        if legacy.exists():
            meta = read_json(legacy).get("meta")

    # Convert data_dictionary to validator-friendly array format with coverage
    dd_array: List[dict] = []
    # include extracted_keys first for explicit IO
    for item in data_dict.get("extracted_keys", []) or []:
        if isinstance(item, dict):
            name = item.get("name")
            if not name:
                continue
            cov = item.get("coverage") or "required"
            dd_array.append({"name": name, "coverage": cov})
        else:
            dd_array.append({"name": item, "coverage": "required"})
    # include all entity.properties keys as optional by default
    for ent in (data_dict.get("entities", {}) or {}).values():
        for k in (ent.get("properties", {}) or {}).keys():
            dd_array.append({"name": k, "coverage": "optional"})

    assembled = {
        "version": idx.get("version", "v1.1.0"),
        "meta": meta or {},
        "user_flow": node_objs,
        "data_dictionary": dd_array,
    }

    # ensure all events are recorded in IDs lock
    for ev in sorted(events_set):
        ensure_in_ids(lock, "userflow", "events", ev)

    return assembled


def write_userflow_monolith(lock: dict):
    assembled = assemble_userflow(lock)
    write_json(OUT / "02_UserFlow_v1.json", assembled)
    return assembled


# --------------------------
# 06 Contextual UX assembly
# --------------------------
def assemble_ctxux(lock: dict, userflow_ctx: dict) -> dict:
    idx = read_json(ROOT / "06_ctxux" / "index.json")
    screens_dir = ROOT / "06_ctxux" / "screens"
    screens: List[dict] = []
    # Build validation context from userflow
    uf_nodes: Set[str] = set()
    uf_events: Set[str] = set()
    if userflow_ctx:
        for n in userflow_ctx.get("user_flow", []):
            nid = n.get("id")
            if nid:
                uf_nodes.add(nid)
        # try to get events from the registry file
        events_reg_path = ROOT / "02_userflow" / "analytics" / "events.json"
        if events_reg_path.exists():
            try:
                uf_events = set(read_json(events_reg_path).get("events", []))
            except Exception:
                uf_events = set()
    if screens_dir.exists():
        for path in sorted(screens_dir.glob("*.json")):
            s = read_json(path)
            validate_ctxux_screen(s, path.stem)
            sid = s.get("id")
            if sid:
                ensure_in_ids(lock, "ctxux", "screens", sid)
            if userflow_ctx:
                id = s.get("id")
                if sid:
                    ensure_in_ids(lock, "ctxux", "screens", sid)
            # Validate refs to UserFlow nodes
            for nid in (s.get("refs", {}).get("UserFlow", []) or []):
                if nid not in uf_nodes:
                    raise ValueError(f"ctxux screen {sid} references unknown UserFlow node: {nid}")
            # Validate telemetry events exist in userflow registry
            for lp in s.get("local_principles", []) or []:
                for ev in lp.get("telemetry", []) or []:
                    if ev not in uf_events:
                        raise ValueError(f"ctxux screen {sid} telemetry event not in registry: {ev}")
            screens.append(s)
    # Flatten local principles from all screens to a single root list (preserve screen_id)
    flat_local_principles: List[dict] = []
    for s in screens:
        sid = s.get("id")
        for lp in s.get("local_principles", []) or []:
            lp_copy = dict(lp)
            lp_copy.setdefault("screen_id", sid)
            # derive global_principle_ids from local principle, or screen refs
            if not lp_copy.get("global_principle_ids"):
                gp = []
                gp.extend(lp_copy.get("related_principles", []) or [])
                gp.extend((s.get("refs", {}) or {}).get("GlobalPrinciple", []) or [])
                # de-dup preserve order
                seen = set(); gp2 = []
                for x in gp:
                    if isinstance(x, str) and x not in seen:
                        seen.add(x); gp2.append(x)
                if gp2:
                    lp_copy["global_principle_ids"] = gp2
            # derive user_story_ids from local principle or screen refs
            if not lp_copy.get("user_story_ids"):
                us = []
                us.extend(lp_copy.get("user_story_ids", []) or [])
                us.extend((s.get("refs", {}) or {}).get("UserStory", []) or [])
                seen2 = set(); us2 = []
                for x in us:
                    if isinstance(x, str) and x not in seen2:
                        seen2.add(x); us2.append(x)
                if us2:
                    lp_copy["user_story_ids"] = us2
            # lock local principle id
            lpid = lp_copy.get("id")
            if isinstance(lpid, str):
                ensure_in_ids(lock, "ctxux", "local_principles", lpid)
            flat_local_principles.append(lp_copy)

    assembled = {
        "version": idx.get("version", "1.0.1"),
        "meta": idx.get("meta", {}),
        "screens": screens,
        "local_principles": flat_local_principles,
    }
    # Attach shared lists if exist
    for name in ["conflicts", "accessibility_review", "acceptance_checklist", "open_questions"]:
        path = ROOT / "06_ctxux" / f"{name}.json"
        if path.exists():
            assembled[name] = read_json(path)
    return assembled


def write_ctxux_monolith(lock: dict, userflow_ctx: dict):
    assembled = assemble_ctxux(lock, userflow_ctx)
    write_json(OUT / "06_Contextual_UX_Guidelines_v1.json", assembled)
    return True


"""
---------------------------
 03 Global UX Principles
---------------------------
"""
def assemble_ux_principles(lock: dict) -> dict:
    ux_root = ROOT / "03_ux_principles"
    index_path = ux_root / "index.json"
    idx = read_json(index_path) if index_path.exists() else {}
    # Load principles from directory
    princip_dir = ux_root / "principles"
    principles: List[dict] = []
    if princip_dir.exists():
        for path in sorted(princip_dir.glob("*.json")):
            p = read_json(path)
            pid = p.get("id")
            if not pid:
                raise ValueError(f"ux principle missing id in {path.name}")
            principles.append(p)
    # Build set of canonical IDs
    canonical_ids: Set[str] = set()
    for p in principles:
        pid = p.get("id")
        if pid in canonical_ids:
            raise ValueError(f"duplicate ux principle id: {pid}")
        canonical_ids.add(pid)
        ensure_in_ids(lock, "ux", "principles", pid)

    # Load registries
    ap_path = ux_root / "antipatterns_registry.json"
    aliases_path = ux_root / "aliases.json"
    conflicts_path = ux_root / "conflicts.json"
    openq_path = ux_root / "open_questions.json"
    acc_path = ux_root / "acceptance_checklist.json"

    antipatterns_registry = read_json(ap_path).get("items", []) if ap_path.exists() else []
    aliases = read_json(aliases_path).get("aliases", []) if aliases_path.exists() else []
    conflicts = read_json(conflicts_path) if conflicts_path.exists() else []
    open_questions = read_json(openq_path) if openq_path.exists() else []
    acceptance_checklist = read_json(acc_path) if acc_path.exists() else []

    # Validate antipatterns registry references
    for item in antipatterns_registry:
        for rid in item.get("related_principle_ids", []) or []:
            if rid not in canonical_ids:
                raise ValueError(f"antipattern references unknown principle id: {rid}")

    # Validate aliases
    seen_aliases: Set[str] = set()
    for a in aliases:
        alias = a.get("alias")
        canonical = a.get("canonical_id")
        if not alias or not canonical:
            raise ValueError("alias entry missing alias or canonical_id")
        if alias in seen_aliases:
            raise ValueError(f"duplicate alias mapping: {alias}")
        seen_aliases.add(alias)
        if canonical not in canonical_ids:
            raise ValueError(f"alias maps to unknown canonical_id: {canonical}")
        if alias in canonical_ids:
            raise ValueError(f"alias collides with existing canonical id: {alias}")

    # Preserve legacy meta if present
    legacy = ROOT.parent / "03_Global_UX_Principles_v1.json"
    meta = idx.get("meta")
    if not meta and legacy.exists():
        meta = read_json(legacy).get("meta")

    assembled = {
        "version": idx.get("version", "1.0.0"),
        "meta": meta or {},
        "principles": principles,
        "antipatterns_registry": antipatterns_registry,
        "conflicts": conflicts,
        "open_questions": open_questions,
        "aliases": aliases,
        "acceptance_checklist": acceptance_checklist,
    }
    return assembled


def write_ux_principles_monolith(lock: dict):
    assembled = assemble_ux_principles(lock)
    write_json(OUT / "03_Global_UX_Principles_v1.json", assembled)
    return True


"""
---------------------------
 04 User Stories assembly
---------------------------
"""
def assemble_userstories(userflow_ctx: dict) -> dict:
    us_root = ROOT / "04_userstories"
    idx = read_json(us_root / "index.json")
    epics = idx.get("epics", {})

    # Build validation context from userflow
    uf_nodes: Set[str] = set()
    uf_events: Set[str] = set()
    if userflow_ctx:
        for n in userflow_ctx.get("user_flow", []):
            nid = n.get("id")
            if nid:
                uf_nodes.add(nid)
        events_reg_path = ROOT / "02_userflow" / "analytics" / "events.json"
        if events_reg_path.exists():
            try:
                uf_events = set(read_json(events_reg_path).get("events", []))
            except Exception:
                uf_events = set()

    # Load stories
    stories_dir = us_root / "us"
    story_objs: List[dict] = []
    seen_ids: Set[str] = set()
    for path in sorted(stories_dir.glob("us-*.json")):
        s = read_json(path)
        sid = s.get("story_id")
        if not sid:
            raise ValueError(f"user story missing story_id in {path.name}")
        if sid in seen_ids:
            raise ValueError(f"duplicate user story id: {sid}")
        seen_ids.add(sid)

        # Validate analytics events
        for ev in s.get("analytics_events", []) or []:
            if ev not in uf_events:
                raise ValueError(f"user story {sid} references unknown analytics event: {ev}")

        # Validate FLOW:#node references inside refs and acceptance_criteria
        def validate_flow_ref(text: str):
            if not isinstance(text, str):
                return
            # naive parse for tokens like FLOW:#node-id separated by space or punct
            tokens = [t for t in text.replace(";", " ").replace(",", " ").split() if t.startswith("FLOW:#")]
            for t in tokens:
                node = t.split("FLOW:#", 1)[1]
                # strip trailing ) ] etc.
                node = node.strip().strip(")].")
                if node and node not in uf_nodes:
                    raise ValueError(f"user story {sid} refers to unknown FLOW node: {node}")

        for r in s.get("refs", []) or []:
            validate_flow_ref(r)
        for ac in s.get("acceptance_criteria", []) or []:
            validate_flow_ref(ac)

        story_objs.append(s)

    # Preserve version/meta if present in legacy
    legacy = ROOT.parent / "04_UserStories_v1.json"
    version = idx.get("version", "1.0.0")
    meta = None
    if legacy.exists():
        meta = read_json(legacy).get("meta")

    assembled = {
        "version": version,
        "meta": meta or {},
        "epics": [
            {"epic_id": k, "title": v.get("title"), "desc": v.get("desc")}
            for k, v in epics.items()
        ],
        "stories": story_objs,
    }
    return assembled


def write_userstories_monolith(userflow_ctx: dict):
    assembled = assemble_userstories(userflow_ctx)
    write_json(OUT / "04_UserStories_v1.json", assembled)
    return True


"""
---------------------------
 05 HIG Pattern Selection
---------------------------
"""
def assemble_hig(userflow_ctx: dict, userstories_ctx: dict) -> dict:
    hig_root = ROOT / "05_hig"
    idx = read_json(hig_root / "index.json")
    # Validation context
    uf_nodes: Set[str] = set(n.get("id") for n in (userflow_ctx or {}).get("user_flow", []) if n.get("id"))
    us_ids: Set[str] = set()
    # Build from stories modules
    stories_dir = hig_root / "stories"
    mono_stories: List[dict] = []

    # Collect user story ids from assembled userstories if available
    if userstories_ctx:
        for s in userstories_ctx.get("stories", []) or []:
            sid = s.get("story_id")
            if sid:
                us_ids.add(sid)
    else:
        # fallback: read us index
        us_idx_path = ROOT / "04_userstories" / "index.json"
        if us_idx_path.exists():
            try:
                for sid in read_json(us_idx_path).get("stories", []):
                    us_ids.add(sid)
            except Exception:
                pass

    for sid, info in (idx.get("stories", {}) or {}).items():
        path = hig_root / info.get("path", f"stories/{sid}/candidates.json")
        data = read_json(path)
        # Validate user story id matches
        if data.get("story_id") != sid:
            raise ValueError(f"HIG story mismatch: index {sid} vs file {data.get('story_id')}")
        if us_ids and sid not in us_ids:
            raise ValueError(f"HIG refers to unknown user story id: {sid}")
        # Validate flow node refs inside candidates and recommendation
        def validate_refs(refs: dict):
            for node in refs.get("flow_nodes", []) or []:
                if node not in uf_nodes:
                    raise ValueError(f"HIG {sid} references unknown flow node: {node}")
        for cand in data.get("candidates", []) or []:
            validate_refs(cand.get("refs", {}))
        if "recommendation" in data:
            validate_refs(data.get("recommendation", {}).get("refs", {}))
        mono_stories.append({
            "story_id": sid,
            "title": data.get("title"),
            "role": data.get("role"),
            "value": data.get("value"),
            "core_actions": data.get("core_actions", []),
            "candidates": data.get("candidates", []),
            "recommendation": data.get("recommendation", {})
        })

    # Preserve legacy meta if present
    legacy = ROOT.parent / "05_HIG_Pattern_selection_v1.json"
    meta = None
    if legacy.exists():
        meta = read_json(legacy).get("meta")

    assembled = {
        "version": idx.get("version", "1.0.0"),
        "meta": meta or {},
        "source_files": {"prd": "00_PRD_v1.json", "cjm": "01_CJM_v1.json", "user_flow": "02_UserFlow_v1.json", "user_stories": "04_UserStories_v1.json", "ux_principles": "03_Global_UX_Principles_v1.json"},
        "governing_rules": idx.get("governing_rules", {}),
        "stories": mono_stories,
    }
    return assembled


def write_hig_monolith(userflow_ctx: dict, userstories_ctx: dict):
    assembled = assemble_hig(userflow_ctx, userstories_ctx)
    write_json(OUT / "05_HIG_Pattern_selection_v1.json", assembled)
    return True


"""
---------------------------
 00 PRD assembly
---------------------------
"""
def assemble_prd(lock: dict) -> dict:
    prd_root = ROOT / "00_prd"
    idx = read_json(prd_root / "index.json")
    section_ids = idx.get("sections", [])
    sections_dir = prd_root / "sections"
    seen: Set[str] = set()
    assembled_sections: List[dict] = []
    for sid in section_ids:
        path = sections_dir / f"{sid}.json"
        data = read_json(path)
        sid2 = data.get("id")
        if sid2 != sid:
            raise ValueError(f"PRD section id mismatch: index {sid} vs file {sid2}")
        if sid in seen:
            raise ValueError(f"Duplicate PRD section id: {sid}")
        seen.add(sid)
        ensure_in_ids(lock, "prd", "sections", sid)
        assembled_sections.append(data)

    # Preserve legacy meta
    legacy = ROOT.parent / "00_PRD_v1.json"
    meta = None
    if legacy.exists():
        meta = read_json(legacy).get("meta")

    return {
        "version": idx.get("version", "1.0.0"),
        "meta": meta or {},
        "prd": assembled_sections,
    }


def write_prd_monolith(lock: dict):
    assembled = assemble_prd(lock)
    write_json(OUT / "00_PRD_v1.json", assembled)
    return True


"""
---------------------------
 01 CJM assembly
---------------------------
"""
def assemble_cjm(lock: dict) -> dict:
    cjm_root = ROOT / "01_cjm"
    idx = read_json(cjm_root / "index.json")
    stage_ids = idx.get("stages", [])
    stages_dir = cjm_root / "stages"
    seen: Set[str] = set()
    assembled_stages: List[dict] = []
    for sid in stage_ids:
        path = stages_dir / f"{sid}.json"
        data = read_json(path)
        sid2 = data.get("id")
        if sid2 != sid:
            raise ValueError(f"CJM stage id mismatch: index {sid} vs file {sid2}")
        if sid in seen:
            raise ValueError(f"Duplicate CJM stage id: {sid}")
        seen.add(sid)
        ensure_in_ids(lock, "cjm", "stages", sid)
        assembled_stages.append(data)

    # Preserve legacy meta
    legacy = ROOT.parent / "01_CJM_v1.json"
    meta = None
    if legacy.exists():
        meta = read_json(legacy).get("meta")

    return {
        "version": idx.get("version", "1.0.0"),
        "meta": meta or {},
        "cjm": assembled_stages,
    }


def write_cjm_monolith(lock: dict):
    assembled = assemble_cjm(lock)
    write_json(OUT / "01_CJM_v1.json", assembled)
    return True


def summarize_status():
    msgs = []
    # PRD
    try:
        prd = read_json(OUT / "00_PRD_v1.json")
        msgs.append(f"Assembled: 00_PRD_v1.json (sections: {len(prd.get('prd', []))})")
    except Exception:
        pass
    # CJM
    try:
        cjm = read_json(OUT / "01_CJM_v1.json")
        msgs.append(f"Assembled: 01_CJM_v1.json (stages: {len(cjm.get('cjm', []))})")
    except Exception:
        pass
    # UserFlow
    try:
        uf = read_json(OUT / "02_UserFlow_v1.json")
        nodes = uf.get('user_flow', [])
        edges = sum(len(n.get('edges', []) or []) for n in nodes)
        # events count from registry
        ev_reg = read_json(ROOT / "02_userflow" / "analytics" / "events.json")
        msgs.append(f"Assembled: 02_UserFlow_v1.json (nodes: {len(nodes)}, edges: {edges}, events: {len(ev_reg.get('events', []))})")
    except Exception:
        pass
    # UX Principles
    try:
        ux = read_json(OUT / "03_Global_UX_Principles_v1.json")
        msgs.append(f"Assembled: 03_Global_UX_Principles_v1.json (principles: {len(ux.get('principles', []))}, antipatterns: {len(ux.get('antipatterns_registry', []))}, aliases: {len(ux.get('aliases', []))})")
    except Exception:
        pass
    # User Stories
    try:
        us = read_json(OUT / "04_UserStories_v1.json")
        msgs.append(f"Assembled: 04_UserStories_v1.json (epics: {len(us.get('epics', []))}, stories: {len(us.get('stories', []))})")
    except Exception:
        pass
    # HIG
    try:
        hig = read_json(OUT / "05_HIG_Pattern_selection_v1.json")
        cand = sum(len(s.get('candidates', []) or []) for s in hig.get('stories', []) or [])
        msgs.append(f"Assembled: 05_HIG_Pattern_selection_v1.json (stories: {len(hig.get('stories', []))}, candidates: {cand})")
    except Exception:
        pass
    # CtxUX
    try:
        cx = read_json(OUT / "06_Contextual_UX_Guidelines_v1.json")
        lps = sum(len(s.get('local_principles', []) or []) for s in cx.get('screens', []) or [])
        msgs.append(f"Assembled: 06_Contextual_UX_Guidelines_v1.json (screens: {len(cx.get('screens', []))}, local_principles: {lps})")
    except Exception:
        pass
    return msgs


def main():
    ensure_out()
    lock = read_ids_lock()

    # Assemble selected modules first
    wrote = []
    if write_prd_monolith(lock):
        wrote.append("00_PRD_v1.json")
    if write_cjm_monolith(lock):
        wrote.append("01_CJM_v1.json")
    uf_assembled = write_userflow_monolith(lock)
    wrote.append("02_UserFlow_v1.json")
    if write_ctxux_monolith(lock, uf_assembled):
        wrote.append("06_Contextual_UX_Guidelines_v1.json")
    if write_ux_principles_monolith(lock):
        wrote.append("03_Global_UX_Principles_v1.json")
    if write_userstories_monolith(uf_assembled):
        wrote.append("04_UserStories_v1.json")
    # Load assembled user stories for HIG validation
    us_assembled = read_json(OUT / "04_UserStories_v1.json") if (OUT / "04_UserStories_v1.json").exists() else None
    if write_hig_monolith(uf_assembled, us_assembled):
        wrote.append("05_HIG_Pattern_selection_v1.json")

    # Persist updated IDs lock
    write_ids_lock(lock)

    for line in summarize_status():
        print(line)


if __name__ == "__main__":
    main()
