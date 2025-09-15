#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SpecHub docs generator

Generates Markdown pages in docs/ from specs/_build/*.json and renders DOT→SVG diagrams.
MVP scope:
 - Parse PRD, CJM, User Flow, User Stories, UX Principles, HIG, Contextual UX JSONs
 - Create per-entity Markdown using Jinja2 templates in docs/_templates/
 - Render userflow.svg and coverage.svg into docs/_media/
 - Build mkdocs.yml navigation automatically based on generated files

This script is idempotent and safe to run multiple times.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
import subprocess
import datetime

# Third-party
from jinja2 import Environment, FileSystemLoader, select_autoescape
import pydot

# Optional import: markdownify for rich text fallbacks
try:
    from markdownify import markdownify as md
except Exception:
    def md(s: str) -> str:
        return s

def page_exists(rel_path: str) -> bool:
    return (DOCS_DIR / rel_path).exists()

def chip(rel_path: Optional[str], label: str) -> Dict[str, Optional[str]]:
    if rel_path and page_exists(rel_path):
        return {"label": label, "href": rel_path}
    return {"label": label, "href": None}

ROOT = Path(__file__).resolve().parents[1]
BUILD_DIR = ROOT / "specs" / "_build"
DOCS_DIR = ROOT / "docs"
MEDIA_DIR = DOCS_DIR / "_media"
TMPL_DIR = DOCS_DIR / "_templates"
CONFIG_FILE = ROOT / "spechub.yml"

REQUIRED_FILES = {
    "prd": BUILD_DIR / "00_PRD_v1.json",
    "cjm": BUILD_DIR / "01_CJM_v1.json",
    "flow": BUILD_DIR / "02_UserFlow_v1.json",
    "ux": BUILD_DIR / "03_Global_UX_Principles_v1.json",
    "stories": BUILD_DIR / "04_UserStories_v1.json",
    "hig": BUILD_DIR / "05_HIG_Pattern_selection_v1.json",
    "ctxux": BUILD_DIR / "06_Contextual_UX_Guidelines_v1.json",
}

GRAPH_FILE = BUILD_DIR / "graph.json"  # optional in MVP; script should tolerate absence


def ensure_dirs() -> None:
    for d in [DOCS_DIR, MEDIA_DIR, TMPL_DIR, DOCS_DIR / "prd", DOCS_DIR / "cjm", DOCS_DIR / "flow", DOCS_DIR / "flow" / "nodes", DOCS_DIR / "stories", DOCS_DIR / "ux", DOCS_DIR / "hig", DOCS_DIR / "ctxux", DOCS_DIR / "coverage"]:
        d.mkdir(parents=True, exist_ok=True)


def slugify(s: str) -> str:
    return (
        s.strip()
        .lower()
        .replace(" ", "-")
        .replace("/", "-")
        .replace(":", "-")
    )


def get_repo_base() -> Tuple[Optional[str], str]:
    """Return (repo_url, default_branch) for building edit links.

    - Try git remote origin; convert SSH to HTTPS.
    - Fallback to SPECHUB_REPO and SPECHUB_DEFAULT_BRANCH env vars.
    - If none available, return (None, branch).
    """
    # Prefer spechub.yml if present
    cfg_repo: Optional[str] = None
    cfg_branch: Optional[str] = None
    try:
        if CONFIG_FILE.exists():
            import yaml  # type: ignore
            cfg = yaml.safe_load(CONFIG_FILE.read_text(encoding="utf-8")) or {}
            cfg_repo = cfg.get("repo_url")
            cfg_branch = cfg.get("default_branch")
    except Exception:
        cfg_repo = None
        cfg_branch = None
    env_repo = os.environ.get("SPECHUB_REPO")
    default_branch = cfg_branch or os.environ.get("SPECHUB_DEFAULT_BRANCH", "main")
    repo_url: Optional[str] = None
    try:
        out = subprocess.check_output(["git", "remote", "get-url", "origin"], cwd=str(ROOT), stderr=subprocess.DEVNULL)
        remote = out.decode().strip()
        # Convert SSH like git@github.com:org/repo.git to https://github.com/org/repo
        if remote.startswith("git@github.com:"):
            path = remote.split(":", 1)[1]
            if path.endswith(".git"):
                path = path[:-4]
            repo_url = f"https://github.com/{path}"
        elif remote.startswith("https://") or remote.startswith("http://"):
            repo_url = remote[:-4] if remote.endswith(".git") else remote
    except Exception:
        repo_url = None
    if not repo_url:
        repo_url = cfg_repo or env_repo
    return repo_url, default_branch


REPO_URL, REPO_BRANCH = get_repo_base()


def edit_link(rel_path: str) -> str:
    """Build an edit/source link pointing to repo file path.

    If repo URL unavailable, return the relative path.
    """
    if REPO_URL:
        # Use blob path for viewing; rely on GitHub default file viewer
        return f"{REPO_URL}/blob/{REPO_BRANCH}/{rel_path}"
    return rel_path


def load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_build_artifacts() -> Dict[str, Dict[str, Any]]:
    missing = [k for k, p in REQUIRED_FILES.items() if not p.exists()]
    if missing:
        print(f"[WARN] Missing build artifacts: {missing}")
    data = {}
    for key, path in REQUIRED_FILES.items():
        if path.exists():
            data[key] = load_json(path)
    return data


def load_graph() -> Dict[str, Any]:
    if GRAPH_FILE.exists():
        return load_json(GRAPH_FILE)
    return {"nodes": [], "edges": []}


def jinja_env() -> Environment:
    env = Environment(
        loader=FileSystemLoader(str(TMPL_DIR)),
        autoescape=select_autoescape(disabled_extensions=("md",), default_for_string=False),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    env.filters["slugify"] = slugify
    # Expose repo globals to templates
    env.globals["REPO_URL"] = REPO_URL
    env.globals["REPO_BRANCH"] = REPO_BRANCH
    return env


# ---------- Rendering helpers ----------
def get_build_info() -> Dict[str, str]:
    ts = datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
    try:
        sha = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], cwd=str(ROOT)).decode().strip()
    except Exception:
        sha = "unknown"
    return {"timestamp": ts, "git_sha": sha}

def write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        f.write(content)


def render_index(env: Environment, artifacts: Dict[str, Any], graph: Dict[str, Any]) -> None:
    tmpl = env.get_template("index.md.j2")
    # Basic counts for MVP
    prd_sections = len(artifacts.get("prd", {}).get("sections", [])) or len(artifacts.get("prd", {}).get("prd", []))
    cjm_stages = len(artifacts.get("cjm", {}).get("stages", [])) or len(artifacts.get("cjm", {}).get("cjm", []))
    flow_nodes = len(artifacts.get("flow", {}).get("user_flow", []))
    stories = len(artifacts.get("stories", {}).get("stories", []))
    ctxux_screens = len(artifacts.get("ctxux", {}).get("screens", []))

    bi = get_build_info()

    content = tmpl.render(
        prd_sections=prd_sections,
        cjm_stages=cjm_stages,
        flow_nodes=flow_nodes,
        stories=stories,
        ctxux_screens=ctxux_screens,
        has_graph=bool(graph.get("nodes")),
        versions={
            "prd": artifacts.get("prd", {}).get("version"),
            "cjm": artifacts.get("cjm", {}).get("version"),
            "flow": artifacts.get("flow", {}).get("version"),
            "stories": artifacts.get("stories", {}).get("version"),
            "hig": artifacts.get("hig", {}).get("version"),
            "ux": artifacts.get("ux", {}).get("version"),
            "ctxux": artifacts.get("ctxux", {}).get("version"),
        },
        build_info=bi,
    )
    write_file(DOCS_DIR / "index.md", content)
    # Persist build info for footer injection
    build_meta = {**bi, "repo_url": REPO_URL or "", "branch": REPO_BRANCH}
    write_file(DOCS_DIR / "assets" / "build.json", json.dumps(build_meta))


def render_prd(env: Environment, prd: Dict[str, Any], graph: Dict[str, Any]) -> None:
    if not prd:
        return
    tmpl = env.get_template("prd_section.md.j2")
    prd_version = prd.get("version")
    for section in prd.get("sections", []):
        sec_id = section.get("id") or section.get("section_id") or "unknown"
        path = DOCS_DIR / "prd" / f"{slugify(str(sec_id))}.md"
        edit_href = edit_link(f"specs/00_prd/sections/{sec_id}.json")
        # Cross-links from PRD section
        prd_nid = f"prd:{sec_id}"
        story_ids = [s.split(":",1)[1] for s in _connected(graph, prd_nid, "story:")]
        flow_nodes = [n.split(":",2)[2] for n in _connected(graph, prd_nid, "flow:node:")]
        story_chips = [{"label": st, "href": f"../stories/{slugify(st)}.md"} for st in story_ids if page_exists(f"stories/{slugify(st)}.md")]
        flow_chips = [{"label": fn, "href": f"../flow/nodes/{slugify(fn)}.md"} for fn in flow_nodes if page_exists(f"flow/nodes/{slugify(fn)}.md")]
        xlinks = {"stories": story_chips, "flow": flow_chips}
        schema_status = os.environ.get("SPECHUB_SCHEMA_STATUS", "unknown").lower()
        schema_ok = True if schema_status == "ok" else False if schema_status == "failed" else None
        content = tmpl.render(section=section, edit_href=edit_href, version=prd_version, build_info=get_build_info(), schema_ok=schema_ok, xlinks=xlinks)
        write_file(path, content)


def render_cjm(env: Environment, cjm: Dict[str, Any], graph: Dict[str, Any]) -> None:
    if not cjm:
        return
    tmpl = env.get_template("cjm_stage.md.j2")
    cjm_version = cjm.get("version")
    for stage in cjm.get("stages", []):
        st_id = stage.get("id") or stage.get("stage_id") or "unknown"
        path = DOCS_DIR / "cjm" / f"{slugify(str(st_id))}.md"
        edit_href = edit_link(f"specs/01_cjm/stages/{st_id}.json")
        # Cross-links
        cjm_nid = f"cjm:{st_id}"
        story_ids = [s.split(":",1)[1] for s in _connected(graph, cjm_nid, "story:")]
        flow_nodes = [n.split(":",2)[2] for n in _connected(graph, cjm_nid, "flow:node:")]
        story_chips = [{"label": st, "href": f"../stories/{slugify(st)}.md"} for st in story_ids if page_exists(f"stories/{slugify(st)}.md")]
        flow_chips = [{"label": fn, "href": f"../flow/nodes/{slugify(fn)}.md"} for fn in flow_nodes if page_exists(f"flow/nodes/{slugify(fn)}.md")]
        xlinks = {"stories": story_chips, "flow": flow_chips}
        schema_status = os.environ.get("SPECHUB_SCHEMA_STATUS", "unknown").lower()
        schema_ok = True if schema_status == "ok" else False if schema_status == "failed" else None
        content = tmpl.render(stage=stage, edit_href=edit_href, version=cjm_version, build_info=get_build_info(), schema_ok=schema_ok, xlinks=xlinks)
        write_file(path, content)


def render_flow(env: Environment, flow: Dict[str, Any], graph: Dict[str, Any]) -> None:
    if not flow:
        return
    # Overview page with embeddable SVG (object) for pan/zoom
    overview = (
        "# User Flow\n\n"
        "<figure class=\"graph\">\n"
        "  <object type=\"image/svg+xml\" data=\"../_media/userflow.svg\" id=\"userflow-object\" aria-label=\"User Flow diagram\"></object>\n"
        "</figure>\n"
    )
    write_file(DOCS_DIR / "flow" / "overview.md", overview)

    tmpl = env.get_template("flow_node.md.j2")
    flow_version = flow.get("version")
    for node in flow.get("user_flow", []):
        node_id = node.get("id")
        if not node_id:
            continue
        path = DOCS_DIR / "flow" / "nodes" / f"{slugify(node_id)}.md"
        # For edit link, map by type if needed. Node definitions live in specs/02_userflow/nodes/<domain>.json
        # We cannot always derive the domain file; provide folder link as fallback
        edit_href = edit_link("specs/02_userflow/nodes/")
        # Cross-links (relative to docs/flow/nodes/<node>.md)
        nid = f"flow:node:{node_id}"
        prd_ids = [p.split(":",1)[1] for p in _connected(graph, nid, "prd:")]
        cjm_ids = [c.split(":",1)[1] for c in _connected(graph, nid, "cjm:")]
        story_ids = [s.split(":",1)[1] for s in _connected(graph, nid, "story:")]
        ctx_screens = [n.split(":",2)[2] for n in _connected(graph, nid, "ctxux:screen:")]
        prd_chips = [{"label": pid, "href": f"../../prd/{slugify(pid)}.md"} for pid in prd_ids if page_exists(f"prd/{slugify(pid)}.md")]
        cjm_chips = [{"label": cid, "href": f"../../cjm/{slugify(cid)}.md"} for cid in cjm_ids if page_exists(f"cjm/{slugify(cid)}.md")]
        story_chips = [{"label": st, "href": f"../../stories/{slugify(st)}.md"} for st in story_ids if page_exists(f"stories/{slugify(st)}.md")]
        ctx_chips = [{"label": cs, "href": f"../../ctxux/{slugify(cs)}.md"} for cs in ctx_screens if page_exists(f"ctxux/{slugify(cs)}.md")]
        xlinks = {"prd": prd_chips, "cjm": cjm_chips, "stories": story_chips, "ctxux": ctx_chips}
        schema_status = os.environ.get("SPECHUB_SCHEMA_STATUS", "unknown").lower()
        schema_ok = True if schema_status == "ok" else False if schema_status == "failed" else None
        content = tmpl.render(node=node, edit_href=edit_href, version=flow_version, build_info=get_build_info(), schema_ok=schema_ok, xlinks=xlinks)
        write_file(path, content)


def render_stories(env: Environment, stories: Dict[str, Any], graph: Dict[str, Any]) -> None:
    if not stories:
        return
    tmpl = env.get_template("story.md.j2")
    us_version = stories.get("version")
    for story in stories.get("stories", []):
        sid = story.get("story_id")
        if not sid:
            continue
        path = DOCS_DIR / "stories" / f"{slugify(sid)}.md"
        edit_href = edit_link(f"specs/04_userstories/us/{sid}.json")
        # Cross-links (relative to docs/stories/<sid>.md)
        story_nid = f"story:{sid}"
        prd_ids = [p.split(":",1)[1] for p in _connected(graph, story_nid, "prd:")]
        cjm_ids = [c.split(":",1)[1] for c in _connected(graph, story_nid, "cjm:")]
        flow_nodes = [n.split(":",2)[2] for n in _connected(graph, story_nid, "flow:node:")]
        ctx_screens = [n.split(":",2)[2] for n in _connected(graph, story_nid, "ctxux:screen:")]
        prd_chips = [{"label": pid, "href": f"../prd/{slugify(pid)}.md"} for pid in prd_ids if page_exists(f"prd/{slugify(pid)}.md")]
        cjm_chips = [{"label": cid, "href": f"../cjm/{slugify(cid)}.md"} for cid in cjm_ids if page_exists(f"cjm/{slugify(cid)}.md")]
        flow_chips = [{"label": fn, "href": f"../flow/nodes/{slugify(fn)}.md"} for fn in flow_nodes if page_exists(f"flow/nodes/{slugify(fn)}.md")]
        ctx_chips = [{"label": cs, "href": f"../ctxux/{slugify(cs)}.md"} for cs in ctx_screens if page_exists(f"ctxux/{slugify(cs)}.md")]
        hig_href = f"../hig/{slugify(sid)}.md" if page_exists(f"hig/{slugify(sid)}.md") else None
        xlinks = {"prd": prd_chips, "cjm": cjm_chips, "flow": flow_chips, "ctxux": ctx_chips, "hig": {"label": "HIG", "href": hig_href}}
        schema_status = os.environ.get("SPECHUB_SCHEMA_STATUS", "unknown").lower()
        schema_ok = True if schema_status == "ok" else False if schema_status == "failed" else None
        content = tmpl.render(story=story, edit_href=edit_href, version=us_version, build_info=get_build_info(), schema_ok=schema_ok, xlinks=xlinks)
        write_file(path, content)


def render_ux(env: Environment, ux: Dict[str, Any], graph: Dict[str, Any]) -> None:
    if not ux:
        return
    tmpl = env.get_template("ux_principle.md.j2")
    ux_version = ux.get("version")
    for principle in ux.get("principles", []) or ux.get("global_principles", []) or []:
        pid = principle.get("id") or principle.get("principle_id")
        if not pid:
            continue
        path = DOCS_DIR / "ux" / f"{slugify(pid)}.md"
        edit_href = edit_link(f"specs/03_ux_principles/principles/{pid}.json")
        schema_status = os.environ.get("SPECHUB_SCHEMA_STATUS", "unknown").lower()
        schema_ok = True if schema_status == "ok" else False if schema_status == "failed" else None
        content = tmpl.render(principle=principle, edit_href=edit_href, version=ux_version, build_info=get_build_info(), schema_ok=schema_ok)
        write_file(path, content)


def render_ctxux(env: Environment, ctxux: Dict[str, Any], graph: Dict[str, Any]) -> None:
    if not ctxux:
        return
    tmpl = env.get_template("ctxux_screen.md.j2")
    ctxux_version = ctxux.get("version")
    for screen in ctxux.get("screens", []):
        sid = screen.get("id")
        if not sid:
            continue
        path = DOCS_DIR / "ctxux" / f"{slugify(sid)}.md"
        edit_href = edit_link(f"specs/06_ctxux/screens/{sid}.json")
        # Cross-links
        nid = f"ctxux:screen:{sid}"
        flow_nodes = [n.split(":",2)[2] for n in _connected(graph, nid, "flow:node:")]
        story_ids = [s.split(":",1)[1] for s in _connected(graph, nid, "story:")]
        flow_chips = [{"label": fn, "href": f"../flow/nodes/{slugify(fn)}.md"} for fn in flow_nodes if page_exists(f"flow/nodes/{slugify(fn)}.md")]
        story_chips = [{"label": st, "href": f"../stories/{slugify(st)}.md"} for st in story_ids if page_exists(f"stories/{slugify(st)}.md")]
        xlinks = {"flow": flow_chips, "stories": story_chips}
        schema_status = os.environ.get("SPECHUB_SCHEMA_STATUS", "unknown").lower()
        schema_ok = True if schema_status == "ok" else False if schema_status == "failed" else None
        content = tmpl.render(screen=screen, edit_href=edit_href, version=ctxux_version, build_info=get_build_info(), schema_ok=schema_ok, xlinks=xlinks)
        write_file(path, content)


def render_hig(env: Environment, hig: Dict[str, Any], graph: Dict[str, Any]) -> None:
    """Render HIG recommendations per user story.

    Input structure: { "stories": [ { story_id, title, candidates: [...], recommendation: {...} } ] }
    Output: docs/hig/<story_id>.md
    Edit link: specs/05_hig/stories/<story_id>/candidates.json
    """
    if not hig:
        return
    tmpl = env.get_template("hig_story.md.j2")
    hig_version = hig.get("version")
    for story in hig.get("stories", []):
        sid = story.get("story_id")
        if not sid:
            continue
        path = DOCS_DIR / "hig" / f"{slugify(sid)}.md"
        edit_href = edit_link(f"specs/05_hig/stories/{sid}/candidates.json")
        schema_status = os.environ.get("SPECHUB_SCHEMA_STATUS", "unknown").lower()
        schema_ok = True if schema_status == "ok" else False if schema_status == "failed" else None
        content = tmpl.render(hig_story=story, edit_href=edit_href, version=hig_version, build_info=get_build_info(), schema_ok=schema_ok)
        write_file(path, content)


# ---------- Diagram rendering ----------

def render_userflow_svg(flow: Dict[str, Any]) -> None:
    if not flow:
        return
    graph = pydot.Dot(graph_type="digraph", rankdir="LR", splines="spline", overlap="false")
    # Add nodes
    for node in flow.get("user_flow", []):
        nid = node.get("id")
        ntype = node.get("type", "node")
        label = f"{nid}\n({ntype})"
        doc_path = DOCS_DIR / "flow" / "nodes" / f"{slugify(nid)}.md"
        url = f"./flow/nodes/{slugify(nid)}.md" if doc_path.exists() else None
        shape = {
            "screen": "box",
            "system": "ellipse",
            "decision": "diamond",
            "error": "octagon",
            "terminator": "oval",
        }.get(ntype, "box")
        kwargs = {"label": label, "shape": shape, "tooltip": label}
        if url:
            kwargs.update({"URL": url})
        graph.add_node(pydot.Node(nid, **kwargs))
    # Add edges
    node_index = {n.get("id"): n for n in flow.get("user_flow", [])}
    for n in flow.get("user_flow", []):
        src = n.get("id")
        for e in n.get("edges", []) or []:
            tgt = e.get("target")
            if not tgt:
                continue
            elabel = e.get("action") or e.get("id") or ""
            graph.add_edge(pydot.Edge(src, tgt, label=elabel, tooltip=elabel))
    MEDIA_DIR.mkdir(parents=True, exist_ok=True)
    graph.write_svg(str(MEDIA_DIR / "userflow.svg"))


def render_coverage_svg(graph_data: Dict[str, Any]) -> None:
    # Simple clustered landscape placeholder for MVP
    g = pydot.Dot(graph_type="digraph", rankdir="LR", compound="true", concentrate="true")

    clusters = {
        "PRD": [],
        "CJM": [],
        "FLOW_NODE": [],
        "STORY": [],
        "HIG": [],
        "UX": [],
        "CTXUX": [],
    }
    # Build URL to doc page for each node
    def node_url_for_coverage(n: Dict[str, Any]) -> str:
        nid = n.get("id", "")
        t = n.get("type")
        if t == "PRD" and nid.startswith("prd:"):
            return f"prd/{slugify(nid.split(':', 1)[1])}.md"
        if t == "CJM" and nid.startswith("cjm:"):
            return f"cjm/{slugify(nid.split(':', 1)[1])}.md"
        if t == "FLOW_NODE" and nid.startswith("flow:node:"):
            return f"flow/nodes/{slugify(nid.split(':', 2)[2])}.md"
        if t == "STORY" and nid.startswith("story:"):
            return f"stories/{slugify(nid.split(':', 1)[1])}.md"
        if t == "HIG" and nid.startswith("hig:"):
            sid = nid.split(":", 2)[1]
            return f"hig/{sid}.md"
        if t == "UX" and nid.startswith("ux:principle:"):
            return f"ux/{nid.split(':', 2)[2]}.md"
        if t == "CTXUX" and nid.startswith("ctxux:screen:"):
            return f"ctxux/{nid.split(':', 2)[2]}.md"
        # Default to flow overview for ANALYTICS/DD or unknown
        return "flow/overview.md"
    # Build a map of original ids -> safe DOT ids (colon is a port separator in DOT)
    def safe_id(s: str) -> str:
        return s.replace(":", "__")

    nodes_map = {n.get("id"): n for n in graph_data.get("nodes", [])}
    for n in graph_data.get("nodes", []):
        t = n.get("type")
        if t in clusters:
            clusters[t].append(n)

    for t, nodes_in_cluster in clusters.items():
        if not nodes_in_cluster:
            continue
        sg = pydot.Cluster(f"cluster_{t}", label=t, style="rounded")
        for n in nodes_in_cluster:
            nid = n.get("id")
            label = n.get("title") or nid
            # compute URL and only set if file exists
            url_rel = node_url_for_coverage(n)
            exists = (DOCS_DIR / url_rel).exists()
            kwargs = {"label": label, "tooltip": label}
            if exists:
                kwargs["URL"] = url_rel
            sg.add_node(pydot.Node(safe_id(nid), **kwargs))
        g.add_subgraph(sg)

    # Edges
    for e in graph_data.get("edges", []):
        src = e.get("from")
        dst = e.get("to")
        g.add_edge(pydot.Edge(safe_id(src), safe_id(dst), label=e.get("type", "")))

    g.write_svg(str(MEDIA_DIR / "coverage.svg"))


def analyze_orphans(graph: Dict[str, Any]) -> Dict[str, List[str]]:
    nodes = graph.get("nodes", [])
    edges = graph.get("edges", [])
    by_id = {n["id"]: n for n in nodes}
    incoming: Dict[str, int] = {}
    outgoing: Dict[str, int] = {}
    for e in edges:
        src = e.get("from"); dst = e.get("to")
        if src: outgoing[src] = outgoing.get(src, 0) + 1
        if dst: incoming[dst] = incoming.get(dst, 0) + 1
    orphans: Dict[str, List[str]] = {
        "STORY": [],
        "CTXUX": [],
        "FLOW_NODE": [],
        "PRD": [],
        "CJM": [],
    }
    for n in nodes:
        t = n.get("type")
        nid = n.get("id")
        inc = incoming.get(nid, 0)
        outc = outgoing.get(nid, 0)
        if t == "STORY" and inc == 0:
            orphans["STORY"].append(nid)
        if t == "CTXUX":
            # screen must have at least one map from flow
            has_map = any(e.get("to") == nid and e.get("type") in {"maps_to"} for e in edges)
            if not has_map:
                orphans["CTXUX"].append(nid)
        if t == "FLOW_NODE" and (inc + outc) == 0:
            orphans["FLOW_NODE"].append(nid)
        if t in ("PRD", "CJM") and outc == 0:
            # no influence/maps_to outward
            orphans[t].append(nid)
    # sort and return
    return {k: sorted(v) for k, v in orphans.items()}


def render_orphans(env: Environment, graph: Dict[str, Any]) -> None:
    data = analyze_orphans(graph)
    lines: List[str] = []
    lines.append("# Orphans\n")
    for section, ids in (("Stories without Flow coverage", data.get("STORY", [])),
                         ("CtxUX screens without Flow mapping", data.get("CTXUX", [])),
                         ("Flow nodes without edges", data.get("FLOW_NODE", [])),
                         ("PRD with no outgoing influence", data.get("PRD", [])),
                         ("CJM with no mapping to Flow", data.get("CJM", []))):
        lines.append(f"## {section}")
        if not ids:
            lines.append("- none")
        else:
            for nid in ids:
                # map to URL similar to coverage
                ntype = nid.split(":", 1)[0].upper()
                # compute candidate URL using same mapping as coverage
                if ntype == "STORY":
                    url_rel = f"stories/{slugify(nid.split(':',1)[1])}.md"
                elif ntype == "CTXUX":
                    url_rel = f"ctxux/{nid.split(':',2)[2]}.md"
                elif ntype == "FLOW":
                    url_rel = f"flow/nodes/{slugify(nid.split(':',2)[2])}.md"
                elif ntype == "PRD":
                    url_rel = f"prd/{slugify(nid.split(':',1)[1])}.md"
                elif ntype == "CJM":
                    url_rel = f"cjm/{slugify(nid.split(':',1)[1])}.md"
                else:
                    url_rel = None
                # only create link if file exists; otherwise render as plain text to satisfy mkdocs strict
                if url_rel and (DOCS_DIR / url_rel).exists():
                    lines.append(f"- [{nid}]({url_rel})")
                else:
                    lines.append(f"- {nid}")
        lines.append("")
    write_file(DOCS_DIR / "orphans.md", "\n".join(lines))


def render_coverage_matrices(artifacts: Dict[str, Any], graph: Dict[str, Any]) -> None:
    # PRD ↔ Stories matrix
    prd_ids = [s.get("id") for s in (artifacts.get("prd", {}).get("prd", []) or artifacts.get("prd", {}).get("sections", []) or [])]
    story_ids = [s.get("story_id") for s in artifacts.get("stories", {}).get("stories", []) or []]
    edges = graph.get("edges", [])
    covered = {(e.get("from"), e.get("to")) for e in edges}
    lines1: List[str] = []
    lines1.append("# PRD ↔ Stories\n")
    # header
    header = "| PRD "+ " | ".join(story_ids) + " |\n"
    sep = "|" + "---|" * (1 + len(story_ids)) + "\n"
    lines1.append(header)
    lines1.append(sep)
    for pid in prd_ids:
        row = [f"prd:{pid}"]
        for sid in story_ids:
            mark = "✔" if (f"prd:{pid}", f"story:{sid}") in covered else ""
            row.append(mark)
        lines1.append("| " + " | ".join(row) + " |")
    write_file(DOCS_DIR / "coverage" / "prd_stories.md", "\n".join(lines1) + "\n")

    # Flow ↔ CtxUX matrix
    flow_nodes = [n.get("id").split(":",2)[2] for n in graph.get("nodes", []) if n.get("type") == "FLOW_NODE"]
    ctx_screens = [n.get("id").split(":",2)[2] for n in graph.get("nodes", []) if n.get("type") == "CTXUX"]
    lines2: List[str] = []
    lines2.append("# Flow ↔ Contextual UX\n")
    header2 = "| Flow Node "+ " | ".join(ctx_screens) + " |\n"
    sep2 = "|" + "---|" * (1 + len(ctx_screens)) + "\n"
    lines2.append(header2)
    lines2.append(sep2)
    for fn in flow_nodes:
        row = [fn]
        for scr in ctx_screens:
            mark = "✔" if (f"flow:node:{fn}", f"ctxux:screen:{scr}") in covered else ""
            row.append(mark)
        lines2.append("| " + " | ".join(row) + " |")
    write_file(DOCS_DIR / "coverage" / "flow_ctxux.md", "\n".join(lines2) + "\n")


# ---------- mkdocs nav ----------

def build_nav() -> str:
    """Compose mkdocs.yml nav section as YAML string (indented)."""
    def list_md(dir_path: Path) -> List[str]:
        return sorted([p.name for p in dir_path.glob("*.md") if p.name != "index.md"]) if dir_path.exists() else []

    lines: List[str] = []
    lines.append("nav:")
    lines.append("  - Overview: index.md")
    # Orphans and Coverage
    if (DOCS_DIR / "orphans.md").exists():
        lines.append("  - Orphans: orphans.md")
    if (DOCS_DIR / "coverage").exists():
        cov = sorted([p.name for p in (DOCS_DIR / "coverage").glob("*.md")])
        if cov:
            lines.append("  - Coverage:")
            for name in cov:
                title = os.path.splitext(name)[0].replace("_", " ")
                lines.append(f"      - {title}: coverage/{name}")
    # Flow overview first
    if (DOCS_DIR / "flow" / "overview.md").exists():
        lines.append("  - User Flow:")
        lines.append("      - Overview: flow/overview.md")
        if (DOCS_DIR / "flow" / "index.md").exists():
            lines.append("      - Index: flow/index.md")
        for fname in list_md(DOCS_DIR / "flow" / "nodes"):
            name = os.path.splitext(fname)[0]
            lines.append(f"      - {name}: flow/nodes/{fname}")
    # nested helper to add sections with optional Index
    def section(title: str, rel: str, dir_path: Path):
        files = list_md(dir_path)
        has_index = (dir_path / "index.md").exists()
        if not files and not has_index:
            return
        lines.append(f"  - {title}:")
        if has_index:
            lines.append(f"      - Index: {rel}/index.md")
        for fname in files:
            name = os.path.splitext(fname)[0]
            lines.append(f"      - {name}: {rel}/{fname}")

    section("User Stories", "stories", DOCS_DIR / "stories")
    section("Global UX Principles", "ux", DOCS_DIR / "ux")
    section("Contextual UX", "ctxux", DOCS_DIR / "ctxux")
    section("HIG Patterns", "hig", DOCS_DIR / "hig")

    return "\n".join(lines) + "\n"


def write_mkdocs_yaml() -> None:
    mkdocs_path = ROOT / "mkdocs.yml"
    bi = get_build_info()
    cache_bust = bi.get("git_sha", "dev")
    base = f"""
site_name: SpecHub
site_url: https://alexivengo.github.io/dailylogs-specs/
site_description: Specification Hub
theme:
  name: material
  language: ru
  features:
    - navigation.instant
    - navigation.tracking
    - navigation.top
    - navigation.tabs
    - navigation.indexes
    - toc.integrate
    - content.code.copy
    - search.suggest
  palette:
    - scheme: default
      primary: indigo
      accent: indigo
plugins:
  - search:
      lang: [ru, en]
      separator: '[\\s\\-]+'
markdown_extensions:
  - admonition
  - toc:
      permalink: true
extra:
  generator: spechub
# We add custom 'Edit source' links inside pages instead of using edit_uri
extra_javascript:
  - assets/javascripts/spechub.js?v={cache_bust}
extra_css:
  - assets/stylesheets/spechub.css?v={cache_bust}
{build_nav()}""".lstrip()
    write_file(mkdocs_path, base)


# ---------- Index pages ----------

def _edges(graph: Dict[str, Any]) -> List[Dict[str, Any]]:
    return graph.get("edges", []) or []

def _connected(graph: Dict[str, Any], node_id: str, prefix: str) -> List[str]:
    out: set[str] = set()
    for e in _edges(graph):
        f = e.get("from"); t = e.get("to")
        if not f or not t: continue
        if f == node_id and t.startswith(prefix):
            out.add(t)
        if t == node_id and f.startswith(prefix):
            out.add(f)
    return sorted(out)

def render_stories_index(artifacts: Dict[str, Any], graph: Dict[str, Any]) -> None:
    data = artifacts.get("stories", {})
    stories = data.get("stories", []) or []
    lines: List[str] = []
    lines.append("# User Stories\n")
    lines.append("| ID | Название | PRD | CJM | Flow | HIG | CtxUX |")
    lines.append("|---|---|---|---|---|---|---|")
    for s in stories:
        sid = s.get("story_id")
        if not sid: 
            continue
        title = s.get("title", "")
        story_nid = f"story:{sid}"
        prd_ids = [p.split(":",1)[1] for p in _connected(graph, story_nid, "prd:")]
        cjm_ids = [c.split(":",1)[1] for c in _connected(graph, story_nid, "cjm:")]
        flow_nodes = [n.split(":",2)[2] for n in _connected(graph, story_nid, "flow:node:")]
        ctx_screens = [n.split(":",2)[2] for n in _connected(graph, story_nid, "ctxux:screen:")]
        prd_cell = ", ".join(f"[{p}](../prd/{slugify(p)}.md)" for p in prd_ids) or "—"
        cjm_cell = ", ".join(f"[{c}](../cjm/{slugify(c)}.md)" for c in cjm_ids) or "—"
        if flow_nodes:
            flow_links = " ".join(f"[`{n}`](../flow/nodes/{slugify(n)}.md)" for n in flow_nodes[:6])
            if len(flow_nodes) > 6:
                flow_links += f" +{len(flow_nodes)-6}"
        else:
            flow_links = "—"
        hig_link = f"[кандидаты](../hig/{slugify(sid)}.md)" if (DOCS_DIR/"hig"/f"{slugify(sid)}.md").exists() else "—"
        ctx_cell = f"[{len(ctx_screens)}](../ctxux/index.md#by-story-{slugify(sid)})" if ctx_screens else "—"
        lines.append(f"| [{sid}]({slugify(sid)}.md) | {title} | {prd_cell} | {cjm_cell} | {flow_links} | {hig_link} | {ctx_cell} |")
    write_file(DOCS_DIR/"stories"/"index.md", "\n".join(lines)+"\n")

def render_prd_index(artifacts: Dict[str, Any], graph: Dict[str, Any]) -> None:
    prd = artifacts.get("prd", {})
    sections = prd.get("sections", []) or prd.get("prd", []) or []
    lines: List[str] = []
    lines.append("# PRD\n")
    lines.append("| Раздел | Цели | Stories | Flow | Ссылки |")
    lines.append("|---|---|---:|---:|---|")
    for sec in sections:
        sid = sec.get("id") or sec.get("section_id")
        if not sid: continue
        goals = "; ".join((sec.get("goals") or [])[:2])
        prd_nid = f"prd:{sid}"
        stories = [n.split(":",1)[1] for n in _connected(graph, prd_nid, "story:")]
        flow_nodes = [n.split(":",2)[2] for n in _connected(graph, prd_nid, "flow:node:")]
        link = f"[страница]({slugify(str(sid))}.md)"
        lines.append(f"| {sid} | {goals or '—'} | {len(stories)} | {len(flow_nodes)} | {link} |")
    write_file(DOCS_DIR/"prd"/"index.md", "\n".join(lines)+"\n")

def render_flow_index(artifacts: Dict[str, Any], graph: Dict[str, Any]) -> None:
    flow = artifacts.get("flow", {})
    nodes = flow.get("user_flow", []) or []
    lines: List[str] = []
    lines.append("# User Flow\n")
    lines.append("| Узел | Тип | Исходящие | Аналитика | Refs |")
    lines.append("|---|---|---:|---|---|")
    for n in nodes:
        nid = n.get("id"); ntype = n.get("type", "node")
        if not nid: continue
        outc = len(n.get("edges", []) or [])
        analytics = ", ".join(n.get("analytics", []) or n.get("telemetry", []) or []) or "—"
        refs_prd = [p.split(":",1)[1] for p in _connected(graph, f"flow:node:{nid}", "prd:")]
        refs_cjm = [c.split(":",1)[1] for c in _connected(graph, f"flow:node:{nid}", "cjm:")]
        refs = []
        if refs_prd:
            refs.append("PRD: " + ", ".join(f"[{p}](../prd/{slugify(p)}.md)" for p in refs_prd))
        if refs_cjm:
            refs.append("CJM: " + ", ".join(f"[{c}](../cjm/{slugify(c)}.md)" for c in refs_cjm))
        ref_cell = "; ".join(refs) or "—"
        lines.append(f"| [{nid}]({ 'nodes/'+slugify(nid)+'.md' }) | {ntype} | {outc} | {analytics} | {ref_cell} |")
    write_file(DOCS_DIR/"flow"/"index.md", "\n".join(lines)+"\n")

def render_ctxux_index(artifacts: Dict[str, Any], graph: Dict[str, Any]) -> None:
    ctx = artifacts.get("ctxux", {})
    screens = ctx.get("screens", []) or []
    lines: List[str] = []
    lines.append("# Contextual UX\n")
    lines.append("| Экран | Local principles | Telemetry | Flow |")
    lines.append("|---|---:|---|---|")
    # Aggregate story->screens for anchors
    by_story: Dict[str, List[str]] = {}
    for s in screens:
        sid = s.get("id"); 
        if not sid: continue
        lcount = len(s.get("local_principles", []) or [])
        telemetry = ", ".join(s.get("telemetry", []) or []) or "—"
        flow_nodes = [n.split(":",2)[2] for n in _connected(graph, f"ctxux:screen:{sid}", "flow:node:")]
        flow_cell = ", ".join(f"[`{n}`](../flow/nodes/{slugify(n)}.md)" for n in flow_nodes) or "—"
        lines.append(f"| [{sid}]({slugify(sid)}.md) | {lcount} | {telemetry} | {flow_cell} |")
        # collect story links for anchor section
        for st in _connected(graph, f"ctxux:screen:{sid}", "story:"):
            story_id = st.split(":",1)[1]
            by_story.setdefault(story_id, []).append(sid)
    # Anchors by story
    if by_story:
        lines.append("\n## По сториз\n")
        for st, scrs in sorted(by_story.items()):
            lines.append(f"<a id=\"by-story-{slugify(st)}\"></a>")
            lines.append(f"### {st}")
            for sc in sorted(scrs):
                lines.append(f"- [{sc}](./{slugify(sc)}.md)")
    write_file(DOCS_DIR/"ctxux"/"index.md", "\n".join(lines)+"\n")

def render_hig_index(artifacts: Dict[str, Any], graph: Dict[str, Any]) -> None:
    hig = artifacts.get("hig", {})
    stories = hig.get("stories", []) or []
    lines: List[str] = []
    lines.append("# HIG Patterns\n")
    lines.append("| Story | Паттерны | Recommendation | Ссылки |")
    lines.append("|---|---:|---|---|")
    for s in stories:
        sid = s.get("story_id")
        if not sid: continue
        cand = s.get("candidates", []) or []
        rec = (s.get("recommendation", {}) or {}).get("pattern_id", "—")
        link = f"[страница]({slugify(sid)}.md)" if (DOCS_DIR/"hig"/f"{slugify(sid)}.md").exists() else "—"
        lines.append(f"| {sid} | {len(cand)} | {rec} | {link} |")
    write_file(DOCS_DIR/"hig"/"index.md", "\n".join(lines)+"\n")

def render_ux_index(artifacts: Dict[str, Any], graph: Dict[str, Any]) -> None:
    ux = artifacts.get("ux", {})
    principles = ux.get("principles", []) or ux.get("global_principles", []) or []
    lines: List[str] = []
    lines.append("# Global UX Principles\n")
    lines.append("| ID | Title | Examples | Ссылки |")
    lines.append("|---|---|---:|---|")
    for p in principles:
        pid = p.get("id") or p.get("principle_id")
        if not pid: continue
        title = p.get("title", "")
        ex_count = len(p.get("examples", []) or [])
        link = f"[страница]({slugify(pid)}.md)"
        lines.append(f"| {pid} | {title} | {ex_count} | {link} |")
    write_file(DOCS_DIR/"ux"/"index.md", "\n".join(lines)+"\n")


def main() -> int:
    ensure_dirs()
    env = jinja_env()
    artifacts = load_build_artifacts()
    graph = load_graph()

    render_index(env, artifacts, graph)
    render_prd(env, artifacts.get("prd", {}), graph)
    render_cjm(env, artifacts.get("cjm", {}), graph)
    render_flow(env, artifacts.get("flow", {}), graph)
    render_stories(env, artifacts.get("stories", {}), graph)
    render_ux(env, artifacts.get("ux", {}), graph)
    render_ctxux(env, artifacts.get("ctxux", {}), graph)
    render_hig(env, artifacts.get("hig", {}), graph)

    # Diagrams
    try:
        render_userflow_svg(artifacts.get("flow", {}))
    except Exception as e:
        print(f"[WARN] userflow.svg generation failed: {e}")
    try:
        render_coverage_svg(graph)
    except Exception as e:
        print(f"[WARN] coverage.svg generation failed: {e}")

    # Orphans and matrices
    try:
        render_orphans(env, graph)
        render_coverage_matrices(artifacts, graph)
    except Exception as e:
        print(f"[WARN] extras generation failed: {e}")

    # Index pages
    try:
        render_stories_index(artifacts, graph)
        render_prd_index(artifacts, graph)
        render_flow_index(artifacts, graph)
        render_ctxux_index(artifacts, graph)
        render_hig_index(artifacts, graph)
        render_ux_index(artifacts, graph)
    except Exception as e:
        print(f"[WARN] indexes generation failed: {e}")

    # mkdocs.yml
    write_mkdocs_yaml()

    print("SpecHub generation complete.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
