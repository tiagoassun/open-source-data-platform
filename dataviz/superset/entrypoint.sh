#!/usr/bin/env bash
set -euo pipefail

CONFIG_DIR="${PYTHONPATH:-/app/pythonpath}"
mkdir -p "${CONFIG_DIR}"

python3 - <<'PY'
import os
from pathlib import Path

user = os.environ.get("POSTGRES_METADATA_USER", "admin")
password = os.environ["POSTGRES_METADATA_PASSWORD"]
secret = os.environ["SUPERSET_SECRET_KEY"]
uri = f"postgresql://{user}:{password}@postgres-metadata:5432/superset_db"
path = Path(os.environ.get("PYTHONPATH", "/app/pythonpath")) / "superset_config.py"
path.write_text(
    "\n".join(
        [
            f"SQLALCHEMY_DATABASE_URI = {uri!r}",
            f"SECRET_KEY = {secret!r}",
            "BABEL_DEFAULT_LOCALE = 'pt_BR'",
            "LANGUAGES = {'pt_BR': {'flag': 'br', 'name': 'Portuguese (Brazil)'}}",
            "WTF_CSRF_ENABLED = True",
            "SESSION_COOKIE_HTTPONLY = True",
            "SESSION_COOKIE_SAMESITE = 'Lax'",
            "",
        ]
    ),
    encoding="utf-8",
)
print(f"Wrote {path}")
PY

echo "Waiting for postgres-metadata..."
until python3 - <<'PY'
import os, sys
try:
    import psycopg2
    psycopg2.connect(
        host="postgres-metadata",
        port=5432,
        user=os.environ.get("POSTGRES_METADATA_USER", "admin"),
        password=os.environ["POSTGRES_METADATA_PASSWORD"],
        dbname="superset_db",
    ).close()
except Exception as exc:
    print(exc)
    sys.exit(1)
sys.exit(0)
PY
do
  sleep 2
done

superset db upgrade

if ! superset fab list-users 2>/dev/null | grep -q " ${SUPERSET_ADMIN_USERNAME:-admin} "; then
  superset fab create-admin \
    --username "${SUPERSET_ADMIN_USERNAME:-admin}" \
    --firstname Admin \
    --lastname User \
    --email "${SUPERSET_ADMIN_EMAIL}" \
    --password "${SUPERSET_ADMIN_PASSWORD}"
fi

superset init

exec /usr/bin/run-server.sh
