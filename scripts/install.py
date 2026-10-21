#!/usr/bin/env python3
"""Install the standalone skill and optional subagent profiles without clobbering files.

No external dependencies, no network requests, no shell execution.
"""
from __future__ import annotations

import argparse
import filecmp
import shutil
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent


def all_files(source: Path):
    """Package only the skill resources, not the clone's .git or local caches."""
    allowed_roots = {'README.md', 'SKILL.md', 'agents', 'assets', 'references', 'scripts'}
    ignored_parts = {'.git', '__pycache__', '.pytest_cache', '.venv', 'venv'}
    return sorted(
        p for p in source.rglob('*')
        if p.is_file()
        and not p.is_symlink()
        and p.relative_to(source).parts[0] in allowed_roots
        and not ignored_parts.intersection(p.relative_to(source).parts)
        and not p.name.endswith(('.pyc', '.pyo'))
    )


def plan(platform: str, scope: str, base: Path):
    if platform == 'claude':
        skill_dest = base / '.claude' / 'skills' / 'research-novelty-audit'
        agent_dir = base / '.claude' / 'agents'
        profile_dir = SKILL / 'agents' / 'claude'
    elif platform == 'codex':
        skill_dest = base / '.agents' / 'skills' / 'research-novelty-audit'
        agent_dir = base / '.codex' / 'agents'
        profile_dir = SKILL / 'agents' / 'codex'
    else:
        raise ValueError(platform)

    if SKILL.resolve() == skill_dest.resolve():
        # Installation already in the desired location; don't recursively copy it.
        entries = []
    else:
        entries = [(f, skill_dest / f.relative_to(SKILL)) for f in all_files(SKILL)]
    suffix = '.md' if platform == 'claude' else '.toml'
    entries += [(f, agent_dir / f.name) for f in sorted(profile_dir.glob('*' + suffix)) if f.is_file() and not f.is_symlink()]
    return entries


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--platform', choices=['claude', 'codex', 'both'], required=True)
    parser.add_argument('--scope', choices=['user', 'project'], default='user')
    parser.add_argument('--project-dir', type=Path, help='Repository root when scope=project (default: cwd)')
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--force', action='store_true', help='Update conflicting files; other existing files are retained')
    args = parser.parse_args()
    if args.scope == 'user' and args.project_dir is not None:
        parser.error('--project-dir requires --scope project')

    base = Path.home() if args.scope == 'user' else (args.project_dir or Path.cwd()).expanduser().resolve()
    platforms = ['claude', 'codex'] if args.platform == 'both' else [args.platform]
    entries = [entry for platform in platforms for entry in plan(platform, args.scope, base)]
    conflicts = [(src, dst) for src, dst in entries if dst.exists() and not (dst.is_file() and filecmp.cmp(src, dst, shallow=False))]
    if conflicts and not args.force:
        print('ERROR: existing files differ; no changes were made. Check paths or rerun with --force:', file=sys.stderr)
        for _, dst in conflicts:
            print(f'  {dst}', file=sys.stderr)
        return 2

    copied = unchanged = 0
    for src, dst in entries:
        if dst.exists() and dst.is_file() and filecmp.cmp(src, dst, shallow=False):
            unchanged += 1
            continue
        if args.dry_run:
            print(f'PLAN {src} -> {dst}')
        else:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            print(f'INSTALLED {dst}')
        copied += 1

    print(f'{"Planned" if args.dry_run else "Installed"}: {copied} files; unchanged: {unchanged}; base: {base}')
    print('Note: actual parallel subagent spawning depends on your agent host, permissions, and tool availability.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
