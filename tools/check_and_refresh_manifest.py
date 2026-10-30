#!/usr/bin/env python3
"""Refresh current-branch AI Studio import inventory; fail rather than exceed 950 files."""
from pathlib import Path
import hashlib
import json
import subprocess

root = Path(__file__).resolve().parent.parent
tracked = subprocess.check_output(["git", "ls-files", "-z"], cwd=root).decode().split("\0")
# Capture even staged/new current branch files, excluding the self-referential manifest.
paths = sorted(p for p in tracked if p and p != "docs/FILE_MANIFEST.json" and (root / p).is_file())
count = len(paths) + 1
if count > 950:
    raise SystemExit(f"AI Studio import would exceed 950 files: {count}")
entries = [
    {"path": p, "sha256": hashlib.sha256((root / p).read_bytes()).hexdigest(),
     "size": (root / p).stat().st_size}
    for p in paths
]
body = {
    "file_count_including_manifest": count,
    "max_files": 950,
    "source_import_native": "648e971034201511d69585cd5deecaa27eddf942",
    "source_import_pr279": "5ff8cbd0da6533d04e0696229cb013936ae39619",
    "source_import_pr277": "9aa3721ca675cd66b4fa04d1c91e2b6a871c04ed",
    "hashes_reflect": "current repository files, not only original imported snapshots",
    "files": entries,
}
dest = root / "docs/FILE_MANIFEST.json"
dest.write_text(json.dumps(body, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"OK: tracked files including manifest: {count} <= 950")
