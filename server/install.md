# Installing TES3MP Server on Linux (via Docker)

## Quick install (recommended)

The script will install Docker, download the server, configure it, and start the container.

```bash
curl -fsSL https://raw.githubusercontent.com/Saagilat/tes3mp-guide/master/server/files/scripts/install.sh | bash
```

Or download and run:

```bash
wget https://raw.githubusercontent.com/Saagilat/tes3mp-guide/master/server/files/scripts/install.sh
sudo bash install.sh
```

The script will ask:

- Server name
- Admin password (can be left empty)
- Max players
- Which HTTP endpoints to enable (with explanations of risks)

Everything else is handled automatically.

---

<details>
<summary>Manual installation (in case the script doesn't fit your needs)</summary>

## 1. Install dependencies

TES3MP server requires: **Docker, Docker Compose, rsync, nano**.

### Arch Linux — via AUR (paru / yay)

```bash
sudo pacman -Syu --noconfirm
```

```bash
sudo pacman -S docker docker-compose rsync nano python tar zip
```

```bash
sudo systemctl enable --now docker
```

### Other Linux distros (Debian, Ubuntu, Fedora, etc.) — without AUR

Use the official Docker convenience script (works on any distribution):

```bash
curl -fsSL https://get.docker.com | sh
```

```bash
sudo systemctl enable --now docker
```

To use docker without `sudo`, add your user to the `docker` group:

```bash
sudo usermod -aG docker $USER
```

Then log out and back in (or run `newgrp docker`).

You'll also need Docker Compose. Install it from the official repo:

```bash
sudo apt-get install docker-compose-plugin   # Debian/Ubuntu
# OR
sudo dnf install docker-compose-plugin        # Fedora
```

Install the rest of the utilities:

```bash
sudo apt-get install -y rsync nano python3 tar zip   # Debian/Ubuntu
# OR
sudo dnf install -y rsync nano python tar zip        # Fedora
```

## 2. Create the folder structure

```bash
sudo mkdir -p /opt/tes3mp/data /opt/tes3mp/mods
```

```bash
sudo chown -R $USER:$USER /opt/tes3mp
```

If logged in as root, `chown` is not needed.

## 3. Download and extract the server

```bash
cd /opt/tes3mp/data
```

```bash
wget https://github.com/TES3MP/TES3MP/releases/download/tes3mp-0.8.1/tes3mp-server-GNU+Linux-x86_64-release-0.8.1-68954091c5-6da3fdea59.tar.gz
```

```bash
tar --strip-components=1 -xzf tes3mp-server-GNU+Linux-x86_64-release-0.8.1-68954091c5-6da3fdea59.tar.gz
```

```bash
rm tes3mp-server-GNU+Linux-x86_64-release-0.8.1-68954091c5-6da3fdea59.tar.gz
```

> `--strip-components=1` removes the root folder `TES3MP-server/` during extraction, so all files go directly into `/opt/tes3mp/data`.

## 4. Dockerfile and docker-compose.yml

Download the ready-made files from this repository:

```bash
cd /opt/tes3mp
```

```bash
wget https://raw.githubusercontent.com/Saagilat/tes3mp-guide/master/server/files/docker/tes3mp.dockerfile
```

```bash
wget https://raw.githubusercontent.com/Saagilat/tes3mp-guide/master/server/files/docker/docker-compose.yml
```

```bash
wget https://raw.githubusercontent.com/Saagilat/tes3mp-guide/master/server/files/docker/nginx.conf
```

```bash
wget https://raw.githubusercontent.com/Saagilat/tes3mp-guide/master/server/files/docker/export.dockerfile
```

```bash
wget https://raw.githubusercontent.com/Saagilat/tes3mp-guide/master/server/files/docker/export_server.py
```

```bash
wget https://raw.githubusercontent.com/Saagilat/tes3mp-guide/master/server/files/scripts/update_mods.sh
```

**Important**: mod files, configs, and scripts are all copied into the image at build time. After changing any file in `/opt/tes3mp/data/`, you must **rebuild the image**. Management commands (logs, stop, rebuild) are in [management.md](management.md).

The `tes3mp` container stores character data in the `tes3mp-characters` volume and world state in the `tes3mp-cells` volume.

---

## HTTP endpoints: /get-mods, /get-world, /get-characters

The server comes with optional HTTP endpoints that serve mods, world state, and character data over port `8085`:

| Endpoint | What it serves |
|----------|---------------|
| `/get-mods` | All server mods as `mods.zip` |
| `/get-world` | World state (all cell JSON files) as `world_state.tar.gz` |
| `/get-characters` | All character data as `characters.tar.gz` |

**All three are disabled by default.** Enabling them is **recommended** — `/get-mods` lets players easily download the mod pack, and the export endpoints are useful for debugging, backups, and community tools.

**Before enabling `/get-world` and `/get-characters`, consider:**
- Character data (inventories, skills, spells, quest progress) becomes publicly downloadable by anyone who knows the server IP.
- The entire world state becomes visible — all cells, placed items, modified objects.
- On a co-op or roleplay server this can be a **valuable feature** (backups, analytics, transparency). On a competitive server you may prefer to keep character data private.

**See [management.md](management.md) for step-by-step instructions on enabling and disabling endpoints.**

---

## 5. Build the image and start the server

```bash
cd /opt/tes3mp
```

```bash
docker compose up -d --build
```

</details>