#!/usr/bin/env python3
"""
export_server.py — lightweight HTTP server that exports TES3MP world state and
character data as tar.gz archives on demand.

Endpoints:
  /get-world      — serves a tar.gz of the cells volume contents
  /get-characters — serves a tar.gz of the characters volume contents

The archive is cached for CACHE_MINUTES minutes. If a request comes in within
that window, the cached archive is served immediately. Otherwise it is rebuilt
from the live volumes.

Environment variables:
  CHARACTERS_DIR — path to the characters volume (default: /mnt/characters)
  CELLS_DIR     — path to the cells volume   (default: /mnt/cells)
  CACHE_DIR     — path to store cached archives (default: /tmp/export_cache)
  CACHE_MINUTES — cache TTL (default: 10)
"""

import io
import os
import tarfile
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path

CHARACTERS_DIR = Path(os.environ.get("CHARACTERS_DIR", "/mnt/characters"))
CELLS_DIR = Path(os.environ.get("CELLS_DIR", "/mnt/cells"))
CACHE_DIR = Path(os.environ.get("CACHE_DIR", "/tmp/export_cache"))
CACHE_MINUTES = int(os.environ.get("CACHE_MINUTES", "10"))
CACHE_TTL = CACHE_MINUTES * 60  # seconds

# Ensure cache directory exists
CACHE_DIR.mkdir(parents=True, exist_ok=True)


def pack_directory(source_dir: Path) -> bytes:
    """Pack the entire contents of source_dir into a tar.gz bytes object."""
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w:gz") as tar:
        for entry in sorted(source_dir.rglob("*")):
            arcname = entry.relative_to(source_dir)
            tar.add(str(entry), arcname=str(arcname))
    return buf.getvalue()


def get_cached_or_build(source_dir: Path, archive_path: Path) -> bytes:
    """
    Return cached archive if it exists and is fresh,
    otherwise rebuild and cache it.
    """
    now = time.time()
    if archive_path.is_file():
        mtime = archive_path.stat().st_mtime
        if now - mtime < CACHE_TTL:
            return archive_path.read_bytes()

    # Rebuild
    data = pack_directory(source_dir)
    archive_path.write_bytes(data)
    return data


class ExportHandler(BaseHTTPRequestHandler):
    """HTTP request handler for world/character export endpoints."""

    def _serve_archive(self, source_dir: Path, archive_name: str):
        archive_path = CACHE_DIR / archive_name
        try:
            data = get_cached_or_build(source_dir, archive_path)
        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(f"Export error: {e}\n".encode())
            return

        self.send_response(200)
        self.send_header("Content-Type", "application/gzip")
        self.send_header("Content-Disposition", f'attachment; filename="{archive_name}"')
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path == "/get-world":
            self._serve_archive(CELLS_DIR, "world_state.tar.gz")
        elif self.path == "/get-characters":
            self._serve_archive(CHARACTERS_DIR, "characters.tar.gz")
        else:
            self.send_response(404)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Not found\n")

    def log_message(self, format, *args):
        """Suppress default logging; we don't need noisy stdout."""
        pass


def main():
    port = int(os.environ.get("PORT", "5000"))
    server = HTTPServer(("0.0.0.0", port), ExportHandler)
    print(f"Export server listening on port {port}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down.", flush=True)
        server.server_close()


if __name__ == "__main__":
    main()