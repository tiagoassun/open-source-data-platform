FROM apache/superset:4.1.1

USER root
RUN pip install --no-cache-dir \
        psycopg2-binary \
        pymysql \
        pymongo \
        "boto3==1.35.36" \
        "s3fs==2024.9.0"

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/bin/bash", "/entrypoint.sh"]
