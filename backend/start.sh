#!/bin/bash
python -m playwright install --with-deps
uvicorn main:app --host 0.0.0.0 --port $PORT
