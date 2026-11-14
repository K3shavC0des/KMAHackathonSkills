"""Register the bundled, unchanged ECC source through Codex's native plugin CLI."""
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import zipfile


def filesystem_path(path):
    """Use extended Windows paths for ECC's deeply nested exported files."""
    path = path.resolve()
    if os.name != "nt":
        return path
    value = str(path)
    if value.startswith("\\\\?\\"):
        return path
    if value.startswith("\\\\"):
        return Path("\\\\?\\UNC\\" + value[2:])
    return Path("\\\\?\\" + value)


def run_codex(args, *command):
    env = os.environ.copy()
    if args.codex_home:
        env["CODEX_HOME"] = str(args.codex_home.resolve())
    result = subprocess.run(
        [args.codex, "plugin", *command, "--json"],
        env=env, check=True, capture_output=True, text=True, encoding="utf-8",
    )
    return json.loads(result.stdout)


def source_matches(archive, root):
    """Check every exported file, including scripts and assets, against the ZIP."""
    for entry in archive.infolist():
        if entry.is_dir():
            continue
        file = root / entry.filename
        if file.is_symlink() or not file.is_file() or file.read_bytes() != archive.read(entry):
            raise ValueError(f"ECC snapshot missing or changed: {file}")


def setup_ecc(root, lock, args):
    snapshot = next(source for source in lock["sources"] if source["bundle"] == "ecc")
    source = filesystem_path(root / ".kma" / "ecc" / snapshot["commit"])
    if args.dry_run:
        print(f"Would unpack ECC {snapshot['version']} -> {source}")
        print(f"Would run: {args.codex} plugin marketplace add {source}")
        print(f"Would run: {args.codex} plugin add ecc@ecc")
        return
    if not shutil.which(args.codex):
        raise ValueError("Codex CLI not found. Set --codex PATH or use --skills-only.")
    if args.codex_home and not args.check:
        args.codex_home.resolve().mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(root / snapshot["archive"]) as archive:
        if not args.check:
            if source.exists():
                source_matches(archive, source)
            else:
                # Validate paths and entry types before extracting the pinned source.
                for entry in archive.infolist():
                    if not (source / entry.filename).resolve().is_relative_to(source.resolve()):
                        raise ValueError(f"Unsafe archive path: {entry.filename}")
                    if stat.S_ISLNK(entry.external_attr >> 16):
                        raise ValueError(f"Unsupported archive link: {entry.filename}")
                archive.extractall(source)
                if os.name != "nt":
                    for entry in archive.infolist():
                        mode = (entry.external_attr >> 16) & 0o777
                        if mode:
                            (source / entry.filename).chmod(mode)
            added = run_codex(args, "marketplace", "add", str(source))
            registered_root = Path(added["installedRoot"])
            if not registered_root.samefile(source):
                raise ValueError(
                    "Existing ecc marketplace points elsewhere. Review it with "
                    "'codex plugin marketplace list --json'. If replacement is intended, "
                    "remove that marketplace with 'codex plugin marketplace remove ecc' "
                    "and rerun this installer."
                )
            result = run_codex(args, "add", "ecc@ecc")
            cache = filesystem_path(Path(result["installedPath"]))
            if result["version"] != snapshot["version"]:
                raise ValueError("Installed ECC version does not match the pinned snapshot")
        else:
            # Registration alone does not prove that the cached files are complete.
            codex_home = args.codex_home
            if codex_home is None:
                codex_home = Path(os.environ["CODEX_HOME"]) if os.environ.get("CODEX_HOME") else Path.home() / ".codex"
            cache = filesystem_path(codex_home / "plugins" / "cache" / "ecc" / "ecc" / snapshot["version"])
        installed = run_codex(args, "list", "--marketplace", "ecc")["installed"]
        if not any(item.get("pluginId") == "ecc@ecc" and item.get("enabled")
                   and item.get("version") == snapshot["version"] for item in installed):
            raise ValueError("Pinned ECC plugin is not installed and enabled")
        source_matches(archive, cache)
    print(f"Verified ECC {snapshot['version']} native plugin and full cached source: {cache}")
    if not args.check:
        print("Restart Codex; review ECC hook trust in /hooks, then use $configure-ecc.")

