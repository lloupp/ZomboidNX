#!/usr/bin/env python3
"""Metadata-only inventory of a legitimately installed Project Zomboid copy.

Reads relative filenames, sizes, binary architecture markers and Java headers.
Does NOT export, alter, decompile or hash any proprietary game files.
"""
import argparse
import collections
import datetime
import json
import os
from pathlib import Path
import platform
import struct
import sys
import zipfile

IMPORTANT = {'.jar', '.dll', '.so', '.exe', '.dylib', '.json', '.sh', '.bat', '.cfg', '.ini'}
MAX_DETAIL = 3000


def bin_type(path: Path):
    try:
        with path.open('rb') as stream:
            head = stream.read(64)
    except OSError:
        return 'unreadable'

    if head[:4] == b'\x7fELF' and len(head) >= 20:
        endian = '<' if head[5] == 1 else '>'
        machine = struct.unpack(endian + 'H', head[18:20])[0]
        return 'ELF-' + {3: 'x86', 62: 'x86_64', 40: 'ARM', 183: 'AArch64'}.get(machine, str(machine))

    if head[:2] == b'MZ':
        try:
            with path.open('rb') as stream:
                stream.seek(0x3c)
                offset = struct.unpack('<I', stream.read(4))[0]
                if offset > 16 * 1024 * 1024:
                    return 'PE-unknown'
                stream.seek(offset)
                pe = stream.read(6)
                if pe[:4] == b'PE\x00\x00':
                    machine = struct.unpack('<H', pe[4:6])[0]
                    return 'PE-' + {0x14c: 'x86', 0x8664: 'x86_64', 0xaa64: 'ARM64'}.get(machine, hex(machine))
        except (OSError, struct.error):
            pass
        return 'PE-unknown'

    return 'unknown'


def java_bytecode(path: Path):
    """Sample one Java class header, not a global maximum version."""
    try:
        with zipfile.ZipFile(path) as archive:
            for name in archive.namelist():
                if name.endswith('.class') and not name.startswith('META-INF/versions/'):
                    with archive.open(name) as stream:
                        header = stream.read(8)
                    if len(header) == 8 and header[:4] == b'\xca\xfe\xba\xbe':
                        return struct.unpack('>H', header[6:8])[0]
                    return None
    except (OSError, zipfile.BadZipFile, RuntimeError):
        pass
    return None


def scan(root: Path):
    total_files = 0
    total_bytes = 0
    selected = []
    counts = collections.Counter()
    binary_formats = collections.Counter()
    unreadable = 0

    for base, dirs, files in os.walk(root, followlinks=False):
        dirs[:] = [name for name in dirs if not (Path(base) / name).is_symlink()]
        for name in files:
            path = Path(base) / name
            if path.is_symlink():
                continue
            try:
                stat = path.stat()
            except OSError:
                unreadable += 1
                continue

            total_files += 1
            total_bytes += stat.st_size
            extension = path.suffix.lower()
            if extension not in IMPORTANT:
                continue
            counts[extension] += 1
            if len(selected) >= MAX_DETAIL:
                continue

            entry = {'path': path.relative_to(root).as_posix(), 'bytes': stat.st_size}
            if extension in {'.dll', '.exe', '.so'}:
                entry['binary_format'] = bin_type(path)
                binary_formats[entry['binary_format']] += 1
            if extension == '.jar':
                entry['class_major_example'] = java_bytecode(path)
            selected.append(entry)

    return {
        'report_format': 'zomboidnx-inventory-v2',
        'created_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'machine_os': platform.system(),
        'files_total': total_files,
        'bytes_total': total_bytes,
        'files_by_extension': dict(sorted(counts.items())),
        'binary_formats': dict(sorted(binary_formats.items())),
        'selected_files': sorted(selected, key=lambda item: item['path'].lower()),
        'selected_truncated': sum(counts.values()) > MAX_DETAIL,
        'unreadable_count': unreadable,
        'note': 'Metadata only: relative filenames, byte sizes, binary format and Java class major sample. No game contents exported.',
    }


def main():
    parser = argparse.ArgumentParser(description='Generate a metadata-only Project Zomboid compatibility inventory')
    parser.add_argument('game_dir', type=Path, help='Path to your Steam Project Zomboid installation')
    parser.add_argument('--output', type=Path, default=Path('zomboid-inventory.json'))
    args = parser.parse_args()

    root = args.game_dir.expanduser().resolve()
    if not root.is_dir():
        parser.error('Game installation directory does not exist: ' + str(root))
    if not any((root / item).exists() for item in
               ['ProjectZomboid64.exe', 'ProjectZomboid32.exe', 'projectzomboid.sh', 'ProjectZomboid', 'zombie']):
        print('WARNING: No recognized launcher found; confirm this is the Steam game directory.', file=sys.stderr)

    payload = scan(root)
    args.output.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding='utf-8')
    print('Saved:', args.output.resolve())
    print('Total files:', payload['files_total'])
    print('Selected metadata records:', len(payload['selected_files']))
    print('Unreadable files:', payload['unreadable_count'])
    print('Review the JSON before sharing. Do not send proprietary files or credentials.')


if __name__ == '__main__':
    main()
