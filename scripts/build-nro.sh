#!/usr/bin/env bash
# Build the independently-authored ZomboidNX diagnostic NRO.
# Requires devkitPro switch-dev in DEVKITPRO, or the official devkitPro Docker image.
set -euo pipefail

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
: "${DEVKITPRO:?Set DEVKITPRO (usually /opt/devkitpro) or run inside devkitpro/devkita64.}"

TEMPLATE="${DEVKITPRO}/examples/switch/templates/application"
if [[ ! -f "${TEMPLATE}/Makefile" ]]; then
  TEMPLATE="${ROOT}/_switch-examples/templates/application"
fi
if [[ ! -f "${TEMPLATE}/Makefile" ]]; then
  echo "ERROR: Switch application template not found." >&2
  echo "Install switch-examples or clone switchbrew/switch-examples into _switch-examples." >&2
  exit 2
fi

WORKDIR="$(mktemp -d)"
trap 'rm -rf -- "${WORKDIR}"' EXIT
mkdir -p "${WORKDIR}/zomboidnx" "${ROOT}/out"
cp -a "${TEMPLATE}/." "${WORKDIR}/zomboidnx/"
# Replace the example program: do not link the template's sample application code.
mkdir -p "${WORKDIR}/zomboidnx/source"
find "${WORKDIR}/zomboidnx/source" -type f -delete
cp "${ROOT}/source/main.c" "${WORKDIR}/zomboidnx/source/main.c"

echo "Building with DEVKITPRO=${DEVKITPRO}"
make -C "${WORKDIR}/zomboidnx" -j2
NRO="${WORKDIR}/zomboidnx/zomboidnx.nro"
if [[ ! -s "${NRO}" ]]; then
  echo "ERROR: compiler finished without a non-empty .nro output." >&2
  exit 3
fi
cp "${NRO}" "${ROOT}/out/zomboidnx.nro"
echo "Created ${ROOT}/out/zomboidnx.nro"
sha256sum "${ROOT}/out/zomboidnx.nro"
