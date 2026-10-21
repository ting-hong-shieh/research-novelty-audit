"""Smoke tests for safe skill installation. Run with python -m unittest discover -s tests."""
from pathlib import Path
import importlib.util
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]

spec = importlib.util.spec_from_file_location('skill_installer', ROOT / 'scripts' / 'install.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class InstallationTests(unittest.TestCase):
    def test_does_not_package_git_or_cache_files(self):
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            (root / 'SKILL.md').write_text('skill')
            (root / 'README.md').write_text('readme')
            (root / '.git').mkdir()
            (root / '.git' / 'config').write_text('token=secret')
            (root / 'scripts').mkdir()
            (root / 'scripts' / 'setup.py').write_text('print(1)')
            (root / 'scripts' / '__pycache__').mkdir()
            (root / 'scripts' / '__pycache__' / 'setup.pyc').write_text('cached')
            (root / 'tests').mkdir()
            (root / 'tests' / 'test_random.py').write_text('test')
            included = {p.relative_to(root).as_posix() for p in module.all_files(root)}
            self.assertEqual(included, {'SKILL.md', 'README.md', 'scripts/setup.py'})

    def test_copies_agent_profiles_and_is_idempotent(self):
        with tempfile.TemporaryDirectory() as tempdir:
            cmd = [sys.executable, str(ROOT / 'scripts' / 'install.py'),
                   '--scope', 'project', '--project-dir', tempdir, '--platform', 'both']
            first = subprocess.run(cmd, text=True, capture_output=True)
            self.assertEqual(first.returncode, 0, first.stderr)
            target = Path(tempdir)
            self.assertTrue((target / '.claude' / 'skills' / 'research-novelty-audit' / 'SKILL.md').is_file())
            self.assertTrue((target / '.claude' / 'agents' / 'novelty-closest.md').is_file())
            self.assertTrue((target / '.agents' / 'skills' / 'research-novelty-audit' / 'SKILL.md').is_file())
            self.assertTrue((target / '.codex' / 'agents' / 'novelty_closest.toml').is_file())
            self.assertFalse((target / '.claude' / 'skills' / 'research-novelty-audit' / '.git').exists())
            second = subprocess.run(cmd, text=True, capture_output=True)
            self.assertEqual(second.returncode, 0, second.stderr)
            self.assertIn('Installed: 0 files', second.stdout)


if __name__ == '__main__':
    unittest.main()
