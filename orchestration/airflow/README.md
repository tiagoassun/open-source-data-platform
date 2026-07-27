# Apache Airflow

Orquestração de pipelines de dados com **LocalExecutor**: webserver (UI), scheduler (execução de tasks) e job de init (migracao DB + admin idempotente). Imagem custom com providers Postgres, Amazon (S3/MinIO) e Docker.

Documentação oficial: https://airflow.apache.org/docs/

## Papel na plataforma

- Agenda e monitora DAGs
- Metadados em `postgres-metadata` / database `airflow_db`
- **DockerOperator** via socket do host (containers efemeros na `data-net`)
- GitOps: DAG `_sync_git_all_repos` sincroniza repos definidos em `repos.json`

## Acesso

| O que | Endereço |
|-------|----------|
| UI web | `http://{IP_DO_SERVIDOR}:8080` |
| Na data-net | `http://airflow-webserver:8080` |
| Usuário admin | `AIRFLOW_ADMIN_USERNAME` (padrão `admin`) |
| Senha admin | `AIRFLOW_ADMIN_PASSWORD` no `.env` |

## Pré-requisitos

1. Stack `postgres-metadata` saudável (`airflow_db` criada no primeiro boot)
2. Rede externa `data-net`
3. Arquivo `.env` nesta pasta (copie de `.env.example`):

```env
POSTGRES_METADATA_USER=admin
POSTGRES_METADATA_PASSWORD=sua_senha_metadata
AIRFLOW__CORE__FERNET_KEY=sua_chave_fernet
AIRFLOW_ADMIN_USERNAME=admin
AIRFLOW_ADMIN_EMAIL=admin@example.com
AIRFLOW_ADMIN_PASSWORD=sua_senha_airflow
GIT_USER=
GIT_TOKEN=
DOCKER_GID=983
```

Gerar `AIRFLOW__CORE__FERNET_KEY`:

```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

Descobrir `DOCKER_GID` no host:

```bash
getent group docker | cut -d: -f3
```

4. **Build da imagem** (obrigatório antes do stack no Portainer):

```bash
docker compose -f orchestration/airflow/docker-compose.yml build
```

5. Pastas no host com dono UID `50000`:

```bash
sudo mkdir -p /docker-data/airflow/{dags,logs,plugins}
sudo chown -R 50000:0 /docker-data/airflow
```

6. Coloque DAGs em `/docker-data/airflow/dags` (inclui `_sync_git_all_repos` do repositorio).

## Senha padrão / primeiro acesso

**Não há senha padrão de fábrica.** O usuário admin e criado pelo container `airflow-init` apenas se ainda não existir, usando:

- `AIRFLOW_ADMIN_USERNAME` (padrão `admin`)
- `AIRFLOW_ADMIN_EMAIL`
- `AIRFLOW_ADMIN_PASSWORD` do `.env`

| Mito | Realidade |
|------|-----------|
| `admin` / `admin` | Não existe salvo se você definiu isso no `.env` |
| Senha escondida no compose | Não ha; vem do `.env` / variáveis da stack |

`AIRFLOW__CORE__FERNET_KEY` e **obrigatória** em produção (cifra connections/variables); sem ela o stack não deve subir em ambiente real.

### Depois do primeiro login: troque a senha

1. Entre na UI com as credenciais do `.env`.
2. **Altere a senha** do admin (menu do usuário / Security).
3. Atualize o `.env` se quiser manter alinhado (o init **não** redefine senha de usuário existente).
4. Crie usuários RBAC com roles minimas para operação diaria.

## Como subir

### Portainer (recomendado)

1. **Build no host primeiro** (ver pré-requisitos)
2. Stack `airflow`, compose desta pasta
3. Preencha todas as variáveis do `.env.example`
4. Deploy; aguarde `airflow-init` completar e webserver healthy

### CLI

```bash
docker compose -f orchestration/airflow/docker-compose.yml build
docker compose -f orchestration/airflow/docker-compose.yml up -d
```

Acompanhar init:

```bash
docker logs airflow-init
docker compose -f orchestration/airflow/docker-compose.yml ps
```

## Volumes e componentes

| Host / recurso | Uso |
|----------------|-----|
| `/docker-data/airflow/dags` | DAGs |
| `/docker-data/airflow/logs` | Logs de tasks |
| `/docker-data/airflow/plugins` | Plugins |
| `/var/run/docker.sock` | DockerOperator |
| `airflow-init` | Migra DB + cria admin (sai apos sucesso) |
| `airflow-webserver` | UI `:8080` |
| `airflow-scheduler` | LocalExecutor (tasks no scheduler) |

## Produção

- `group_add: DOCKER_GID` em vez de `chmod 666` no socket
- Pin da imagem `tiagoassun/airflow:2.10.5`; rebuild ao mudar Dockerfile
- Não exponha `:8080` sem TLS e controle de acesso
- Rotacione `FERNET_KEY` apenas com plano de migracao (quebra secrets existentes)
- `GIT_TOKEN` apenas via env; URLs em `repos.json` sem credenciais embarcadas

## DockerOperator (referencia)

Tasks podem usar `tiagoassun/mega-jupyter:latest` na `data-net` com mounts em `/docker-data/airflow/dags`. Ver DAGs de exemplo no repositorio.
