#!/bin/bash

# Install OS-level dependencies for Chromium to work
apt-get update && apt-get install -y wget gnupg ca-certificates fonts-liberation libasound2 \
    libatk-bridge2.0-0 libatk1.0-0 libcups2 libdbus-1-3 libgdk-pixbuf2.0-0 libnspr4 libnss3 \
    libxcomposite1 libxdamage1 libxrandr2 xdg-utils libxss1 libxtst6 libgbm1 libglib2.0-0

# Install playwright browsers (if not cached)
playwright install chromium

# Start your backend server
uvicorn main:app --host 0.0.0.0 --port 8000

