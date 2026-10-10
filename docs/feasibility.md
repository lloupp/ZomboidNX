# Technical feasibility and evidence gates

**Target:** Nintendo Switch V2 (Mariko) with Atmosphère, native Horizon OS homebrew (\`.nro\`). Each gate must be demonstrated rather than assumed.

## Gate 0 — hardware diagnostic

Compile the independent libnx test application with devkitPro. Launch it through hbmenu title override. Verify Joy-Con A/B/+ input, 16 MiB allocation, and optional read-only SD access.

**Status:** code written; `.nro` cross-compiled successfully in CI (devkitpro/devkita64, no warnings). Physical hardware validation **not done**.

## Gate 1 — installed game inventory

Run the metadata-only scanner against the user's legitimately installed Project Zomboid Steam version on Windows or Linux. Determine installed build, Java runtime/classfile versions, native binary architecture and graphics/audio dependencies. Do not upload any proprietary game binary or asset.

**Status:** scanners written; real Steam installation **not scanned**.

## Gate 2 — Java/JNI feasibility

Prototype a legal, independently authored Java test app on the target runtime. Check required Java bytecode compatibility, threads, JNI, file I/O and garbage collection. A toy Java-on-Switch proof of concept does **not** mean LWJGL-based Project Zomboid can run. Linux x86-64 libraries do not run on Switch's ARM64 Horizon ABI.

**Status:** not started.

## Gate 3 — graphics, audio and resource budget

Examine OpenGL/LWJGL rendering, audio, memory use, asset footprint and file loading. Test a minimal legal graphics workload and measure actual heap, frame rate, load times and stability on physical Switch V2. The Switch's ~4 GiB shared system memory is far below the game's desktop 8 GiB minimum and cannot all be assigned to a homebrew application.

**Status:** not started.

## Gate 4 — rights and distribution

No proprietary code, JARs, assets, maps or audio may be committed here. Respect the game license and obtain permission where necessary for modifications and distribution. Keep experiments, tooling and any eventual redistributable code independently authored.

**Status:** continuous requirement.

## Go/no-go principles

- No native port claim without real game code booting legally and reliably.
- No feasibility claim from a menu mock-up or unrelated Java sample.
- Stop the direct-port approach if the necessary runtime or proprietary engine access is unavailable.
- Streaming from a PC is a separate fallback, **not** a Switch port.
