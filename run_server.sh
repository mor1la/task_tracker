#!/bin/bash
cd ~/noco_db/ && docker compose up
cd ~/python_p/fastapi_simple_auth && uvicorn app.main:app --reload