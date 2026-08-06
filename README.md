# TrapPack

Minecraft 1.21.8 · Fabric · the modpack for the Trap House server.

Install it once and it **updates itself every time you launch**. You should
never have to download a file again.

## Setup (do this once, then never again)

**1. Install [Prism Launcher](https://prismlauncher.org/)** and add your
Microsoft account.

**2. Import the pack.** Get `server.mrpack` from the server chat, then in Prism:
**Add Instance → Import → Browse** and pick it. This gets you Minecraft 1.21.8,
Fabric, and every mod in one go.

**3. Download the auto-updater.** Grab `packwiz-installer-bootstrap.jar` from
[the packwiz releases page](https://github.com/packwiz/packwiz-installer-bootstrap/releases)
(the only file there, about 20 KB).

**4. Put it in the instance.** Right-click your TrapPack instance → **Folder**.
That opens the instance directory; go into the `minecraft` folder inside it and
drop the jar there. It must sit next to `mods/` and `config/`, not above them.

**5. Turn on auto-updating.** Right-click the instance → **Edit** → **Settings**
→ tick **Custom commands**, and put this in **Pre-launch command**:

```
"$INST_JAVA" -jar packwiz-installer-bootstrap.jar https://heezq-git.github.io/trappack/pack.toml
```

**6. Hit Launch.**

Done. From now on every launch checks this repo first and pulls down whatever
changed — mods added, updated, or removed, and config changes. If nothing
changed it just starts. You never download a file again.

**Say yes to the resource pack prompt** when you join, or the custom blocks and
items won't render.

**Say yes to the resource pack prompt** when you join. The server's custom
blocks and items won't render without it.

## If something looks wrong

- **Purple-and-black blocks, or item names like `item.trapcraft.seeds_kush`** —
  you declined the resource pack. Rejoin and accept it.
- **"Failed to update" on launch** — you're offline, or GitHub is. You can play
  on the last-synced version; it'll catch up next time.
- **Nothing ever updates** — the pre-launch command probably isn't finding the
  jar. Check it's in the `minecraft` folder, not the instance folder above it,
  and that **Custom commands** is actually ticked.
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
