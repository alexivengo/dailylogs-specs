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

# Third-party
from jinja2 import Environment, FileSystemLoader, select_autoescape
import pydot

# Optional import: markdownify for rich text fallbacks
try:
    from markdownify import markdownify as md
except Exception:
    def md(s: str) -> str:
        return s

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
    return env


# ---------- Rendering helpers ----------

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
    )
    write_file(DOCS_DIR / "index.md", content)


def render_prd(env: Environment, prd: Dict[str, Any], graph: Dict[str, Any]) -> None:
    if not prd:
        return
    tmpl = env.get_template("prd_section.md.j2")
    prd_version = prd.get("version")
    for section in prd.get("sections", []):
        sec_id = section.get("id") or section.get("section_id") or "unknown"
        path = DOCS_DIR / "prd" / f"{slugify(str(sec_id))}.md"
        edit_href = edit_link(f"specs/00_prd/sections/{sec_id}.json")
        content = tmpl.render(section=section, edit_href=edit_href, version=prd_version)
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
        content = tmpl.render(stage=stage, edit_href=edit_href, version=cjm_version)
        write_file(path, content)


def render_flow(env: Environment, flow: Dict[str, Any], graph: Dict[str, Any]) -> None:
    if not flow:
        return
    # Overview page placeholder
    overview = "# User Flow\n\n![User Flow](../_media/userflow.svg)\n"
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
        content = tmpl.render(node=node, edit_href=edit_href, version=flow_version)
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
        content = tmpl.render(story=story, edit_href=edit_href, version=us_version)
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
        content = tmpl.render(principle=principle, edit_href=edit_href, version=ux_version)
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
        content = tmpl.render(screen=screen, edit_href=edit_href, version=ctxux_version)
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
        content = tmpl.render(hig_story=story, edit_href=edit_href, version=hig_version)
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
        url = f"./flow/nodes/{slugify(nid)}/"
        shape = {
            "screen": "box",
            "system": "ellipse",
            "decision": "diamond",
            "error": "octagon",
            "terminator": "oval",
        }.get(ntype, "box")
        graph.add_node(pydot.Node(nid, label=label, shape=shape, URL=url, target="_self"))
    # Add edges
    node_index = {n.get("id"): n for n in flow.get("user_flow", [])}
    for n in flow.get("user_flow", []):
        src = n.get("id")
        for e in n.get("edges", []) or []:
            tgt = e.get("target")
            if not tgt:
                continue
            elabel = e.get("action") or e.get("id") or ""
            graph.add_edge(pydot.Edge(src, tgt, label=elabel))
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
            return f"prd/{nid.split(':', 1)[1]}.md"
        if t == "CJM" and nid.startswith("cjm:"):
            return f"cjm/{nid.split(':', 1)[1]}.md"
        if t == "FLOW_NODE" and nid.startswith("flow:node:"):
            return f"flow/nodes/{slugify(nid.split(':', 2)[2])}.md"
        if t == "STORY" and nid.startswith("story:"):
            return f"stories/{nid.split(':', 1)[1]}.md"
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
            sg.add_node(pydot.Node(safe_id(nid), label=label, URL=node_url_for_coverage(n)))
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
                url = "#"
                if ntype == "STORY":
                    url = f"stories/{nid.split(':',1)[1]}.md"
                elif ntype == "CTXUX":
                    url = f"ctxux/{nid.split(':',2)[2]}.md"
                elif ntype == "FLOW":
                    url = f"flow/nodes/{slugify(nid.split(':',2)[2])}.md"
                elif ntype == "PRD":
                    url = f"prd/{nid.split(':',1)[1]}.md"
                elif ntype == "CJM":
                    url = f"cjm/{nid.split(':',1)[1]}.md"
                lines.append(f"- [{nid}]({url})")
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
            for f in cov:
                name = os.path.splitext(f)[0]
                lines.append(f"      - {name}: coverage/{f}")

    def section(title: str, rel: str, dir_path: Path):
        files = list_md(dir_path)
        if not files:
            return
        lines.append(f"  - {title}:")
        for fname in files:
            name = os.path.splitext(fname)[0]
            lines.append(f"      - {name}: {rel}/{fname}")

    section("PRD", "prd", DOCS_DIR / "prd")
    section("CJM", "cjm", DOCS_DIR / "cjm")
    # Flow overview first
    if (DOCS_DIR / "flow" / "overview.md").exists():
        lines.append("  - User Flow:")
        lines.append("      - Overview: flow/overview.md")
        for fname in list_md(DOCS_DIR / "flow" / "nodes"):
            name = os.path.splitext(fname)[0]
            lines.append(f"      - {name}: flow/nodes/{fname}")
    section("User Stories", "stories", DOCS_DIR / "stories")
    section("Global UX Principles", "ux", DOCS_DIR / "ux")
    section("Contextual UX", "ctxux", DOCS_DIR / "ctxux")
    section("HIG Patterns", "hig", DOCS_DIR / "hig")

    return "\n".join(lines) + "\n"


def write_mkdocs_yaml() -> None:
    mkdocs_path = ROOT / "mkdocs.yml"
    base = f"""
site_name: SpecHub
site_description: Specification Hub
theme:
  name: material
  language: en
  features:
    - navigation.instant
    - navigation.tracking
    - content.code.copy
    - search.suggest
  palette:
    - scheme: default
      primary: indigo
      accent: indigo
plugins:
  - search
markdown_extensions:
  - admonition
  - toc:
      permalink: true
extra:
  generator: spechub
# We add custom 'Edit source' links inside pages instead of using edit_uri
{build_nav()}""".lstrip()
    write_file(mkdocs_path, base)


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

    # mkdocs.yml
    write_mkdocs_yaml()

    print("SpecHub generation complete.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
