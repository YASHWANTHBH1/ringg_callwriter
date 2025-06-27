#!/bin/bash

# Install Playwright Chromium browser
playwright install chromium

# Start the FastAPI app
uvicorn main:app --host 0.0.0.0 --port 8000
