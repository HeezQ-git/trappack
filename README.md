# TrapPack

Minecraft 1.21.8 · Fabric · the modpack for the Trap House server.

Install it once and it **updates itself every time you launch**. You should
never have to download a file again.

## Setup (do this once)

1. Install [Prism Launcher](https://prismlauncher.org/) and add your Microsoft
   account.
2. Download the starter instance from the server chat and import it:
   **Add Instance → Import → Browse**.
3. Hit **Launch**.

That's it. On every launch the pack checks this repo and pulls down anything
that changed — new mods, updated mods, removed mods, config changes. If nothing
changed it starts normally.

**Say yes to the resource pack prompt** when you join. The server's custom
blocks and items won't render without it.

## If something looks wrong

- **Purple-and-black blocks, or item names like `item.trapcraft.seeds_kush`** —
  you declined the resource pack. Rejoin and accept it.
- **"Failed to update" on launch** — you're offline, or GitHub is. You can play
  on the last-synced version; it'll catch up next time.
- **A mod others have and you don't** — check the pack version in Prism against
  what everyone else has. Mismatched versions are the usual cause of
  "works for me".

## What's in here

`pack.toml` and `index.toml` are the manifest. `mods/*.pw.toml` are one small
metadata file per mod — the mods themselves download from Modrinth on demand,
which is why this repo is small. `config/` is the shared configuration, and a
couple of jars that aren't on Modrinth live directly in `mods/`.

Everything is pinned to exact versions. Nothing updates because upstream
released something new; it updates because someone changed it here.

## Maintainers

Regenerate from a fresh Modrinth App export:

```bash
python3 tools/from_mrpack.py && packwiz refresh && git commit -am "update" && git push
```

Players get it on their next launch.
