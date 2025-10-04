#!/bin/sh

set -e

msfdb init

echo "[+] Starting the HADES backend..."
uvicorn hades.main:api --host 0.0.0.0 --port 8888
