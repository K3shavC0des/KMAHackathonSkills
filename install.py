#!/usr/bin/env python3
"""Install project Agent Skills and the bundled native ECC plugin for Codex."""
import argparse
import hashlib
import json
import shutil
import subprocess
from pathlib import Path
from ecc_setup import setup_ecc

ROOT = Path(__file__).resolve().parent
SKILLS = ("graphify", "headroom", "claude-mem", "task-observer", "claude-code-setup", "hackathon-autopilot")
AGENTS = ROOT / ".codex" / "agents"

def digest(path):
    h = hashlib.sha256()
    for f in sorted(p for p in path.rglob("*") if p.is_file()):
        h.update(f.relative_to(path).as_posix().encode())
        h.update(f.read_bytes())
    return h.hexdigest()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", type=Path, default=Path.cwd(), help="Codex project root")
    ap.add_argument("--check", action="store_true", help="verify installed skills and the pinned ECC plugin")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--force", action="store_true", help="replace installed skills that differ")
    ap.add_argument("--skills-only", action="store_true", help="copy project skills without registering ECC")
    ap.add_argument("--codex", default="codex", help="Codex CLI executable (default: codex)")
    ap.add_argument("--codex-home", type=Path, help="explicit Codex home, for example an isolated test directory")
    args = ap.parse_args()
    lock = json.loads((ROOT / "upstream-lock.json").read_text(encoding="utf-8-sig"))
    for relative, expected in lock["sha256"].items():
        file = ROOT / relative
        if not file.is_file() or hashlib.sha256(file.read_bytes()).hexdigest() != expected:
            print(f"Bundle verification failed: {relative}")
            return 1
    target = args.project.resolve() / ".agents" / "skills"
    failures = []
    for name in SKILLS:
        src = ROOT / "vendor" / name
        if name == "hackathon-autopilot": src = ROOT / ".agents" / "skills" / name
        dst = target / name
        if not (src / "SKILL.md").is_file():
            failures.append(f"Bundle incomplete: {src / 'SKILL.md'}")
        elif args.check:
            if not dst.is_dir() or digest(src) != digest(dst): failures.append(f"Missing or changed: {dst}")
        elif dst.is_symlink():
            failures.append(f"Refusing symbolic link: {dst}")
        elif dst.exists() and not dst.is_dir():
            failures.append(f"Not a directory: {dst}")
        elif dst.exists() and digest(src) != digest(dst) and not args.force:
            failures.append(f"Existing edits preserved: {dst}; use --force to replace")
        elif src.resolve() == dst.resolve():
            print(f"Already present: {name}")
        elif dst.is_dir() and digest(src) == digest(dst):
            print(f"Already present: {name}")
        elif not args.dry_run:
            dst.parent.mkdir(parents=True, exist_ok=True)
            if dst.exists(): shutil.rmtree(dst)
            shutil.copytree(src, dst)
            print(f"Installed {name}")
        else: print(f"Would install {name} -> {dst}")
    agents_target = args.project.resolve() / ".codex" / "agents"
    if not AGENTS.is_dir():
        failures.append(f"Bundle incomplete: {AGENTS}")
    elif args.check:
        if not agents_target.is_dir() or digest(AGENTS) != digest(agents_target):
            failures.append(f"Missing or changed: {agents_target}")
    elif agents_target.is_symlink():
        failures.append(f"Refusing symbolic link: {agents_target}")
    elif agents_target.exists() and not agents_target.is_dir():
        failures.append(f"Not a directory: {agents_target}")
    elif agents_target.exists() and digest(AGENTS) != digest(agents_target) and not args.force:
        failures.append(f"Existing edits preserved: {agents_target}; use --force to replace")
    elif agents_target.is_dir() and digest(AGENTS) == digest(agents_target):
        print(f"Already present: {agents_target}")
    elif not args.dry_run:
        agents_target.parent.mkdir(parents=True, exist_ok=True)
        if agents_target.exists(): shutil.rmtree(agents_target)
        shutil.copytree(AGENTS, agents_target)
        print(f"Installed Codex agents -> {agents_target}")
    else:
        print(f"Would install Codex agents -> {agents_target}")
    if args.check and not failures: print(f"Verified {len(SKILLS)} skills in {target}")
    for error in failures: print(error)
    if not failures and not args.skills_only:
        setup_ecc(ROOT, lock, args)
    return bool(failures)

if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        print(f"Setup failed: {error}")
        if isinstance(error, subprocess.CalledProcessError) and error.stderr:
            print(error.stderr.strip())
        raise SystemExit(1)
