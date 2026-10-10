# ZomboidNX Evidence Report — 2026-10-09

## Environment (verified)
- OS: Linux 7.0.0-38-generic x86_64 (Ubuntu 24.04)
- Java: OpenJDK 17.0.20.1 (available, but Switch homebrew does not run desktop JVMs directly)
- Steam/ProjectZomboid: NOT FOUND on this PC (no ~/Steam, ~/.steam, or /home/eduardodlima/.local/share/Steam)
- devkitPro / libnx: NOT INSTALLED; no `dkp-pacman`, no `devkitA64`, no cross-compiler for ARM64
- Git repo: https://github.com/lloupp/ZomboidNX cloned successfully; master branch

## Tests executed (real)
- `python3 -m unittest discover -s tests -v` → 2 passed (synthetic inventory tests)
- `python3 tools/inventory-project-zomboid.py` → fails correctly when no Steam dir given; no proprietary files accessed or modified
- Source `main.c` inspected: independent libnx diagnostic (Joy-Con A/B/+, 16 MiB RAM test, read-only SD manifest check). Not a game port.

## Feasibility assessment per docs/feasibility.md (honest no-go gates)
- Gate 0 (hardware diagnostic): Code present; CANNOT BUILD `.nro` without devkitPro installed.
- Gate 1 (game inventory): CANNOT EXECUTE without installed legitimate Steam copy; scanner code exists and is safe.
- Gate 2 (Java/JNI): Build 41 uses LWJGL + desktop OpenGL + native x86_64 libraries. Switch uses ARM64 Horizon ABI. No drop-in JVM available; must be independently authored.
- Gate 3 (graphics/audio/resource): Desktop minimum ~8 GiB RAM; Switch V2 ~4 GiB shared system RAM, far less for homebrew; no LWJGL ARM64 build exists.
- Gate 4 (rights): No proprietary binaries, JARs, assets, or Steam credentials committed.

## Build 41 / native port blockers (evidence-based)
- Architecture mismatch: PE/x86_64 or ELF/Amd64 vs ARM64 (AArch64)
- Graphics runtime: LWJGL desktop OpenGL does not map to Switch GPU (NVN / OpenGL ES 2.0 via libnx) automatically
- Audio: desktop OpenAL vs Switch audio service (Audren/Audout) — different APIs
- Memory: 16 MiB test in main.c is far below game requirements; actual heap would fail
- Java runtime: no certified JVM for Switch homebrew; must port/rewrite runtime independently

## Proofs of concept created / possible
1. Synthetic inventory scanner (passed tests)
2. Memory allocation test code (`main.c`) — demonstrates libnx API usage
3. Read-only SD manifest check (`main.c`) — safe, non-destructive
4. Report and documentation commits — real artifacts

## Limitations (transparent)
- No `.nro` compiled (missing devkitPro)
- No Project Zomboid installation found locally → no real architecture audit of game binaries
- No physical Switch V2 with Atmosphère available in this environment
- No proprietary files distributed or modified
- No claim of compatibility made

## Next steps (blocked by prerequisites)
1. Install devkitPro with `switch-dev`, `devkitA64`, `libnx` to compile `.nro`
2. Obtain legitimate Steam installation of Project Zomboid locally to run scanner
3. Physically test `.nro` on unlocked Switch V2 via hbmenu title override
4. Only after independent runtime proof should any port claim proceed

## Commit / PR evidence
- Git commits created locally; branch maintained on clone
- PR not automatically merged; manual review required by repo owner before opening PR
