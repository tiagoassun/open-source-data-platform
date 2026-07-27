# PostgreSQL Columnar (Hydra)

Postgres com extensão **columnar** (imagem Hydra) para cargas analíticas e consultas agregadas. Separado do `postgres-metadata` de propósito: carga analitica não derruba metadados do Airflow, Hub ou Superset.

Documentação Hydra: https://github.com/hydradatabase/hydra

## Papel na plataforma

- Banco analítico / OLAP leve na plataforma
- Porta padrão Postgres no host (`5432`); conflito evitado porque metadata usa `5433`
- DNS interno: `postgres-columnar:5432`

## Acesso

| O que | Endereço |
|-------|----------|
| Host | `{IP_DO_SERVIDOR}:5432` |
| Na data-net | `postgres-columnar:5432` |
| Usuário | `POSTGRES_USER` (padrão `admin`) |
| Database | `POSTGRES_DB` (padrão `analytics`) |
| Senha | `POSTGRES_PASSWORD` no `.env` |

## Pré-requisitos

1. Rede externa `data-net`
2. Arquivo `.env` nesta pasta (copie de `.env.example`):

```env
POSTGRES_USER=admin
POSTGRES_PASSWORD=sua_senha_forte
POSTGRES_DB=analytics
```

3. Pasta de dados:

```bash
mkdir -p /docker-data/postgres-columnar
```

## Senha padrão / primeiro acesso

**Não há senha padrão de fábrica.** Usuário, senha e database inicial vêm do `.env` (`POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`).

| Situacao | O que usar |
|----------|------------|
| Volume novo | Credenciais do `.env` |
| Volume existente | Credenciais com que o cluster foi inicializado |

### Depois do primeiro acesso: troque a senha

1. Conecte com `psql` ou cliente SQL.
2. **Altere a senha** do usuário admin (`ALTER USER ...`).
3. Atualize o `.env` e conexões dos pipelines / Superset que apontam para este banco.

## Como subir

### Portainer (recomendado)

1. Stack `postgres-columnar`, compose desta pasta
2. Variaveis `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`
3. Deploy

### CLI

```bash
docker compose -f databases/postgres-columnar/docker-compose.yml up -d
```

## Volumes

| Host | Uso |
|------|-----|
| `/docker-data/postgres-columnar` | Dados do cluster |

## Produção

- Imagem pinada (`ghcr.io/hydradatabase/hydra:16`); não use `:latest`
- Backup de `/docker-data/postgres-columnar`
- Restrinja `:5432` no firewall se não precisar de acesso externo direto
- Monitore espaço em disco; cargas columnares podem crescer rápido
