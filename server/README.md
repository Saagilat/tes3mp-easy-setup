# Server

This directory contains documentation and files for setting up and managing a TES3MP server via Docker.

## Documentation

| File | Description |
|------|-------------|
| [install.md](install.md) | Quick install script (recommended) |
| [management.md](management.md) | Daily server management (start, stop, logs, config, endpoints) |
| [modding.md](modding.md) | Adding mods to the server (scripts by OS) |
| [tes3mp_settings.md](tes3mp_settings.md) | Full `config.lua` reference with all settings |

## Files

- [docker/](docker/) — Docker files (compose, Dockerfiles, nginx config, export script)
- [scripts/](scripts/) — Shell scripts (`install.sh`, `update_mods.sh`)