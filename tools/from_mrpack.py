#!/usr/bin/env python3
"""Convert modpacks/server.mrpack into this packwiz pack.

Run once to seed the pack, and again whenever you re-export from the Modrinth
App and want packwiz to match it.

Why not `packwiz modrinth add` 136 times: that resolves each mod to its LATEST
version, which would silently change the pack everyone is running. The mrpack
index already pins exact version ids, so we generate the metadata from it and
nothing moves that you didn't ask to move.
"""

import json
import re
import shutil
import sys
import zipfile
from pathlib import Path

PACK = Path(__file__).resolve().parent.parent
MRPACK = PACK.parent / "modpacks/server.mrpack"

# CDN urls look like .../data/<projectId>/versions/<versionId>/<file>.jar
CDN = re.compile(r"/data/([^/]+)/versions/([^/]+)/")


def side_of(env: dict) -> str:
    client = env.get("client", "required") != "unsupported"
    server = env.get("server", "required") != "unsupported"
    if client and server:
        return "both"
    return "client" if client else "server"


def slug(filename: str) -> str:
    stem = Path(filename).stem
    stem = re.sub(r"[^A-Za-z0-9]+", "-", stem).strip("-").lower()
    return stem or "mod"


def toml_escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')


def main() -> None:
    if not MRPACK.exists():
        sys.exit(f"missing {MRPACK}")

    zin = zipfile.ZipFile(MRPACK)
    index = json.loads(zin.read("modrinth.index.json"))

    # Wipe previously generated metadata so removals actually propagate --
    # this is the thing Prism's update-from-file can't do.
    for old in PACK.rglob("*.pw.toml"):
        old.unlink()

    written = 0
    unresolved = []
    for entry in index["files"]:
        path = Path(entry["path"])
        url = entry["downloads"][0]
        match = CDN.search(url)
        target = PACK / path.parent / f"{slug(path.name)}.pw.toml"
        target.parent.mkdir(parents=True, exist_ok=True)

        lines = [
            f'name = "{toml_escape(path.stem)}"',
            f'filename = "{toml_escape(path.name)}"',
            f'side = "{side_of(entry.get("env") or {})}"',
            "",
            "[download]",
            f'url = "{toml_escape(url)}"',
            'hash-format = "sha512"',
            f'hash = "{entry["hashes"]["sha512"]}"',
        ]
        if match:
            project_id, version_id = match.groups()
            lines += [
                "",
                "[update.modrinth]",
                f'mod-id = "{project_id}"',
                f'version = "{version_id}"',
            ]
        else:
            # Still installable via the direct url, just not auto-updatable.
            unresolved.append(path.name)

        target.write_text("\n".join(lines) + "\n")
        written += 1

    # Overrides are plain files: packwiz hashes them into index.toml and the
    # installer pulls them straight off the Pages site. That includes
    # trapcraft's jar, so it needs no separate hosting.
    copied = 0
    for name in zin.namelist():
        if not name.startswith("overrides/") or name.endswith("/"):
            continue
        rel = Path(name).relative_to("overrides")
        dest = PACK / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        with zin.open(name) as src, open(dest, "wb") as out:
            shutil.copyfileobj(src, out)
        copied += 1

    zin.close()
    print(f"{written} mod metafiles, {copied} override files")
    if unresolved:
        print(f"NOT auto-updatable ({len(unresolved)}): {', '.join(unresolved[:5])}")
    print("now run: packwiz refresh")


if __name__ == "__main__":
    main()
