#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    SELECT 'CREATE DATABASE airflow_db'
    WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'airflow_db')\gexec

    SELECT 'CREATE DATABASE jupyterhub_db'
    WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'jupyterhub_db')\gexec

    SELECT 'CREATE DATABASE superset_db'
    WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'superset_db')\gexec
EOSQL
