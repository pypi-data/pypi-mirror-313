#! /bin/bash
set -e
uvicorn --host 0.0.0.0 --port 80 --workers 1 --forwarded-allow-ips=* torrent_worker.app:app
#!/bin/bash

# Run qBittorrent from extracted directory
cd /app/bin/extracted
./AppRun "$@"
