"""Synthetic scanner tests; no commercial game files are required."""
import importlib.util
from pathlib import Path
import struct
import tempfile
import unittest
import zipfile

SCANNER = Path(__file__).resolve().parents[1] / 'tools' / 'inventory-project-zomboid.py'
spec = importlib.util.spec_from_file_location('zomboid_inventory', SCANNER)
inventory = importlib.util.module_from_spec(spec)
spec.loader.exec_module(inventory)


class InventoryTests(unittest.TestCase):
    def test_architectures_java_metadata_and_no_asset_export(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / 'ProjectZomboid64.exe').write_bytes(
                b'MZ' + bytes(58) + struct.pack('<I', 64)
                + b'PE\x00\x00' + struct.pack('<H', 0x8664)
            )
            (root / 'example.so').write_bytes(
                b'\x7fELF' + bytes([2, 1]) + bytes(12) + struct.pack('<H', 183)
            )
            with zipfile.ZipFile(root / 'sample.jar', 'w') as archive:
                archive.writestr('demo/Main.class', b'\xca\xfe\xba\xbe\x00\x00\x00\x3d')
            (root / 'media').mkdir()
            (root / 'media' / 'asset.txt').write_text('synthetic test content')

            report = inventory.scan(root)
            self.assertEqual(report['files_total'], 4)
            self.assertEqual(report['binary_formats']['PE-x86_64'], 1)
            self.assertEqual(report['binary_formats']['ELF-AArch64'], 1)
            selected = {entry['path']: entry for entry in report['selected_files']}
            self.assertEqual(selected['sample.jar']['class_major_example'], 61)
            self.assertNotIn('media/asset.txt', selected)
            self.assertFalse(report['selected_truncated'])

    def test_empty_directory(self):
        with tempfile.TemporaryDirectory() as folder:
            report = inventory.scan(Path(folder))
            self.assertEqual(report['files_total'], 0)
            self.assertEqual(report['selected_files'], [])


if __name__ == '__main__':
    unittest.main()
