FROM apache/airflow:2.10.5

USER root
RUN apt-get update \
    && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/*

USER airflow
RUN pip install --no-cache-dir \
    "apache-airflow-providers-postgres==5.14.0" \
    "apache-airflow-providers-amazon==9.2.0" \
    "apache-airflow-providers-docker==3.14.0"
