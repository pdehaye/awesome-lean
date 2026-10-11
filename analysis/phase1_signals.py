"""Phase 1: automated signals for every repo in inventory.json.

Each repo is cloned shallowly with a sparse checkout restricted to Lean
sources and build files, so huge repos (mathlib4, lean4, SymCrypt) stay small.
Signals are counted on comment-stripped Lean code and written to
analysis/signals.json and analysis/signals.csv.

Usage: python3 -I phase1_signals.py <clone-dir>
"""
import collections, csv, json, os, pathlib, re, subprocess, sys
import concurrent.futures as cf

ROOT = pathlib.Path(__file__).resolve().parent
CLONES = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "clones")
SPARSE = ["*.lean", "/lakefile.lean", "/lakefile.toml", "/lake-manifest.json", "/lean-toolchain"]
SKIP_DIRS = (".lake/", "lake-packages/")

MODIFIERS = r"(?:(?:@\[[^\]]*\]\s*)*(?:private|protected|public|noncomputable|partial|unsafe|nonrec|scoped|local)\s+)*"
DECL = re.compile(r"^\s*(?:@\[[^\]]*\]\s*)*" + MODIFIERS +
                  r"(theorem|lemma|def|abbrev|instance|structure|class|inductive|axiom|opaque|example)\b", re.M)
COUNTERS = {
    # proof hygiene
    "sorry": r"\bsorry\b", "admit": r"\badmit\b",
    "decide": r"\bdecide\b", "native_decide": r"\bnative_decide\b",
    # language extension / metaprogramming
    "syntax": r"^\s*(?:@\[[^\]]*\]\s*)*(?:scoped |local )?syntax\b",
    "macro": r"^\s*(?:@\[[^\]]*\]\s*)*(?:scoped |local )?macro(?:_rules)?\b",
    "elab": r"^\s*(?:@\[[^\]]*\]\s*)*(?:scoped |local )?elab(?:_rules)?\b",
    "syntax_cat": r"\bdeclare_syntax_cat\b",
    "notation": r"^\s*(?:scoped |local )?(?:notation|infixl?|infixr|prefix|postfix)\b",
    "meta_monads": r"\b(?:MetaM|TacticM|TermElabM|CommandElabM|CoreM)\b",
    # programming
    "main_def": r"^\s*(?:unsafe\s+)?def\s+main\b",
    "io": r"\bIO\b",
    "extern": r"@\[\s*extern\b", "export": r"@\[\s*export\b",
    "partial_def": r"\bpartial\s+def\b",
    # evaluation, tests, interactivity
    "eval": r"^\s*#eval\b", "guard": r"^\s*#guard(?:_msgs)?\b",
    "plausible": r"\bplausible\b",
    "widget": r"@\[\s*widget|\bProofWidgets\b|\bWidget\.",
}
COUNTERS = {k: re.compile(v, re.M) for k, v in COUNTERS.items()}
IMPORT = re.compile(r"^import\s+([\w.]+)", re.M)

def strip_comments(src):
    out, i, depth, n = [], 0, 0, len(src)
    while i < n:
        if src.startswith("/-", i):
            depth += 1; i += 2; continue
        if depth and src.startswith("-/", i):
            depth -= 1; i += 2; continue
        if depth:
            i += 1; continue
        if src.startswith("--", i):
            j = src.find("\n", i); i = n if j < 0 else j; continue
        if src[i] == '"':                       # skip string literals
            j = i + 1
            while j < n and src[j] != '"':
                j += 2 if src[j] == "\\" else 1
            out.append(src[i:j + 1]); i = j + 1; continue
        out.append(src[i]); i += 1
    return "".join(out)

def git(*args, cwd=None):
    return subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True,
                          env={**os.environ, "GIT_TERMINAL_PROMPT": "0"}, timeout=900)

def fetch(rec):
    dest = CLONES / rec["repo"].replace("/", "__")
    if (dest / ".git").exists():
        return dest, None
    args = ["clone", "--depth", "1", "--filter=blob:none", "--no-checkout", "--quiet"]
    if rec.get("branch"):
        args += ["--branch", rec["branch"]]
    r = git(*args, f"https://github.com/{rec['repo']}", str(dest))
    if r.returncode:
        return None, r.stderr.strip()[-200:]
    git("sparse-checkout", "set", "--no-cone", *SPARSE, cwd=dest)
    r = git("checkout", "--quiet", cwd=dest)
    return (dest, None) if r.returncode == 0 else (None, r.stderr.strip()[-200:])

def lakefile_info(dest):
    info = {"lean_exe": 0, "lean_lib": 0, "requires": []}
    for name in ("lakefile.lean", "lakefile.toml"):
        p = dest / name
        if p.exists():
            t = p.read_text(errors="ignore")
            info["lean_exe"] += len(re.findall(r"^\s*(?:@\[[^\]]*\]\s*)?lean_exe\b|^\s*\[\[lean_exe\]\]", t, re.M))
            info["lean_lib"] += len(re.findall(r"^\s*(?:@\[[^\]]*\]\s*)?lean_lib\b|^\s*\[\[lean_lib\]\]", t, re.M))
    p = dest / "lake-manifest.json"
    if p.exists():
        try:
            info["requires"] = sorted(pk.get("name", "?") for pk in json.loads(p.read_text()).get("packages", []))
        except ValueError:
            pass
    return info

