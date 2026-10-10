# Resultados executáveis — 2026-10-09

## O que foi executado REALMENTE
- git clone https://github.com/lloupp/ZomboidNX ✓
- python3 -m unittest discover -s tests -v → 2 OK ✓
- source/main.c inspecionado (libnx diagnostic) ✓
- docs/feasibility.md analisado ✓
- docs/evidence-report-2026-10-09.md criado (evidência real) ✓
- Commit local + branch feasibility-2026-10-09 + PR #1 (draft, NÃO merge automático) ✓
- PoC: poc/java-runtime-analysis.md (independente, sem arquivos proprietários) ✓

## O que NÃO foi feito (documentado com motivo)
- .nro NÃO compilado: devkitPro / libnx NÃO instalado no PC
- Inventário de Project Zomboid NÃO executado: NÃO há Steam/Zomboid no PC
- Teste em Switch físico NÃO feito: não há hardware disponível
- Nenhum arquivo do jogo foi modificado, extraído ou distribuído ✓

## PR criada (sem auto-merge)
https://github.com/lloupp/ZomboidNX/pull/1
Status: draft. Não foi feito merge.

## Próximos bloqueios técnicos (evidência)
1. Instalar devkitPro (devkitA64, libnx) para compilar .nro
2. Obter instalação legítima do jogo localmente para escanear arquitetura real
3. Testar .nro em Switch V2 com Atmosphère (hbmenu, title override)
4. Resolver arquitetura x86_64 → ARM64 (não automático)
5. Resolver runtime Java/LWJGL → Switch Horizon ABI (não drop-in)
6. Resolver memória (desktop ~8 GiB vs Switch ~4 GiB compartilhado)
