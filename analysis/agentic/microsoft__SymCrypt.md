# microsoft/SymCrypt: agent setup

- **Snapshot:** commit `c2e575a` (2026-07-12), branch `feature/verifiedcrypto`, from `repos/microsoft__SymCrypt/snapshot.json`.
- **Tools targeted:** `AGENTS.md` readers (Codex and others) and GitHub Copilot (`.github/copilot-instructions.md`, which only points to `AGENTS.md`).
- **Files:**
  - `AGENTS.md` (~24 KB): repo overview, build, tests, C style, threat model, FIPS rules, versioning, PR workflow.
  - `.github/copilot-instructions.md`: "All agent instructions live in /AGENTS.md".
- **What agents are asked to do:** C, assembly and C++ test changes to the crypto library, bug triage and code review "grounded in SymCrypt's specific threat model", and changelog entries. Lean is never mentioned. The Lean code on this branch lives under `SymCRust/lean/` (per `tree.txt`), and `AGENTS.md` only calls `SymCRust` an "Experimental new Rust implementation".
- **Build and verification:** CMake presets (`cmake --preset Linux_AMD64_GCC_Debug`, `cmake --build --preset …`) or `python3 scripts/build.py cmake <build_dir>`. Run `symcryptunittest` directly, using `+<alg. prefix>` to test only the changed algorithm. "Generally you should run the tests in Debug mode for your host CPU." Agents should "do native builds unless explicitly instructed otherwise". Nothing is said about `lake` or Lean proofs.
- **Proof policy:** none stated. The closest rules are about tests: "**Never skip or weaken self-tests**" (FIPS).
- **Lean and Mathlib guidance:** none stated.
- **Skills, commands, hooks, MCP:** none. Deep Wiki via MCP is mentioned as optional, "only … a starting point", and anything it says must be confirmed.
- **Permissions and safety:** a "Things You Must NEVER Do" list:
  - timing side channels ("the #1 rule");
  - ABI breaks;
  - editing generated `.asm`/`.S`;
  - `memcmp` on secrets;
  - undefined behavior.

  Agents must "**NEVER** push changes to GitHub" (to prevent premature disclosure of confidential fixes) and must not modify the version "unless asked to".
- **Human oversight:** humans handle branch management, publishing and versioning. For "any MSRC case or CVE, always ask the human contributor" which branch to use. All CI checks must pass, and changes to public headers need an ABI impact assessment. The file ends with a PR checklist.
- **Notable ideas:**
  - Put the threat model in the agent file, so triage and reviews follow it.
  - Point the Copilot file at `AGENTS.md` so there is a single source of truth.
  - Give an explicit list of what only humans may do (push, versioning, confidential branches).
- **Lean-specificity:** low. The instructions cover only the C library, with nothing on the Lean-verified code on this branch.
- **Evidence:** `agent_files/AGENTS.md`, `agent_files/.github/copilot-instructions.md`; `tree.txt` for `SymCRust/lean/`.
