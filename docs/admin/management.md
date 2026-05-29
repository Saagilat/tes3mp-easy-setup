# Server management reference

## Common commands

All commands are run on the server via SSH. Replace `my-server` with your SSH host.

| Action | Command |
|--------|---------|
| Start | `ssh my-server "cd /tes3mp-easy && docker compose up -d"` |
| Stop | `ssh my-server "cd /tes3mp-easy && docker compose down"` |
| Restart | `ssh my-server "cd /tes3mp-easy && docker compose restart"` |
| View logs | `ssh my-server "cd /tes3mp-easy && docker compose logs -f"` |
| Edit config | `ssh my-server "nano /tes3mp-easy/container-data/tes3mp-server-default.cfg"` |
| Edit Lua config | `ssh my-server "nano /tes3mp-easy/container-data/server/scripts/config.lua"` |
| Edit ban list | `ssh my-server "nano /tes3mp-easy/container-data/server/data/banlist.json"` |
| Sync mods | `tes3mp-easy-server-update-mods` |

## HTTP endpoints

The server can provide optional HTTP endpoints on port **8085**.
All endpoints are disabled by default.

| Endpoint | Description | Backend |
|----------|-------------|---------|
| `/get-mods` | Download all server mods (`mods.zip`) | nginx (static file) |
| `/get-server-scripts` | Download all custom Lua scripts (`server-scripts.zip`) | nginx (static file) |
| `/get-world` | Download players + cells for world recovery (combined tar.gz) | export service |

To enable endpoints:

1. **Uncomment the desired location blocks** in `/tes3mp-easy/nginx.conf`
2. For `/get-world` — also **uncomment the `export` service** in `/tes3mp-easy/docker-compose.yml`
3. **Uncomment the `nginx` service** in `docker-compose.yml` (required for all endpoints)
4. Restart the container:

   ```bash
   ssh my-server "cd /tes3mp-easy && docker compose restart"
   ```

When enabled, endpoints are available at:
- `http://<server-ip>:8085/get-mods`
- `http://<server-ip>:8085/get-server-scripts`
- `http://<server-ip>:8085/get-world`

## Further reading

- [Modding — what works and what doesn't in TES3MP 0.8.1](modding.md)
- [config.lua reference — full settings documentation](tes3mp_settings.md)