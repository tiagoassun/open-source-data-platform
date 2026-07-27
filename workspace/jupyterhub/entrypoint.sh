#!/usr/bin/env bash
set -euo pipefail

echo "Waiting for postgres-metadata..."
until python - <<'PY'
import os, sys
try:
    import psycopg2
    psycopg2.connect(os.environ["DATABASE_URL"]).close()
except Exception as exc:
    print(exc)
    sys.exit(1)
sys.exit(0)
PY
do
  sleep 2
done

echo "Starting JupyterHub..."
exec jupyterhub -f /etc/jupyterhub/jupyterhub_config.py
