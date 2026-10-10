# ZomboidNX

Experimental **Nintendo Switch V2 / Atmosphère feasibility project** for studying whether a legitimately owned Steam installation of Project Zomboid can ever be made compatible with Switch homebrew.

> **Status: diagnostics only.** ZomboidNX does **not** launch or include Project Zomboid, and no game port or working `.nro` has been demonstrated yet.

## What is in this repository?

- `source/main.c`: libnx console diagnostic to check Joy-Con input, a small memory allocation, and read-only SD access.
- `tools/inventory-project-zomboid.py`: Windows/Linux metadata-only scanner for your installed Steam copy.
- `tools/inventory-project-zomboid.ps1`: Windows PowerShell fallback scanner.
- `tests/`: synthetic tests; no game files required.
- `docs/feasibility.md`: technical gates and stop/go criteria.

## Step 1 — inspect the installed Steam game

**Windows (PowerShell, Python installed):**

```powershell
python .\tools\inventory-project-zomboid.py "C:\Program Files (x86)\Steam\steamapps\common\ProjectZomboid"
```

If Python is not installed:

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\inventory-project-zomboid.ps1 -GameDir "C:\Program Files (x86)\Steam\steamapps\common\ProjectZomboid"
```

**Linux:**

```bash
python3 tools/inventory-project-zomboid.py "$HOME/.local/share/Steam/steamapps/common/ProjectZomboid"
```

Replace the path with the actual location selected by Steam → Library → Project Zomboid → Manage → Browse local files. Output: `zomboid-inventory.json` in your working folder. Review it before sharing; it includes relative filenames and file sizes, binary architecture markers, and one Java classfile-header sample per JAR, **not file contents**. It does not modify the installation. Do not upload game binaries, assets, savegames, or Steam credentials.

## Step 2 — build the Switch diagnostic

Install a compatible [devkitPro](https://devkitpro.org/) environment with `switch-dev` (`devkitA64` + `libnx`), then from the repository root:

```bash
make            # produces zomboidnx.nro
```

Or, with Docker and no local toolchain:

```bash
docker run --rm -v "$PWD":/src -w /src devkitpro/devkita64 make
```

CI also builds the `.nro` on every push and uploads it as the `zomboidnx-nro` artifact.

Copy `zomboidnx.nro` to `sdmc:/switch/zomboidnx.nro`. In Atmosphère, launch hbmenu in **title override** for full application resources. Press `A` for a 16 MiB RAM allocation test, `B` to look for `sdmc:/switch/zomboidnx/game-manifest.txt`, and `+` to exit.

**Build/console status:** a standalone `Makefile` and a CI build job exist, but a successful toolchain build and testing on a physical Switch have not yet been confirmed.

## Tests

```bash
python3 -m unittest discover -s tests -v
```

## Scope and rights

This repository contains independently written diagnostic code only. **Do not commit or redistribute Project Zomboid game files, proprietary libraries, maps, or artwork.** A Steam license does not automatically permit redistributing or modifying proprietary game binaries. Any actual port or redistribution must respect the game's license and obtain permission where required.

A Switch V2 has significantly less available RAM than the game's desktop minimum, and the native graphics/runtime dependencies are not drop-in compatible. See [feasibility gates](docs/feasibility.md) for explicit go/no-go checkpoints.
