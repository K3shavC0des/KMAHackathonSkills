#!/usr/bin/env python3
"""Install the bundled upstream Agent Skills into a Codex project."""
import argparse
import hashlib
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SKILLS = ("graphify", "headroom", "claude-mem", "omniroute", "task-observer", "claude-code-setup", "hackathon-autopilot")

def digest(path):
    h = hashlib.sha256()
    for f in sorted(p for p in path.rglob("*") if p.is_file()):
        h.update(f.relative_to(path).as_posix().encode())
        h.update(f.read_bytes())
    return h.hexdigest()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", type=Path, default=Path.cwd(), help="Codex project root")
    ap.add_argument("--check", action="store_true", help="verify installed skills match this bundle")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--force", action="store_true", help="replace installed skills that differ")
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
        elif not args.dry_run:
            dst.parent.mkdir(parents=True, exist_ok=True)
            if dst.exists(): shutil.rmtree(dst)
            shutil.copytree(src, dst)
            print(f"Installed {name}")
        else: print(f"Would install {name} -> {dst}")
    if args.check and not failures: print(f"Verified {len(SKILLS)} skills in {target}")
    for error in failures: print(error)
    return bool(failures)

if __name__ == "__main__": raise SystemExit(main())
