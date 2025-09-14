#!/usr/bin/env python3
import json
import sys
from pathlib import Path
from typing import Optional, Tuple, Set, Dict, List

ROOT = Path(__file__).parent
BUILD = ROOT / "specs" / "_build"
CJM_PATH = BUILD / "01_CJM_v1.json"
UF_PATH = BUILD / "02_UserFlow_v1.json"
PRD_PATH = BUILD / "00_PRD_v1.json"
UX_PATH = BUILD / "03_Global_UX_Principles_v1.json"
STORIES_PATH = BUILD / "04_UserStories_v1.json"
HIG_PATH = BUILD / "05_HIG_Pattern_selection_v1.json"
CTX_UX_PATH = BUILD / "06_Contextual_UX_Guidelines_v1.json"
ANALYTICS_SCHEMA_PATH = ROOT / "analytics_schema.json"


def load_json(p: Path):
    if not p.exists():
        raise FileNotFoundError(f"Missing required build artifact: {p}. Run 'python3 specs/_build/build.py' first.")
    with p.open("r", encoding="utf-8") as f:
        return json.load(f)


def gather_cjm_stage_ids(cjm_doc: dict) -> set[str]:
    ids = set()
    for item in cjm_doc.get("cjm", []):
        if isinstance(item, dict) and "id" in item:
            ids.add(item["id"])
    return ids


def has_cjm_ref(refs: list) -> bool:
    return any(isinstance(r, str) and r.startswith("CJM:#") for r in refs or [])


def has_prd_ref(refs: list) -> bool:
    return any(isinstance(r, str) and r.startswith("PRD:#") for r in refs or [])


def check_userflow_refs(userflow_doc: dict):
    problems = []
    nodes = userflow_doc.get("user_flow", [])
    for node in nodes:
        nid = node.get("id")
        nrefs = node.get("refs", [])
        if not has_prd_ref(nrefs):
            problems.append(("node-missing-prd-ref", nid))
        if not has_cjm_ref(nrefs):
            problems.append(("node-missing-cjm-ref", nid))
        for edge in node.get("edges", []) or []:
            eid = edge.get("id")
            erefs = edge.get("refs", [])
            if not has_prd_ref(erefs):
                problems.append(("edge-missing-prd-ref", f"{nid}:{eid}"))
            # Edges may sometimes not map to a CJM stage directly; warn rather than error
            if not has_cjm_ref(erefs):
                problems.append(("edge-missing-cjm-ref", f"{nid}:{eid}"))
    return problems


def check_analytics_events(userflow_doc: dict):
    problems = []
    for ev in userflow_doc.get("analytics_events", []) or []:
        name = ev.get("event")
        if not ev.get("owner"):
            problems.append(("analytics-missing-owner", name))
        if not ev.get("kpi_ref"):
            problems.append(("analytics-missing-kpi_ref", name))
    return problems


def build_dd_maps(userflow_doc: dict) -> tuple[set[str], dict[str, str]]:
    names: set[str] = set()
    cov: dict[str, str] = {}
    for d in userflow_doc.get("data_dictionary", []) or []:
        if isinstance(d, dict) and isinstance(d.get("name"), str):
            n = d["name"]
            names.add(n)
            cov[n] = d.get("coverage") or "required"
    return names, cov

def build_enum_literals(userflow_doc: dict) -> set[str]:
    literals: set[str] = set()
    for d in userflow_doc.get("data_dictionary", []) or []:
        t = d.get("type")
        if not isinstance(t, str):
            continue
        t = t.strip()
        if t.startswith("enum[") and t.endswith("]"):
            inner = t[len("enum["):-1]
            for part in inner.split(','):
                val = part.strip()
                if val:
                    literals.add(val)
    # Also allow some common symbolic literals used in guards
    literals.update({"true","false","today","granted","denied","pdf_a_2u"})
    return literals

def check_io_against_dd(userflow_doc: dict):
    problems = []
    dd, coverage = build_dd_maps(userflow_doc)
    enum_literals = build_enum_literals(userflow_doc)
    def check_list(lst, kind, nid):
        for name in lst or []:
            if name not in dd:
                # Unknown entirely → always fatal
                problems.append((f"{kind}-not-in-data-dictionary", f"{nid}:{name}"))
    for node in userflow_doc.get("user_flow", []) or []:
        nid = node.get("id")
        check_list(node.get("inputs"), "input", nid)
        check_list(node.get("outputs"), "output", nid)
        for edge in node.get("edges", []) or []:
            # naive guard var extraction: split by non-alnum/underscore and check tokens against dd
            guard = edge.get("guard")
            if guard:
                import re
                # enforce allowed operators only
                if not re.fullmatch(r"[A-Za-z0-9_\s\(\)\"'<>!=]+", guard or ""):
                    problems.append(("guard-invalid-operator", f"{nid}:{edge.get('id')}:{guard}"))
                tokens = [t for t in re.split(r"[^A-Za-z0-9_]+", guard) if t]
                # classify
                blacklist = {"len", "true", "false", "today"}
                for t in tokens:
                    if t.isdigit() or t in blacklist or t in enum_literals:
                        continue
                    # if token matches an identifier in dd, it's okay
                    if t in dd:
                        continue
                    # token might be an unquoted string literal → error
                    problems.append(("guard-unquoted-literal", f"{nid}:{edge.get('id')}:{t}"))
    return problems


def check_cjm_coverage(userflow_doc: dict, cjm_ids: set[str]):
    # Ensure each core in-app CJM stage has at least one mention in refs anywhere
    refs_all = []
    for node in userflow_doc.get("user_flow", []) or []:
        refs_all.extend(node.get("refs", []) or [])
        for edge in node.get("edges", []) or []:
            refs_all.extend(edge.get("refs", []) or [])
    present = {r.split("#",1)[1] for r in refs_all if isinstance(r, str) and r.startswith("CJM:#")}
    missing = sorted(list((cjm_ids - present)))
    return missing

