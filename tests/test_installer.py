import tempfile
import unittest
from pathlib import Path
import sys
import subprocess

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from install import digest


class AgentComparisonTests(unittest.TestCase):
    def test_fresh_install_check_and_preserve_edits(self):
        installer = Path(__file__).resolve().parents[1] / 'install.py'
        with tempfile.TemporaryDirectory() as folder:
            command = [sys.executable, str(installer), '--project', folder, '--skills-only']
            for extra in ([], [], ['--check']):
                result = subprocess.run(command + extra, capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            launcher = Path(folder) / 'codex-headroom.cmd'
            launcher.write_text('custom launcher\n')
            result = subprocess.run(command, capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('Existing edits preserved', result.stdout)
            self.assertEqual(launcher.read_text(), 'custom launcher\n')

    def test_windows_checkout_line_endings_match(self):
        with tempfile.TemporaryDirectory() as folder:
            left, right = Path(folder) / 'left', Path(folder) / 'right'
            left.mkdir()
            right.mkdir()
            (left / 'reviewer.toml').write_bytes(b'model = "example"\n')
            (right / 'reviewer.toml').write_bytes(b'model = "example"\r\n')
            self.assertEqual(digest(left), digest(right))
            (right / 'reviewer.toml').write_bytes(b'model = "changed"\r\n')
            self.assertNotEqual(digest(left), digest(right))


if __name__ == '__main__':
    unittest.main()
