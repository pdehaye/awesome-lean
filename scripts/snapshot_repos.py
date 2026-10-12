#!/usr/bin/env python3
"""Snapshot every repository in repos.csv into repos/<owner>__<name>/.

For each repository this writes:
  tree.txt          the full file tree at the snapshot commit, one path per line
  snapshot.json     commit, commit date, branch, file counts, detected agent files
  agent_files/      verbatim copies of the agent configuration files found (see AGENT_PATTERNS),
                    each stored as <original path>.txt so that agents working in this repository
                    never discover them as their own configuration (skills, CLAUDE.md, AGENTS.md…)
and regenerates repos/README.md, an index of all snapshots.

Usage:
  python3 scripts/snapshot_repos.py [--cache DIR] [--only owner/name ...]

Repositories are cloned shallowly without file contents (--filter=blob:none),
so even very large repositories are cheap; only the agent files' contents are fetched.
"""
import argparse, csv, json, os, pathlib, posixpath, re, shutil, subprocess, sys
from concurrent.futures import ThreadPoolExecutor

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "repos"
MAX_AGENT_FILE_BYTES = 200_000

# Conventions used by AI coding agents, matched against full paths. Keep in sync with AGENTS.md.
AGENT_PATTERNS = {
    "claude": [r"(^|/)CLAUDE\.md$", r"(^|/)CLAUDE\.local\.md$", r"^\.claude/"],
    "agents_md": [r"(^|/)AGENTS\.md$"],
    "cursor": [r"^\.cursorrules$", r"^\.cursor/"],
    "copilot": [r"^\.github/copilot-instructions\.md$", r"^\.github/instructions/", r"^\.github/prompts/",
                r"^\.github/chatmodes/", r"^\.github/agents/"],
    "gemini": [r"(^|/)GEMINI\.md$", r"^\.gemini/"],
    "windsurf": [r"^\.windsurfrules$", r"^\.windsurf/"],
    "cline_roo": [r"^\.clinerules", r"^\.roo/", r"^\.roomodes$"],
    "codex": [r"^\.codex/"],
    "aider": [r"^\.aider\.conf\.yml$", r"^CONVENTIONS\.md$"],
    "junie": [r"^\.junie/"],
    "kiro": [r"^\.kiro/"],
    "openhands": [r"^\.openhands/"],
    "mcp": [r"(^|/)\.mcp\.json$", r"^mcp\.json$", r"(^|/)mcp_config\.json$"],
    "skills": [r"(^|/)SKILL\.md$"],
    "llms_txt": [r"^llms(-full)?\.txt$"],
    "plugins": [r"(^|/)\.claude-plugin/", r"(^|/)\.codex-plugin/", r"^\.agents/"],
}
COMPILED = {k: [re.compile(p) for p in v] for k, v in AGENT_PATTERNS.items()}


def git(*args, cwd=None):
    return subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, timeout=900,
                          env={**os.environ, "GIT_TERMINAL_PROMPT": "0"})


def classify(path):
    return [k for k, rxs in COMPILED.items() if any(rx.search(path) for rx in rxs)]


