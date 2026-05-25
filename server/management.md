# Managing the TES3MP server (Docker)

All commands are run as root on the VPS.

| Action | Command | Details |
|--------|---------|---------|
| Start | `docker compose up -d --build` | |
| View live logs | `docker compose logs -f` | |
| Stop | `docker compose down` | |
| Edit config | `nano /opt/tes3mp/data/tes3mp-server-default.cfg` | Afterwards, run **Start** to apply changes |

---

## Build and start

```bash
cd /opt/tes3mp
docker compose up -d --build
```

What happens:
- Stops the old container
- Rebuilds the Docker image (picks up changes in configs, mods, scripts)
- Creates and starts a new container

Player progress (characters, inventory, cells) is stored in named volumes `tes3mp-characters` and `tes3mp-cells`. They are not deleted on rebuild, so data is preserved.

---

## Enabling endpoints: /get-mods, /get-world, /get-characters

All three endpoints are **disabled by default**. Enabling them is **recommended** — they allow players to easily download mods, and give access to world/character data for debugging, backups, or community tools.

### Available endpoints

| Endpoint | Description | Archive |
|----------|-------------|---------|
| `/get-mods` | Download all server mods (`.esp`/`.esm` files) | `mods.zip` |
| `/get-world` | Download world state (all cell JSON files) | `world_state.tar.gz` |
| `/get-characters` | Download all character data | `characters.tar.gz` |

### Before enabling — understand the implications

Enabling `/get-world` and `/get-characters` makes your server's data **publicly readable**:
- **Character data**: anyone with the server IP can download all characters — their inventories, skills, spells, quest progress, etc.
- **World state**: anyone can download every cell, every placed item, every modified object.
- **This can affect gameplay** — players could inspect each other's progress, bases, or hidden stashes.

Consider whether this fits your server's vision. For a co-op or roleplay server it can be a **valuable feature** (transparency, backups, community analytics). For a competitive server you may want to keep character data private.

### To enable

1. **Uncomment the desired location blocks** in `/opt/tes3mp/nginx.conf`.
2. For `/get-world` and `/get-characters` you also need to **uncomment the `export` service** in `/opt/tes3mp/docker-compose.yml`.
3. Uncomment the **`nginx` service** in docker-compose.yml (required for all endpoints).
4. Rebuild and restart:
   ```bash
   cd /opt/tes3mp && docker compose up -d --build
   ```

### To disable

Reverse the steps above and rebuild.

### Notes

- Rate limit: each endpoint has its own configurable limit (default: **5 requests per minute** per IP). Archive is cached for 10 minutes.
- When enabled, endpoints are available at:
  - `http://<server-IP>:8085/get-mods`
  - `http://<server-IP>:8085/get-world`
  - `http://<server-IP>:8085/get-characters`
