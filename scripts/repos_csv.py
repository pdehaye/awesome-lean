#!/usr/bin/env python3
"""Generate repos.csv: one row per GitHub repository linked from README.md.

Usage:
  python3 scripts/repos_csv.py           # rewrite repos.csv from README.md
  python3 scripts/repos_csv.py --check   # exit 1 if repos.csv is out of date

The CSV is derived from README.md only (no network access), so it is
deterministic and can be checked in CI. A repository linked from several
entries gets one row, listing every entry it appears in.
"""
import csv, io, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
OUT = ROOT / "repos.csv"

ENTRY = re.compile(r"^\s*- \[(?P<name>[^\]]+)\]\((?P<url>[^)]+)\)(?P<rest>.*)$")
SECONDARY = re.compile(r"\]\((https://github\.com/[^)\s]+)\)")
REPO = re.compile(r"https://github\.com/([^/#?)]+)/([^/#?)]+)(?:/tree/([^#?)]+))?")
FIELDS = ["repo", "url", "branch", "entry", "section", "link_role", "description", "other_entries"]


def strip_markdown(text):
    text = re.sub(r"\s*\(\[[^\]]+\]\([^)]+\)(?:,\s*\[[^\]]+\]\([^)]+\))*\)", "", text)  # "([GitHub](…))"
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)  # remaining links -> their text
    return text.replace("`", "").strip()


def collect():
    rows, section = {}, ""
    for line in README.read_text(encoding="utf-8").splitlines():
        if line.startswith("## ") or line.startswith("### "):
            heading = line.lstrip("#").strip()
            section = heading if line.startswith("## ") else f"{section.split(' > ')[0]} > {heading}"
            continue
        m = ENTRY.match(line)
        if not m or m["url"].startswith("#") or section.startswith("Contents"):
            continue
        desc = strip_markdown(m["rest"].lstrip(" -"))
        links = [(m["url"], "primary")] + [(u, "github") for u in SECONDARY.findall(m["rest"])]
        for url, role in links:
            r = REPO.match(url)
            if not r:
                continue  # not GitHub, or an organization page
            repo = f"{r.group(1)}/{r.group(2).removesuffix('.git')}"
            row = {"repo": repo, "url": f"https://github.com/{repo}",
                   "branch": r.group(3) or "", "entry": m["name"], "section": section,
                   "link_role": role, "description": desc, "other_entries": []}
            old = rows.get(repo)
            if old is None:
                rows[repo] = row
            elif old["link_role"] == "github" and role == "primary":
                # the repo's own entry takes precedence over a secondary "([GitHub](…))" link
                row["other_entries"] = old["other_entries"] + [old["entry"]]
                rows[repo] = row
            elif m["name"] != old["entry"]:
                old["other_entries"].append(m["name"])
    for row in rows.values():
        row["other_entries"] = "; ".join(dict.fromkeys(row["other_entries"]))
    return sorted(rows.values(), key=lambda r: r["repo"].lower())


def render(rows):
    buf = io.StringIO()
    w = csv.DictWriter(buf, FIELDS, lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
    return buf.getvalue()


def main():
    text = render(collect())
    if "--check" in sys.argv:
        current = OUT.read_text(encoding="utf-8") if OUT.exists() else ""
        if current != text:
            print("repos.csv is out of date: run `python3 scripts/repos_csv.py` and commit the result.")
            sys.exit(1)
        print("repos.csv is up to date.")
        return
    OUT.write_text(text, encoding="utf-8")
    print(f"Wrote {OUT.name} with {text.count(chr(10)) - 1} repositories.")


if __name__ == "__main__":
    main()
