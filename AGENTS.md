# Instructions for AI agents

This repository is an [awesome list](https://awesome.re) of Lean resources. `README.md` is the list itself; everything else supports it.

## Keep `repos.csv` in sync with the README

`repos.csv` lists every GitHub repository linked from `README.md`, one row per repository. It is **generated**: never edit it by hand.

**After any change to `README.md`**, regenerate it and commit both files together:

```sh
python3 scripts/repos_csv.py          # rewrite repos.csv
python3 scripts/repos_csv.py --check  # verify it is up to date (CI runs this)
```

Columns:

| Column | Meaning |
|---|---|
| `repo` | `owner/name` on GitHub |
| `url` | `https://github.com/owner/name` |
| `branch` | Branch named in the link (`…/tree/<branch>`), empty otherwise |
| `entry` | Name of the list entry the repository belongs to |
| `section` | README section, with subsections written as `Section > Subsection` |
| `link_role` | `primary` if it is the entry's main link, `github` if it comes from a `([GitHub](…))` link next to it |
| `description` | The entry's description, with Markdown removed |
| `other_entries` | Other entries that also link to the repository, separated by `; ` |

Rows are sorted by `repo`. Organization links (e.g. `https://github.com/leanprover`) and non-GitHub links are not included. If a repository appears in several entries, the entry whose main link it is wins; the others go in `other_entries`.

If you change how the CSV is built, change `scripts/repos_csv.py` (not the CSV), update the column table above, and regenerate.

## Editing the list

Follow [`contributing.md`](contributing.md). In short:

- **Entry format:** `- [Name](link) - Description.`, with the description starting with a capital letter and ending with a period. Extra links go in parentheses at the end, e.g. `([GitHub](https://github.com/owner/repo))`.
- **Verify every link before adding it.** Check that GitHub repositories exist (`git ls-remote https://github.com/owner/repo` works even where github.com web pages are blocked) and that web pages load. Base descriptions on the project's own README or site, not on memory.
- **No duplicates:** search the README first. `awesome-lint` rejects a URL that appears twice as a main link.
- **Run the checks before committing:**

  ```sh
  npx awesome-lint
  python3 scripts/repos_csv.py --check
  ```

## The `analysis/` folder

`analysis/` holds a study of how the listed repositories use Lean (see `analysis/README.md`). It isn't regenerated automatically and doesn't need to change when the list changes. Its scripts have their own instructions there.