def cjm_coverage_map(userflow_doc: dict, cjm_ids: set[str]) -> dict[str, list[str]]:
    """Return mapping CJM stage -> list of UserFlow nodes/edges referencing it."""
    cov: dict[str, list[str]] = {cid: [] for cid in cjm_ids}
    for node in userflow_doc.get("user_flow", []) or []:
        nid = node.get("id", "<unknown>")
        for r in node.get("refs", []) or []:
            if isinstance(r, str) and r.startswith("CJM:#"):
                stage = r.split("#", 1)[1]
                if stage in cov:
                    cov[stage].append(f"node:{nid}")
        for edge in node.get("edges", []) or []:
            eid = edge.get("id", "<unknown>")
            for r in edge.get("refs", []) or []:
                if isinstance(r, str) and r.startswith("CJM:#"):
                    stage = r.split("#", 1)[1]
                    if stage in cov:
                        cov[stage].append(f"edge:{nid}:{eid}")
    # remove duplicates while preserving order
    for k, lst in cov.items():
        seen = set()
        uniq = []
        for x in lst:
            if x in seen:
                continue
            seen.add(x)
            uniq.append(x)
        cov[k] = uniq
    return cov

# ------------------------
# Lightweight JSON Schema validation
# ------------------------

def _is_list_of_strings(v) -> bool:
    return isinstance(v, list) and all(isinstance(x, str) for x in v)

def validate_cjm_schema(doc: dict) -> list[tuple[str, str]]:
    issues: list[tuple[str, str]] = []
    if not isinstance(doc, dict):
        return [("schema-violation", "CJM: root is not an object")] 
    if not isinstance(doc.get("cjm"), list):
        issues.append(("schema-violation", "CJM: 'cjm' must be an array"))
        return issues
    for i, stage in enumerate(doc.get("cjm", [])):
        path = f"cjm[{i}]"
        if not isinstance(stage, dict):
            issues.append(("schema-violation", f"{path}: must be an object"))
            continue
        if not isinstance(stage.get("id"), str) or not stage["id"]:
            issues.append(("schema-violation", f"{path}.id: required non-empty string"))
        if "refs" in stage and not _is_list_of_strings(stage.get("refs")):
            issues.append(("schema-violation", f"{path}.refs: must be array of strings if present"))
    return issues

def validate_userflow_schema(doc: dict) -> list[tuple[str, str]]:
    issues: list[tuple[str, str]] = []
    if not isinstance(doc, dict):
        return [("schema-violation", "UserFlow: root is not an object")]
    if not isinstance(doc.get("user_flow"), list):
        issues.append(("schema-violation", "UserFlow: 'user_flow' must be an array"))
        return issues
    for i, node in enumerate(doc.get("user_flow", [])):
        npath = f"user_flow[{i}]"
        if not isinstance(node, dict):
            issues.append(("schema-violation", f"{npath}: must be an object"))
            continue
        if not isinstance(node.get("id"), str) or not node["id"]:
            issues.append(("schema-violation", f"{npath}.id: required non-empty string"))
        if not isinstance(node.get("type"), str) or not node["type"]:
            issues.append(("schema-violation", f"{npath}.type: required non-empty string"))
        if "refs" in node and not _is_list_of_strings(node.get("refs")):
            issues.append(("schema-violation", f"{npath}.refs: must be array of strings if present"))
        edges = node.get("edges")
        if edges is not None:
            if not isinstance(edges, list):
                issues.append(("schema-violation", f"{npath}.edges: must be an array if present"))
            else:
                for j, edge in enumerate(edges):
                    epath = f"{npath}.edges[{j}]"
                    if not isinstance(edge, dict):
                        issues.append(("schema-violation", f"{epath}: must be an object"))
                        continue
                    if not isinstance(edge.get("id"), str) or not edge["id"]:
                        issues.append(("schema-violation", f"{epath}.id: required non-empty string"))
                    if not isinstance(edge.get("target"), str) or not edge["target"]:
                        issues.append(("schema-violation", f"{epath}.target: required non-empty string"))
                    if "refs" in edge and not _is_list_of_strings(edge.get("refs")):
                        issues.append(("schema-violation", f"{epath}.refs: must be array of strings if present"))
    # analytics_events
    if "analytics_events" in doc:
        if not isinstance(doc.get("analytics_events"), list):
            issues.append(("schema-violation", "analytics_events: must be an array if present"))
        else:
            for i, ev in enumerate(doc.get("analytics_events", [])):
                epath = f"analytics_events[{i}]"
                if not isinstance(ev, dict):
                    issues.append(("schema-violation", f"{epath}: must be an object"))
                    continue
                if not isinstance(ev.get("event"), str) or not ev["event"]:
                    issues.append(("schema-violation", f"{epath}.event: required non-empty string"))
                if "owner" in ev and not isinstance(ev.get("owner"), str):
                    issues.append(("schema-violation", f"{epath}.owner: must be a string if present"))
                if "kpi_ref" in ev and not isinstance(ev.get("kpi_ref"), str):
                    issues.append(("schema-violation", f"{epath}.kpi_ref: must be a string if present"))
    return issues


