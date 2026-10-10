# Bloqueios reais — ambiente remoto (Inspiron-3477-AIO)

Ambiente: Linux x86_64 Ubuntu 24.04 (remoto). NÃO é PC físico do Eduardo.

1. Steam/Project Zomboid: NÃO encontrado em nenhuma unidade/local (find interrompido, ZERO resultados).
2. devkitPro: NÃO instalado; script de instalação falhou (Cloudflare bloqueou download).
3. .nro: NÃO pode ser compilado sem toolchain ARM64 (devkitA64 + libnx).
4. PR #1 aberta (draft, sem merge): https://github.com/lloupp/ZomboidNX/pull/1

Comandos para executar NO PC CORRETO (local):

# 1. Instalar devkitPro
curl -sL https://pkg.devkitpro.org/get-devkitpro-pacman.sh | bash
sudo dkp-pacman -S switch-dev devkitA64 libnx switch-examples

# 2. Verificar Steam real
python3 tools/inventory-project-zomboid.py "/caminho/real/do/ProjectZomboid"
# OU PowerShell no Windows

# 3. Compilar .nro (após devkitPro instalado)
cp -R $(dkp-pacman -Ql switch-examples | grep templates) ./build
cp source/main.c ./build/source/
cd build && make

# 4. Copiar para Switch
cp build/zomboidnx.nro sdmc:/switch/zomboidnx.nro
