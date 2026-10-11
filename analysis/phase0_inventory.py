"""Phase 0: inventory every GitHub repository linked from README.md.

Output: analysis/inventory.json (one record per unique repo) with the README
entry/section it comes from, whether it is the entry's primary link, and
Reservoir metadata when the repo is a registered Lean package.
"""
import json, re, sys, urllib.request, concurrent.futures as cf, pathlib

ROOT = pathlib.Path(__file__).resolve().parent
README = ROOT.parent / "README.md"
ENTRY = re.compile(r"^\s*- \[(?P<name>[^\]]+)\]\((?P<url>[^)]+)\)(?P<rest>.*)$")
LINK = re.compile(r"\]\((https://github\.com/[^)\s]+)\)")

def repo_of(url):
    m = re.match(r"https://github\.com/([^/]+)/([^/#?]+)(?:/tree/([^#?]+))?", url)
    if not m:
        return None, None
    return f"{m.group(1)}/{m.group(2).removesuffix('.git')}", m.group(3)

def reservoir(full):
    try:
        with urllib.request.urlopen(f"https://reservoir.lean-lang.org/index/{full}/metadata.json", timeout=20) as r:
            d = json.load(r)
        return {k: d.get(k) for k in ("description", "keywords", "homepage", "license", "createdAt", "updatedAt", "stars")}
    except Exception:
        return None

def main():
    section, repos = None, {}
    for line in README.read_text().splitlines():
        if line.startswith("## ") or line.startswith("### "):
            section = line.lstrip("# ").strip()
            continue
        m = ENTRY.match(line)
        if not m or m["url"].startswith("#"):
            continue
        desc = m["rest"].lstrip(" -").strip()
        for i, url in enumerate([m["url"]] + LINK.findall(m["rest"])):
            full, branch = repo_of(url)
            if not full:
                continue          # not GitHub, or an organization page
            rec = repos.setdefault(full, {"repo": full, "branch": branch, "entries": []})
            rec["entries"].append({"name": m["name"], "section": section,
                                   "primary": i == 0, "description": desc})
    with cf.ThreadPoolExecutor(12) as ex:
        for rec, meta in zip(repos.values(), ex.map(reservoir, repos)):
            rec["reservoir"] = meta
    out = sorted(repos.values(), key=lambda r: r["repo"].lower())
    (ROOT / "inventory.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
    print(f"{len(out)} repos, {sum(1 for r in out if r['reservoir'])} on Reservoir")

if __name__ == "__main__":
    main()
