#!/bin/sh

set -e

echo "[+] Starting the HADES frontend..."
./server -b $VITE_BACKEND -p $PORT
