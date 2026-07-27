# Open Source Data Platform

Plataforma de dados modular com ferramentas open source, orquestrada via Docker/Portainer, pensada para **operar como produção** (segredos, tags pinadas, healthchecks, init idempotente) em servidores Linux.

## Arquitetura

* **Management:** [Portainer](management/portainer/README.md) (gestão de containers/stacks)
* **Networking:** [Cloudflare Tunnel](networking/cloudflare/README.md)
* **Storage:** [MinIO](storage/minio/README.md) (Object Storage S3)
* **Databases (core):** [PostgreSQL Metadata](databases/postgres-metadata/README.md), [PostgreSQL Columnar / Hydra](databases/postgres-columnar/README.md)
* **Databases (on-demand):** [MySQL](databases/mysql/README.md), [MariaDB](databases/mariadb/README.md), [MongoDB](databases/mongodb/README.md), [Cassandra](databases/cassandra/README.md), [OpenSearch](databases/opensearch/README.md)
* **Workspace:** [JupyterHub](workspace/jupyterhub/README.md)
* **Orchestration:** [Apache Airflow](orchestration/airflow/README.md)
* **Dataviz:** [Apache Superset](dataviz/superset/README.md)

## Sequência de leitura (entender o ambiente)

Depois do mapa acima, leia nesta ordem. Cada passo depende do anterior no desenho da plataforma.

1. **Postura de produção** e **Como iniciar** (seções abaixo neste README) - rede `data-net`, `/docker-data` e regras gerais.
2. [`management/portainer/README.md`](management/portainer/README.md) - como tudo é operado (Stacks, socket Docker, primeiro admin).
3. [`databases/postgres-metadata/README.md`](databases/postgres-metadata/README.md) - banco de metadados (`airflow_db`, `jupyterhub_db`, `superset_db`); base do core.
4. [`storage/minio/README.md`](storage/minio/README.md) - object storage S3 usado por pipelines e apps.
5. [`orchestration/airflow/README.md`](orchestration/airflow/README.md) - orquestração de DAGs (depende do metadata + MinIO/Docker).
6. [`workspace/jupyterhub/README.md`](workspace/jupyterhub/README.md) - workspace interativo (depende do metadata + Docker).
7. [`dataviz/superset/README.md`](dataviz/superset/README.md) - BI sobre as fontes na `data-net` (depende do metadata).
8. [`databases/postgres-columnar/README.md`](databases/postgres-columnar/README.md) - Postgres analítico (Hydra), separado do metadata de propósito.
9. **Bancos on-demand** (só o que for usar): [MySQL](databases/mysql/README.md), [MariaDB](databases/mariadb/README.md), [MongoDB](databases/mongodb/README.md), [Cassandra](databases/cassandra/README.md), [OpenSearch](databases/opensearch/README.md).
10. [`networking/cloudflare/README.md`](networking/cloudflare/README.md) - exposição pública/Zero Trust **depois** do core interno estável.

Dica: em cada pasta, leia o `README.md` antes do `docker-compose.yml`. O compose tem só comentários curtos; o detalhe (senhas, portas, bootstrap) está no README do serviço.

## Postura de produção (ler antes de subir)

1. **Rede:** `data-net` (externa) - todos os stacks usam a mesma rede.
2. **Dados no host:** tudo em `/docker-data/{servico}` (persistente).
3. **Segredos:** cada pasta tem `.env.example`. Copie para `.env` (gitignored).
4. **Portainer primeiro via terminal;** o restante como **Stacks** no Portainer.
5. **Imagens custom** (Airflow / JupyterHub hub / Superset): faça `docker compose build` no host **antes** do stack no Portainer (Portainer sobe pela `image:`, sem `build`).
6. **Docker socket:** use `group_add: DOCKER_GID` (GID do grupo `docker` no host). Não use `chmod 666` no socket.
7. **Airflow volumes:** dono UID `50000` -> `chown -R 50000:0 /docker-data/airflow`.
8. **Metadados:** `postgres-metadata` cria `airflow_db`, `jupyterhub_db`, `superset_db` no **primeiro** boot (`init-databases.sh`). Se o volume já existir sem essas DBs, crie manualmente.
9. **Documentação:** overview na raiz; detalhes de cada ferramenta no `README.md` da pasta do serviço. Compose com comentários curtos apontando para o README.
10. **Scripts shell:** `.gitattributes` força LF (`*.sh`). CRLF quebra entrypoints no Linux.
11. **Texto:** pt-BR com acentos; pontuação ASCII (`-`, `...`, `->`).

Ordem sugerida de stacks: `postgres-metadata` -> `minio` -> `airflow` -> `jupyterhub` -> `superset` -> (opcionais) Cloudflare, Hydra, OpenSearch, demais DBs.

## Como iniciar

### 1. Criar a rede unificada

Todas as ferramentas comunicam-se pela rede externa `data-net`.

```bash
chmod +x scripts/create_network.sh
./scripts/create_network.sh
```

### 2. Subir o gerenciamento (Portainer)

O Portainer é o primeiro serviço a levantar e o **único** que sobe via terminal. Os demais sobem como Stacks na UI.

Documentação completa: [`management/portainer/README.md`](management/portainer/README.md)

```bash
docker compose -f management/portainer/docker-compose.yml up -d
```

* **Acesso:** `https://{IP_DO_SERVIDOR}:9443`
* **Dados:** `/docker-data/portainer/`

### 3. Demais serviços (Stacks no Portainer)

Deploy detalhado, senhas, volumes e notas de produção estão no **README de cada pasta**. Resumo com links:

| Área | Serviço | README |
|------|---------|--------|
| Networking | Cloudflare Tunnel | [networking/cloudflare/README.md](networking/cloudflare/README.md) |
| Storage | MinIO | [storage/minio/README.md](storage/minio/README.md) |
| DB core | PostgreSQL Metadata | [databases/postgres-metadata/README.md](databases/postgres-metadata/README.md) |
| DB core | PostgreSQL Columnar (Hydra) | [databases/postgres-columnar/README.md](databases/postgres-columnar/README.md) |
| DB on-demand | MySQL | [databases/mysql/README.md](databases/mysql/README.md) |
| DB on-demand | MariaDB | [databases/mariadb/README.md](databases/mariadb/README.md) |
| DB on-demand | MongoDB | [databases/mongodb/README.md](databases/mongodb/README.md) |
| DB on-demand | Cassandra | [databases/cassandra/README.md](databases/cassandra/README.md) |
| DB on-demand | OpenSearch | [databases/opensearch/README.md](databases/opensearch/README.md) |
| Orchestration | Apache Airflow | [orchestration/airflow/README.md](orchestration/airflow/README.md) |
| Workspace | JupyterHub | [workspace/jupyterhub/README.md](workspace/jupyterhub/README.md) |
| Dataviz | Apache Superset | [dataviz/superset/README.md](dataviz/superset/README.md) |

Padrão de deploy (todos exceto Portainer):

1. Copie `.env.example` para `.env` na pasta do serviço (quando existir).
2. No Portainer: **Stacks** -> **Add stack** -> aponte para o `docker-compose.yml` da pasta.
3. Injete variáveis de ambiente conforme o README do serviço.
4. Para Airflow, JupyterHub e Superset: **build da imagem no host antes** do deploy da stack.

Alternativa CLI (exemplo):

```bash
docker compose -f <caminho>/docker-compose.yml up -d
```

Consulte o README do serviço para pré-requisitos, ordem de subida e bootstrap de senhas.