def analyze(rec):
    dest, err = fetch(rec)
    row = {"repo": rec["repo"], "error": err}
    if not dest:
        return row
    files = git("ls-tree", "-r", "--name-only", "HEAD", cwd=dest).stdout.split()
    exts = collections.Counter(pathlib.PurePath(f).suffix.lower() or "(none)" for f in files
                               if not f.startswith(SKIP_DIRS))
    row["files_total"] = sum(exts.values())
    row["top_exts"] = ", ".join(f"{e}:{c}" for e, c in exts.most_common(5))
    decls, counts, imports, loc, nlean = collections.Counter(), collections.Counter(), collections.Counter(), 0, 0
    for f in dest.rglob("*.lean"):
        rel = f.relative_to(dest).as_posix()
        if rel.startswith(SKIP_DIRS):
            continue
        nlean += 1
        code = strip_comments(f.read_text(errors="ignore"))
        loc += sum(1 for l in code.splitlines() if l.strip())
        decls.update(m.group(1) for m in DECL.finditer(code))
        for k, rx in COUNTERS.items():
            counts[k] += len(rx.findall(code))
        imports.update(i.split(".")[0] for i in IMPORT.findall(code))
    row.update(lean_files=nlean, lean_loc=loc,
               lean_file_share=round(nlean / max(1, row["files_total"]), 3))
    row.update({f"d_{k}": decls[k] for k in ("theorem", "lemma", "def", "abbrev", "instance",
                                              "structure", "class", "inductive", "axiom", "opaque", "example")})
    row.update(counts)
    row["imports_top"] = ", ".join(f"{m}:{c}" for m, c in imports.most_common(6))
    row.update(lakefile_info(dest))
    row["requires"] = " ".join(row["requires"])
    tc = dest / "lean-toolchain"
    row["toolchain"] = tc.read_text().strip().split(":")[-1] if tc.exists() else ""
    return row

def derive(r):
    if r.get("error") or not r.get("lean_loc"):
        return r
    kloc = r["lean_loc"] / 1000
    proofs = r["d_theorem"] + r["d_lemma"]
    defs = sum(r[f"d_{k}"] for k in ("def", "abbrev", "instance", "structure", "class", "inductive", "opaque"))
    meta = r["syntax"] + r["macro"] + r["elab"] + r["syntax_cat"] + r["meta_monads"]
    r["proof_ratio"] = round(proofs / max(1, proofs + defs), 2)
    r["meta_per_kloc"] = round(meta / kloc, 1)
    r["io_per_kloc"] = round((r["io"] + 20 * r["main_def"] + 5 * r["extern"]) / kloc, 1)
    r["eval_per_kloc"] = round((r["eval"] + r["guard"]) / kloc, 1)
    r["sorry_per_kloc"] = round(r["sorry"] / kloc, 2)
    r["roles_guess"] = guess(r)
    return r

def guess(r):
    """Heuristic first-pass roles; calibrated by hand on a sample before use."""
    roles = []
    if r["lean_file_share"] < 0.2 and r["lean_loc"] < 5000:
        roles.append("tool-around-Lean")
    if r["proof_ratio"] >= 0.45:
        roles.append("certifier")
    elif r["proof_ratio"] >= 0.2:
        roles.append("spec+proof")
    if r["meta_per_kloc"] >= 8:
        roles.append("DSL/metaprogramming")
    if r["lean_exe"] or r["main_def"] or r["io_per_kloc"] >= 5:
        roles.append("program")
    if r["eval_per_kloc"] >= 5:
        roles.append("computation/examples")
    if r["widget"]:
        roles.append("interactive")
    if not roles:
        roles.append("definitions/library")
    return " + ".join(roles)

def main():
    CLONES.mkdir(parents=True, exist_ok=True)
    inv = json.loads((ROOT / "inventory.json").read_text())
    with cf.ThreadPoolExecutor(6) as ex:
        rows = [derive(r) for r in ex.map(analyze, inv)]
    by = {r["repo"]: r for r in rows}
    for rec in inv:
        e = rec["entries"][0]
        by[rec["repo"]].update(entry=e["name"], section=e["section"],
                               on_reservoir=bool(rec["reservoir"]),
                               stars=(rec["reservoir"] or {}).get("stars"))
    (ROOT / "signals.json").write_text(json.dumps(rows, indent=1))
    keys = list(dict.fromkeys(k for r in rows for k in r))
    with open(ROOT / "signals.csv", "w", newline="") as f:
        w = csv.DictWriter(f, keys); w.writeheader(); w.writerows(rows)
    print(f"{len(rows)} repos analyzed, {sum(1 for r in rows if r.get('error'))} errors")

if __name__ == "__main__":
    main()