def main():
    cjm = load_json(CJM_PATH)
    uf = load_json(UF_PATH)
    prd = load_json(PRD_PATH)
    try:
        ux = load_json(UX_PATH)
    except FileNotFoundError:
        ux = None
    try:
        stories = load_json(STORIES_PATH)
    except FileNotFoundError:
        stories = None
    try:
        hig = load_json(HIG_PATH)
    except FileNotFoundError:
        hig = None
    try:
        ctxux = load_json(CTX_UX_PATH)
    except FileNotFoundError:
        ctxux = None
    try:
        analytics_schema = load_json(ANALYTICS_SCHEMA_PATH)
    except FileNotFoundError:
        analytics_schema = None

    cjm_ids = gather_cjm_stage_ids(cjm)
    prd_ids = {item.get("id") for item in prd.get("prd", []) if isinstance(item, dict) and item.get("id")}

    issues = []
    # Schema validation first
    schema_issues = []
    schema_issues += validate_cjm_schema(cjm)
    schema_issues += validate_userflow_schema(uf)
    # Basic PRD schema check
    if not isinstance(prd, dict) or not isinstance(prd.get("prd"), list):
        schema_issues.append(("schema-violation", "PRD: 'prd' must be an array"))
    # Basic UX schema check
    if ux is not None:
        if not isinstance(ux, dict) or not isinstance(ux.get("principles"), list):
            schema_issues.append(("schema-violation", "UX: 'principles' must be an array"))
        else:
            for i, p in enumerate(ux.get("principles", [])):
                ppath = f"ux.principles[{i}]"
                if not isinstance(p, dict):
                    schema_issues.append(("schema-violation", f"{ppath}: must be an object"))
                    continue
                if not isinstance(p.get("id"), str) or not p["id"]:
                    schema_issues.append(("schema-violation", f"{ppath}.id: required non-empty string"))
                if not isinstance(p.get("title"), str) or not p["title"]:
                    schema_issues.append(("schema-violation", f"{ppath}.title: required non-empty string"))
                if "refs" in p and not _is_list_of_strings(p.get("refs")):
                    schema_issues.append(("schema-violation", f"{ppath}.refs: must be array of strings if present"))
                if "antipatterns" in p and not isinstance(p.get("antipatterns"), list):
                    schema_issues.append(("schema-violation", f"{ppath}.antipatterns: must be an array if present"))
                else:
                    for j, a in enumerate(p.get("antipatterns", []) or []):
                        apath = f"{ppath}.antipatterns[{j}]"
                        if not isinstance(a, dict):
                            schema_issues.append(("schema-violation", f"{apath}: must be an object"))
                            continue
                        if "refs" in a and not _is_list_of_strings(a.get("refs")):
                            schema_issues.append(("schema-violation", f"{apath}.refs: must be array of strings if present"))
    # Basic UserStories schema check
    if stories is not None:
        if not isinstance(stories, dict):
            schema_issues.append(("schema-violation", "Stories: root must be an object"))
        else:
            if "stories" in stories and not isinstance(stories.get("stories"), list):
                schema_issues.append(("schema-violation", "Stories: 'stories' must be an array"))
            if "epics" in stories and not isinstance(stories.get("epics"), list):
                schema_issues.append(("schema-violation", "Stories: 'epics' must be an array if present"))
            for i, s in enumerate(stories.get("stories", []) or []):
                spath = f"stories[{i}]"
                if not isinstance(s, dict):
                    schema_issues.append(("schema-violation", f"{spath}: must be an object"))
                    continue
                if not isinstance(s.get("story_id"), str) or not s["story_id"]:
                    schema_issues.append(("schema-violation", f"{spath}.story_id: required non-empty string"))
                if "acceptance_criteria" in s and not isinstance(s.get("acceptance_criteria"), list):
                    schema_issues.append(("schema-violation", f"{spath}.acceptance_criteria: must be an array if present"))
                if isinstance(s.get("acceptance_criteria"), list):
                    for j, ac in enumerate(s.get("acceptance_criteria", [])):
                        if not isinstance(ac, str):
                            schema_issues.append(("schema-violation", f"{spath}.acceptance_criteria[{j}]: must be a string"))
    if schema_issues:
        issues += [(f"schema", msg) for _, msg in schema_issues]

    # Optional: formal JSON Schema validation if jsonschema is installed
    try:
        import jsonschema  # type: ignore
        def _try_schema(doc: dict, schema: dict, label: str):
            try:
                jsonschema.validate(instance=doc, schema=schema)
            except Exception as e:
                issues.append((f"schema-jsonschema-{label}", str(e)))

        # Minimal illustrative schemas (can be extended later)
        PRD_SCHEMA = {
            "type": "object",
            "properties": {
                "prd": {
                    "type": "array",
                    "items": {"type": "object", "required": ["id", "title"],
                               "properties": {"id": {"type": "string"}}}
                }
            },
            "required": ["prd"]
        }
        CJM_SCHEMA = {"type": "object", "properties": {"cjm": {"type": "array"}}, "required": ["cjm"]}
        UF_SCHEMA = {"type": "object", "properties": {"user_flow": {"type": "array"}}, "required": ["user_flow"]}
        UX_SCHEMA = {"type": "object", "properties": {"principles": {"type": "array"}}}
        STORIES_SCHEMA = {"type": "object", "properties": {"stories": {"type": "array"}}}
        HIG_SCHEMA = {"type": "object", "properties": {"stories": {"type": "array"}}}

        _try_schema(prd, PRD_SCHEMA, "prd")
        _try_schema(cjm, CJM_SCHEMA, "cjm")
        _try_schema(uf, UF_SCHEMA, "userflow")
        if ux is not None:
            _try_schema(ux, UX_SCHEMA, "ux")
        if stories is not None:
            _try_schema(stories, STORIES_SCHEMA, "stories")
        if hig is not None:
            _try_schema(hig, HIG_SCHEMA, "hig")
    except Exception:
        # jsonschema not available; skip without failing
        pass

    # Traceability validations
    issues += check_userflow_refs(uf)
    issues += check_analytics_events(uf)
    issues += check_io_against_dd(uf)

    # CJM coverage
    missing_cjm = check_cjm_coverage(uf, cjm_ids)
    cjm_cov = cjm_coverage_map(uf, cjm_ids)

    # ---------------- PRD traceability ----------------
    def _collect_prd_refs_in_cjm(obj, path="$"):
        refs: list[tuple[str, str]] = []
        if isinstance(obj, dict):
            for k, v in obj.items():
                if k == "refs" and isinstance(v, list):
                    for s in v:
                        if isinstance(s, str) and s.startswith("PRD:#"):
                            refs.append((path+".refs", s.split("#",1)[1]))
                else:
                    refs.extend(_collect_prd_refs_in_cjm(v, path+f".{k}"))
        elif isinstance(obj, list):
            for i, it in enumerate(obj):
                refs.extend(_collect_prd_refs_in_cjm(it, path+f"[{i}]"))
        return refs

    cjm_prd_refs = _collect_prd_refs_in_cjm(cjm)

    uf_prd_refs = []
    # nodes and edges refs
    for node in uf.get("user_flow", []) or []:
        nid = node.get("id", "<unknown>")
        for r in node.get("refs", []) or []:
            if isinstance(r, str) and r.startswith("PRD:#"):
                uf_prd_refs.append((f"node:{nid}", r.split("#",1)[1]))
        for edge in node.get("edges", []) or []:
            eid = edge.get("id", "<unknown>")
            for r in edge.get("refs", []) or []:
                if isinstance(r, str) and r.startswith("PRD:#"):
                    uf_prd_refs.append((f"edge:{nid}:{eid}", r.split("#",1)[1]))
    # analytics kpi_ref
    for ev in uf.get("analytics_events", []) or []:
        kr = ev.get("kpi_ref")
        if isinstance(kr, str) and kr.startswith("PRD:#"):
            uf_prd_refs.append((f"analytics:{ev.get('event')}", kr.split("#",1)[1]))

    # validate PRD refs exist
    for loc, pid in cjm_prd_refs:
        if pid not in prd_ids:
            issues.append(("cjm-prd-ref-missing", f"{loc} -> PRD:{pid}"))
    for loc, pid in uf_prd_refs:
        if pid not in prd_ids:
            issues.append(("userflow-prd-ref-missing", f"{loc} -> PRD:{pid}"))

    # PRD coverage maps
    from collections import defaultdict
    prd_cov_cjm: dict[str, list[str]] = defaultdict(list)
    for loc, pid in cjm_prd_refs:
        prd_cov_cjm[pid].append(loc)
    prd_cov_uf: dict[str, list[str]] = defaultdict(list)
    for loc, pid in uf_prd_refs:
        prd_cov_uf[pid].append(loc)

    # ---------------- Additional Core Enhancements ----------------
    # 1) PRD sub-ID semantics: allow refs like PRD:#4_2.export to resolve to base PRD id 4_2
    def _split_prd_ref(pr: str) -> Tuple[str, Optional[str]]:
        # accepts '4_2' or '4_2.export'
        base, *rest = pr.split('.', 1)
        return base, (rest[0] if rest else None)

    # Validate PRD sub-IDs across collected references
    for (loc, pid) in cjm_prd_refs + uf_prd_refs:
        base, sub = _split_prd_ref(pid)
        if base not in prd_ids:
            issues.append(("prd-subid-missing-base", f"{loc} -> PRD:{pid} (base {base} not found)"))

    # 2) Duplicate ID detection
    def _dupe_ids(objs: List[dict], field: str) -> List[str]:
        seen, dup = set(), []
        for o in objs or []:
            vid = o.get(field)
            if not isinstance(vid, str):
                continue
            if vid in seen:
                dup.append(vid)
            else:
                seen.add(vid)
        return dup

    uf_node_dups = _dupe_ids(uf.get("user_flow", []) or [], "id")
    if uf_node_dups:
        issues.append(("userflow-duplicate-node-id", ", ".join(sorted(set(uf_node_dups)))))

    # 3) Orphan detection and reachability graph checks in UserFlow
    # Build graph
    node_by_id: Dict[str, dict] = {n.get("id"): n for n in uf.get("user_flow", []) or [] if isinstance(n, dict) and n.get("id")}
    adj: Dict[str, Set[str]] = {nid: set() for nid in node_by_id}
    for nid, n in node_by_id.items():
        for e in n.get("edges", []) or []:
            tgt = e.get("target")
            if isinstance(tgt, str) and tgt in node_by_id:
                adj[nid].add(tgt)
    # entry nodes: prefer type == 'entry', else known 'app-launch', else first node
    entry_nodes = [nid for nid, n in node_by_id.items() if n.get("type") == "entry"]
    if not entry_nodes and "app-launch" in node_by_id:
        entry_nodes = ["app-launch"]
    if not entry_nodes and node_by_id:
        entry_nodes = [next(iter(node_by_id.keys()))]
    # reachability
    reachable: Set[str] = set()
    frontier = list(entry_nodes)
    while frontier:
        cur = frontier.pop()
        if cur in reachable:
            continue
        reachable.add(cur)
        frontier.extend(adj.get(cur, []))
    unreachable = sorted([nid for nid in node_by_id if nid not in reachable])
    if unreachable:
        issues.append(("userflow-unreachable-node", ", ".join(unreachable)))

    # dead-end detection: nodes with no outgoing edges and not terminal types
    TERMINAL_TYPES = {"success", "error", "terminator"}
    dead_ends = []
    for nid, n in node_by_id.items():
        if not (n.get("edges") or []) and n.get("type") not in TERMINAL_TYPES:
            dead_ends.append(nid)
    if dead_ends:
        issues.append(("userflow-dead-end-node", ", ".join(sorted(dead_ends))))

    # decision default-edge checks
    for nid, n in node_by_id.items():
        edges = n.get("edges", []) or []
        if not edges:
            continue
        has_guard = any(bool(e.get("guard")) for e in edges)
        policy = n.get("decision_policy") or {}
        if has_guard:
            if policy.get("mutually_exclusive") and policy.get("exhaustive") and not policy.get("default_edge_id"):
                issues.append(("userflow-decision-missing-default", nid))

    # 4) Improved guard parser: extract identifiers robustly
    def parse_guard_identifiers(expr: str) -> Set[str]:
        import re
        # tokens of interest: identifiers [A-Za-z_][A-Za-z0-9_]*
        idents = set(re.findall(r"\b[A-Za-z_][A-Za-z0-9_]*\b", expr or ""))
        # remove operators/keywords/booleans/common funcs
        blacklist = {"and","or","not","true","false","len","today","if","else"}
        return {t for t in idents if t not in blacklist}

    # rebuild enum literal set
    enum_literals = build_enum_literals(uf)

    # ensure all identifiers used in guards come from data_dictionary
    dd, dd_cov = build_dd_maps(uf)
    for nid, n in node_by_id.items():
        for e in n.get("edges", []) or []:
            g = e.get("guard")
            if not g:
                continue
            for ident in parse_guard_identifiers(g):
                if ident.isdigit() or ident in enum_literals:
                    continue
                if ident not in dd:
                    issues.append(("guard-var-not-in-data-dictionary", f"{nid}:{e.get('id')}:{ident}"))

    # 5) Data dictionary unused fields
    used_dd: Set[str] = set()
    def mark_used(lst):
        for x in lst or []:
            if isinstance(x, str):
                used_dd.add(x)
    for n in uf.get("user_flow", []) or []:
        mark_used(n.get("inputs"))
        mark_used(n.get("outputs"))
        for e in n.get("edges", []) or []:
            g = e.get("guard")
            if g:
                for ident in parse_guard_identifiers(g):
                    used_dd.add(ident)
    # consider analytics_events params as DD usage too
    for ev in uf.get("analytics_events", []) or []:
        for p in ev.get("params", []) or []:
            if isinstance(p, dict) and isinstance(p.get("name"), str):
                used_dd.add(p["name"]) 
    unused_dd = sorted(list(dd - used_dd))
    # classify by coverage: fatal for required; skip optional warnings
    for name in unused_dd:
        if dd_cov.get(name, "required") == "required":
            issues.append(("unused-required-data-dictionary", name))

    # 6) Analytics integrity checks
    for ev in uf.get("analytics_events", []) or []:
        event = ev.get("event")
        if not ev.get("owner"):
            issues.append(("analytics-missing-owner", event))
        if not ev.get("kpi_ref"):
            issues.append(("analytics-missing-kpi_ref", event))
        # simple type validation for params
        for p in ev.get("params", []) or []:
            if not isinstance(p, dict) or not p.get("name") or not p.get("type"):
                issues.append(("analytics-param-invalid", f"{event}:{p}"))

    # 7) Stories linkage strictness: each AC line with FLOW must include PRD
    if stories is not None:
        import re
        for i, s in enumerate(stories.get("stories", []) or []):
            for j, ac in enumerate(s.get("acceptance_criteria", []) or []):
                has_flow = re.search(r"\b(FLOW|UserFlow):#", ac or "") is not None
                has_prd = re.search(r"\bPRD:#", ac or "") is not None
                if has_flow and not has_prd:
                    issues.append(("stories-flow-without-prd", f"stories[{i}].acceptance_criteria[{j}]"))

    # -------------- Pretty printing with colors --------------
    class C:
        RED = "\033[31m"
        GREEN = "\033[32m"
        YELLOW = "\033[33m"
        CYAN = "\033[36m"
        BOLD = "\033[1m"
        RESET = "\033[0m"

    def hdr(title: str):
        print(f"{C.BOLD}{C.CYAN}{title}{C.RESET}")

    def ok(msg: str):
        print(f"{C.GREEN}✔ {msg}{C.RESET}")

    def warn(msg: str):
        print(f"{C.YELLOW}• {msg}{C.RESET}")

    def err(msg: str):
        print(f"{C.RED}✖ {msg}{C.RESET}")

    hdr("Traceability validation report")
    ok(f"CJM stages: {', '.join(sorted(cjm_ids))}")
    ok(f"PRD sections: {', '.join(sorted(prd_ids))}")
    if ux is not None:
        ok(f"UX principles: {len(ux.get('principles', []))}")
    if stories is not None:
        ok(f"User stories: {len(stories.get('stories', []))}")
    if hig is not None:
        ok(f"HIG patterns stories: {len(hig.get('stories', []))}")
    if ctxux is not None:
        ok(f"Contextual UX local principles: {len(ctxux.get('local_principles', []))}")

    if missing_cjm:
        hdr("CJM stages not referenced in UserFlow (info)")
        for m in missing_cjm:
            warn(m)
    else:
        ok("All CJM stages referenced at least once in UserFlow refs.")

    # Coverage map
    hdr("CJM coverage map (stage -> nodes/edges)")
    for stage in sorted(cjm_cov.keys()):
        items = cjm_cov[stage]
        if items:
            print(f"{C.BOLD}- {stage}:{C.RESET}")
            for it in items:
                print(f"    • {it}")
        else:
            warn(f"{stage}: (no references)")

    # PRD coverage maps
    hdr("PRD coverage in CJM (PRD id -> locations)")
    for pid in sorted(prd_ids):
        locs = prd_cov_cjm.get(pid, [])
        if locs:
            print(f"{C.BOLD}- PRD:{pid}:{C.RESET}")
            for l in locs:
                print(f"    • {l}")
        else:
            warn(f"PRD:{pid}: (no references)")

    hdr("PRD coverage in UserFlow (PRD id -> nodes/edges/analytics)")
    for pid in sorted(prd_ids):
        locs = prd_cov_uf.get(pid, [])
        if locs:
            print(f"{C.BOLD}- PRD:{pid}:{C.RESET}")
            for l in locs:
                print(f"    • {l}")
        else:
            warn(f"PRD:{pid}: (no references)")

    # --------------- Data Dictionary coverage (summary) ---------------
    try:
        dd_names, dd_cov = build_dd_maps(uf)
        # Recompute used keys from previously computed used_dd if available; otherwise rebuild
        used_dd: set[str] = set()
        for n in uf.get("user_flow", []) or []:
            for x in (n.get("inputs") or []):
                if isinstance(x, str):
                    used_dd.add(x)
            for x in (n.get("outputs") or []):
                if isinstance(x, str):
                    used_dd.add(x)
            for e in n.get("edges", []) or []:
                g = e.get("guard")
                if g:
                    for ident in parse_guard_identifiers(g):
                        used_dd.add(ident)
        req = sorted([k for k in dd_names if dd_cov.get(k, "required") == "required"])
        opt = sorted([k for k in dd_names if dd_cov.get(k, "required") == "optional"])
        req_used = [k for k in req if k in used_dd]
        req_unused = [k for k in req if k not in used_dd]
        opt_used = [k for k in opt if k in used_dd]
        opt_unused = [k for k in opt if k not in used_dd]
        hdr("Data Dictionary coverage (required/optional)")
        ok(f"Required used: {len(req_used)} / {len(req)} | Optional used: {len(opt_used)} / {len(opt)}")
        if req_unused:
            for k in req_unused:
                err(f"unused-required: {k}")
        # Optional unused are intentionally not warned to reduce noise
    except Exception:
        pass

    # --------------- UX: check refs back to PRD/CJM and coverage ---------------
    if ux is not None:
        from collections import defaultdict
        ux_prd_cov: dict[str, list[str]] = defaultdict(list)
        ux_cjm_cov: dict[str, list[str]] = defaultdict(list)

        def collect_refs(obj, base):
            if isinstance(obj, dict):
                if "refs" in obj and isinstance(obj.get("refs"), list):
                    for s in obj["refs"]:
                        if isinstance(s, str) and s.startswith("PRD:#"):
                            pid = s.split("#",1)[1]
                            ux_prd_cov[pid].append(base)
                            if pid not in prd_ids:
                                issues.append(("ux-prd-ref-missing", f"{base} -> PRD:{pid}"))
                        if isinstance(s, str) and s.startswith("CJM:#"):
                            sid = s.split("#",1)[1]
                            ux_cjm_cov[sid].append(base)
                            if sid not in cjm_ids:
                                issues.append(("ux-cjm-ref-missing", f"{base} -> CJM:{sid}"))
                for k, v in obj.items():
                    collect_refs(v, f"{base}.{k}")
            elif isinstance(obj, list):
                for i, it in enumerate(obj):
                    collect_refs(it, f"{base}[{i}]")

        collect_refs(ux, "ux")

        hdr("PRD coverage in UX Principles (PRD id -> locations)")
        for pid in sorted(prd_ids):
            locs = ux_prd_cov.get(pid, [])
            if locs:
                print(f"{C.BOLD}- PRD:{pid}:{C.RESET}")
                for l in locs:
                    print(f"    • {l}")
            else:
                warn(f"PRD:{pid}: (no references)")

        hdr("CJM coverage in UX Principles (CJM id -> locations)")
        for cid in sorted(cjm_ids):
            locs = ux_cjm_cov.get(cid, [])
            if locs:
                print(f"{C.BOLD}- CJM:{cid}:{C.RESET}")
                for l in locs:
                    print(f"    • {l}")
            else:
                warn(f"CJM:{cid}: (no references)")

    # --------------- User Stories: validate refs and coverage ---------------
    if stories is not None:
        import re
        # Build sets for FLOW validation (UserFlow ids)
        node_ids = {n.get("id") for n in uf.get("user_flow", []) or [] if isinstance(n, dict) and n.get("id")}
        edge_ids = set()
        for n in uf.get("user_flow", []) or []:
            for e in n.get("edges", []) or []:
                if isinstance(e, dict) and e.get("id"):
                    edge_ids.add(e.get("id"))

        from collections import defaultdict
        stories_prd_cov: dict[str, list[str]] = defaultdict(list)
        stories_cjm_cov: dict[str, list[str]] = defaultdict(list)
        stories_flow_cov: dict[str, list[str]] = defaultdict(list)

        def check_line_for_refs(line: str, base: str):
            # Supports patterns like PRD:#4_2, CJM:#daily-logging, FLOW:#node-id, UserFlow:#node-id
            for m in re.finditer(r"(PRD|CJM|FLOW|UserFlow):#([A-Za-z0-9_\-]+)", line):
                kind, ident = m.group(1), m.group(2)
                if kind == "PRD":
                    if ident not in prd_ids:
                        issues.append(("stories-prd-ref-missing", f"{base} -> PRD:{ident}"))
                    stories_prd_cov[ident].append(base)
                elif kind == "CJM":
                    if ident not in cjm_ids:
                        issues.append(("stories-cjm-ref-missing", f"{base} -> CJM:{ident}"))
                    stories_cjm_cov[ident].append(base)
                else:  # FLOW/UserFlow
                    # accept if ident is a node id or an edge id
                    if ident not in node_ids and ident not in edge_ids:
                        issues.append(("stories-flow-ref-missing", f"{base} -> FLOW:{ident}"))
                    stories_flow_cov[ident].append(base)

        for i, s in enumerate(stories.get("stories", []) or []):
            base = f"stories[{i}]"
            for j, ac in enumerate(s.get("acceptance_criteria", []) or []):
                check_line_for_refs(ac, f"{base}.acceptance_criteria[{j}]")
            # metrics
            metrics = s.get("metrics", {}) or {}
            for kind in ("leading", "lagging"):
                arr = metrics.get(kind) or []
                if isinstance(arr, list):
                    for k, mobj in enumerate(arr):
                        if isinstance(mobj, dict) and isinstance(mobj.get("kpi_ref"), str):
                            kr = mobj["kpi_ref"]
                            if kr.startswith("PRD:#"):
                                pid = kr.split("#",1)[1]
                                if pid not in prd_ids:
                                    issues.append(("stories-kpi-prd-ref-missing", f"{base}.metrics.{kind}[{k}] -> PRD:{pid}"))
                                stories_prd_cov[pid].append(f"{base}.metrics.{kind}[{k}]")

        # Print coverage maps for stories
        hdr("PRD coverage in User Stories (PRD id -> locations)")
        for pid in sorted(prd_ids):
            locs = stories_prd_cov.get(pid, [])
            if locs:
                print(f"{C.BOLD}- PRD:{pid}:{C.RESET}")
                for l in locs:
                    print(f"    • {l}")
            else:
                warn(f"PRD:{pid}: (no references)")

        hdr("CJM coverage in User Stories (CJM id -> locations)")
        for cid in sorted(cjm_ids):
            locs = stories_cjm_cov.get(cid, [])
            if locs:
                print(f"{C.BOLD}- CJM:{cid}:{C.RESET}")
                for l in locs:
                    print(f"    • {l}")
            else:
                warn(f"CJM:{cid}: (no references)")

        hdr("FLOW coverage in User Stories (UserFlow id -> story references)")
        # Show only referenced ones to keep output shorter
        for ident in sorted(stories_flow_cov.keys()):
            locs = stories_flow_cov[ident]
            print(f"{C.BOLD}- FLOW:{ident}:{C.RESET}")
            for l in locs:
                print(f"    • {l}")

    # --------------- HIG Patterns: validate schema, source links, governance, and story links ---------------
    if hig is not None:
        # source_files must point to existing files
        sf = hig.get("source_files", {}) or {}
        expected = {
            "prd": PRD_PATH.name,
            "cjm": CJM_PATH.name,
            "user_flow": UF_PATH.name,
            "user_stories": STORIES_PATH.name,
            "ux_principles": UX_PATH.name,
        }
        for k, v in expected.items():
            actual = sf.get(k)
            if actual != v:
                issues.append(("hig-source-file-mismatch", f"{k}: expected {v}, got {actual}"))

        # governing rules
        gr = hig.get("governing_rules", {}) or {}
        # iOS min must be >= 18.0 (per user global rules)
        ios_min = (gr.get("ios_min") or "").strip()
        def _parse_ver(s):
            try:
                parts = s.split('.')
                return tuple(int(x) for x in (parts + ['0','0'])[:2])
            except Exception:
                return (0,0)
        if _parse_ver(ios_min) < _parse_ver("18.0"):
            issues.append(("hig-ios-min-too-low", f"ios_min={ios_min}, require >= 18.0"))
        if gr.get("swiftui_only") is not True:
            issues.append(("hig-swiftui-only", "swiftui_only must be true"))

        # cross-link story_id existence
        story_ids = {s.get("story_id") for s in (stories or {}).get("stories", []) or [] if isinstance(s, dict)}
        for i, st in enumerate(hig.get("stories", []) or []):
            sid = st.get("story_id")
            if sid and sid not in story_ids:
                issues.append(("hig-story-not-found", f"stories[{i}].story_id={sid}"))

        # stricter per-story checks: require at least one HIG section and SwiftUI primitive across candidates
        for i, st in enumerate(hig.get("stories", []) or []):
            cands = st.get("candidates", []) or []
            has_hig = any(isinstance(c, dict) and c.get("hig_sections") for c in cands)
            has_swiftui = any(isinstance(c, dict) and c.get("swiftui_primitives") for c in cands)
            if not has_hig:
                issues.append(("hig-story-missing-hig-section", f"stories[{i}].story_id={st.get('story_id')}"))
            if not has_swiftui:
                issues.append(("hig-story-missing-swiftui-primitive", f"stories[{i}].story_id={st.get('story_id')}"))

    # --------------- Contextual UX Guidelines: validate schema and cross-refs ---------------
    if ctxux is not None:
        # schema basics
        if not isinstance(ctxux, dict):
            issues.append(("schema", "ContextualUX: root must be object"))
        else:
            if "local_principles" in ctxux and not isinstance(ctxux.get("local_principles"), list):
                issues.append(("schema", "ContextualUX: 'local_principles' must be array"))
            if "antipatterns_registry" in ctxux and not isinstance(ctxux.get("antipatterns_registry"), list):
                issues.append(("schema", "ContextualUX: 'antipatterns_registry' must be array if present"))

        # Build indices for cross-refs
        story_ids = {s.get("story_id") for s in (stories or {}).get("stories", []) or [] if isinstance(s, dict)}
        ux_principle_ids = set()
        if ux is not None:
            for p in ux.get("principles", []) or []:
                pid = p.get("id")
                if isinstance(pid, str):
                    ux_principle_ids.add(pid)

        node_ids = {n.get("id") for n in uf.get("user_flow", []) or [] if isinstance(n, dict) and n.get("id")}
        # Known analytics events come from monolith analytics_events (if present),
        # all node/edge analytics arrays, and the source registry specs/02_userflow/analytics/events.json
        analytics_names = {a.get("event") for a in uf.get("analytics_events", []) or [] if isinstance(a, dict) and a.get("event")}
        for n in uf.get("user_flow", []) or []:
            for ev in (n.get("analytics") or []):
                if isinstance(ev, str):
                    analytics_names.add(ev)
            for e in n.get("edges", []) or []:
                for ev in (e.get("analytics") or []):
                    if isinstance(ev, str):
                        analytics_names.add(ev)
        # Add events from registry file if present
        try:
            reg = json.load((ROOT / "specs" / "02_userflow" / "analytics" / "events.json").open("r", encoding="utf-8"))
            for ev in reg.get("events", []) or []:
                if isinstance(ev, str):
                    analytics_names.add(ev)
        except Exception:
            pass

        # Validate meta.context screen_id against UserFlow node ids (warn if missing)
        for ctx in (ctxux.get("meta", {}) or {}).get("context", []) or []:
            sid = None
            if isinstance(ctx, dict):
                sid = ctx.get("screen_id")
            elif isinstance(ctx, str):
                sid = ctx
            if sid and sid not in node_ids:
                issues.append(("warn-ctxux-screen-not-in-userflow", sid))

        # Validate local principles
        from collections import defaultdict
        ctxux_story_cov: dict[str, list[str]] = defaultdict(list)
        ctxux_ux_cov: dict[str, list[str]] = defaultdict(list)

        for i, lp in enumerate(ctxux.get("local_principles", []) or []):
            base = f"ctxux.local_principles[{i}]"
            # user_story_ids coverage
            us_arr = lp.get("user_story_ids") or []
            if not isinstance(us_arr, list) or not us_arr:
                issues.append(("warn-ctxux-missing-links", f"{base}: missing user_story_ids"))
            else:
                for sid in us_arr:
                    if isinstance(sid, str):
                        if sid not in story_ids:
                            issues.append(("ctxux-story-ref-missing", f"{base} -> UserStory:{sid}"))
                        else:
                            ctxux_story_cov[sid].append(base)
            # global_principle_ids coverage
            gp_arr = lp.get("global_principle_ids") or []
            if not isinstance(gp_arr, list) or not gp_arr:
                issues.append(("warn-ctxux-missing-links", f"{base}: missing global_principle_ids"))
            else:
                for gid in gp_arr:
                    if isinstance(gid, str):
                        if ux is not None and gid not in ux_principle_ids:
                            issues.append(("ctxux-global-principle-missing", f"{base} -> UX:{gid}"))
                        else:
                            ctxux_ux_cov[gid].append(base)
            # telemetry can be a list of event names, or an object
            tele = lp.get("telemetry")
            if isinstance(tele, list):
                for ev in tele:
                    if isinstance(ev, str) and ev and ev not in analytics_names:
                        issues.append(("ctxux-telemetry-event-unknown", f"{base} -> {ev}"))
            elif isinstance(tele, dict):
                ev = tele.get("event")
                if isinstance(ev, str) and ev and ev not in analytics_names:
                    issues.append(("ctxux-telemetry-event-unknown", f"{base} -> {ev}"))

        # antipatterns_registry refs to UserStory
        for i, ap in enumerate(ctxux.get("antipatterns_registry", []) or []):
            base = f"ctxux.antipatterns_registry[{i}]"
            for r in ap.get("refs", []) or []:
                if isinstance(r, str) and r.startswith("UserStory:#"):
                    sid = r.split("#", 1)[1]
                    if sid not in story_ids:
                        issues.append(("ctxux-story-ref-missing", f"{base} -> UserStory:{sid}"))

        # Coverage outputs
        hdr("Contextual UX coverage: UserStory id -> local principles")
        for sid in sorted(story_ids):
            locs = ctxux_story_cov.get(sid, [])
            if locs:
                print(f"{C.BOLD}- UserStory:{sid}:{C.RESET}")
                for l in locs:
                    print(f"    • {l}")
            else:
                warn(f"UserStory:{sid}: (no local principles)")

        if ux is not None:
            hdr("Contextual UX coverage: UX global principle id -> local principles")
            for gid in sorted(ux_principle_ids):
                locs = ctxux_ux_cov.get(gid, [])
                if locs:
                    print(f"{C.BOLD}- UX:{gid}:{C.RESET}")
                    for l in locs:
                        print(f"    • {l}")
                else:
                    warn(f"UX:{gid}: (no local principles)")

    if issues:
        hdr("Issues found")
        from collections import Counter
        fatal = [(k, v) for (k, v) in issues if not str(k).startswith("warn-")]
        warns = [(k, v) for (k, v) in issues if str(k).startswith("warn-")]
        print(f"{C.RED}Total: {len(fatal)} fatal{C.RESET}, {C.YELLOW}{len(warns)} warning(s){C.RESET}")
        from collections import Counter
        counts = Counter(k for k,_ in issues)
        for k, c in counts.most_common():
            err(f"{k}: {c}")
        hdr("Details")
        for k, v in issues:
            if str(k).startswith("warn-"):
                print(f"  - {C.YELLOW}{k}{C.RESET}: {v}")
            else:
                print(f"  - {C.RED}{k}{C.RESET}: {v}")
        sys.exit(1 if fatal else 0)
    else:
        ok("No issues found. Cross-spec trace looks consistent.")
        sys.exit(0)


if __name__ == "__main__":
    main()