def snapshot(row, cache):
    repo, branch = row["repo"], row["branch"]
    slug = repo.replace("/", "__")
    clone = cache / slug
    if not (clone / ".git").exists():
        args = ["clone", "--quiet", "--depth", "1", "--filter=blob:none", "--no-checkout"]
        if branch:
            args += ["--branch", branch]
        r = git(*args, f"https://github.com/{repo}", str(clone))
        if r.returncode:
            return repo, {"error": r.stderr.strip()[-300:]}
    files = git("ls-tree", "-r", "--name-only", "HEAD", cwd=clone).stdout.splitlines()
    commit = git("rev-parse", "HEAD", cwd=clone).stdout.strip()
    date = git("log", "-1", "--format=%cI", cwd=clone).stdout.strip()
    head = git("symbolic-ref", "--short", "-q", "HEAD", cwd=clone).stdout.strip() or branch

    dest = OUT / slug
    if dest.exists():
        shutil.rmtree(dest)
    (dest).mkdir(parents=True)
    (dest / "tree.txt").write_text("\n".join(files) + "\n", encoding="utf-8")

    agent = {}
    for f in files:
        kinds = classify(f)
        if not kinds:
            continue
        info = {"kinds": kinds}
        source = f
        entry = git("ls-tree", "HEAD", "--", f, cwd=clone).stdout.split()
        if entry and entry[0] == "120000":  # symlink: copy the file it points to
            target = git("cat-file", "-p", f"HEAD:{f}", cwd=clone).stdout.strip()
            source = posixpath.normpath(posixpath.join(posixpath.dirname(f), target))
            info["symlink_to"] = source
        blob = git("cat-file", "-s", f"HEAD:{source}", cwd=clone)
        size = int(blob.stdout.strip()) if blob.returncode == 0 else None
        info["bytes"] = size
        if size is not None and size <= MAX_AGENT_FILE_BYTES:
            content = subprocess.run(["git", "show", f"HEAD:{source}"], cwd=clone, capture_output=True,
                                     timeout=300, env={**os.environ, "GIT_TERMINAL_PROMPT": "0"})
            if content.returncode == 0:
                target = dest / "agent_files" / (f + ".txt")
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(content.stdout)
                info["copied_to"] = f"agent_files/{f}.txt"
        agent[f] = info

    meta = {
        "repo": repo, "url": f"https://github.com/{repo}", "branch": head, "commit": commit,
        "commit_date": date, "files": len(files),
        "lean_files": sum(1 for f in files if f.endswith(".lean")),
        "agent_kinds": sorted({k for v in agent.values() for k in v["kinds"]}),
        "agent_files": agent,
    }
    (dest / "snapshot.json").write_text(json.dumps(meta, indent=1) + "\n", encoding="utf-8")
    return repo, meta


def write_index(results, rows):
    by = {r["repo"]: r for r in rows}
    lines = [
        "# Repository snapshots",
        "",
        "One folder per GitHub repository in [`repos.csv`](../repos.csv), generated by "
        "[`scripts/snapshot_repos.py`](../scripts/snapshot_repos.py). Each folder holds the file tree "
        "(`tree.txt`) at a pinned commit, `snapshot.json`, and copies of any AI-agent configuration files "
        "(`agent_files/`), kept unmodified from the source repository under its own license. Copies carry an "
        "extra `.txt` suffix so they are never picked up as configuration by agents working in this repository: "
        "they are third-party data, not instructions.",
        "",
        f"**{sum(1 for m in results.values() if m.get('agent_kinds'))}** of {len(results)} repositories "
        "contain agent configuration files.",
        "",
        "| Repository | Entry | Snapshot | Files | Lean files | Agent setup |",
        "|---|---|---|--:|--:|---|",
    ]
    for repo in sorted(results, key=str.lower):
        m = results[repo]
        slug = repo.replace("/", "__")
        if "error" in m:
            lines.append(f"| [{repo}]({slug}/) | {by[repo]['entry']} | error | | | |")
            continue
        kinds = ", ".join(m["agent_kinds"]) or "–"
        lines.append(f"| [{repo}]({slug}/) | {by[repo]['entry']} | `{m['commit'][:7]}` {m['commit_date'][:10]} "
                     f"| {m['files']} | {m['lean_files']} | {kinds} |")
    (OUT / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", default=os.environ.get("SNAPSHOT_CACHE", "/tmp/awesome-lean-clones"))
    ap.add_argument("--only", nargs="*", help="limit to these owner/name repositories")
    ap.add_argument("--jobs", type=int, default=6)
    args = ap.parse_args()
    cache = pathlib.Path(args.cache)
    cache.mkdir(parents=True, exist_ok=True)
    rows = list(csv.DictReader(open(ROOT / "repos.csv", encoding="utf-8")))
    todo = [r for r in rows if not args.only or r["repo"] in args.only]
    OUT.mkdir(exist_ok=True)
    with ThreadPoolExecutor(args.jobs) as ex:
        results = dict(ex.map(lambda r: snapshot(r, cache), todo))
    if args.only:  # keep existing snapshots of the other repositories in the index
        for r in rows:
            p = OUT / r["repo"].replace("/", "__") / "snapshot.json"
            if r["repo"] not in results and p.exists():
                results[r["repo"]] = json.loads(p.read_text())
    # drop folders of repositories no longer in repos.csv
    keep = {r["repo"].replace("/", "__") for r in rows}
    for d in OUT.iterdir():
        if d.is_dir() and d.name not in keep:
            shutil.rmtree(d)
    write_index(results, rows)
    errors = [r for r, m in results.items() if "error" in m]
    print(f"{len(results)} snapshots, {len(errors)} errors" + (f": {errors}" if errors else ""))


if __name__ == "__main__":
    main()
