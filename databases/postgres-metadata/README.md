# PostgreSQL Metadata

Banco relacional central de **metadados** da plataforma. Não e o destino de cargas analíticas pesadas; guarda estado e configuração do Airflow, JupyterHub e Superset.

No **primeiro** boot com volume vazio, o script `init-databases.sh` cria automaticamente:

- `airflow_db`
- `jupyterhub_db`
- `superset_db`

Documentação da imagem: https://hub.docker.com/_/postgres

## Papel na plataforma

- Backend de metadados para Airflow, JupyterHub e Superset
- Separado do `postgres-columnar` (analytics) para isolar falhas e carga
- DNS interno: `postgres-metadata:5432`

## Acesso

| O que | Endereço |
|-------|----------|
| Host (debug / cliente externo) | `{IP_DO_SERVIDOR}:5433` |
| Dentro da data-net | `postgres-metadata:5432` |
| Usuário | Valor de `POSTGRES_METADATA_USER` (padrão `admin`) |
| Senha | Valor de `POSTGRES_METADATA_PASSWORD` no `.env` |

## Pré-requisitos

1. Rede externa `data-net`
2. Arquivo `.env` nesta pasta (copie de `.env.example`):

```env
POSTGRES_METADATA_USER=admin
POSTGRES_METADATA_PASSWORD=sua_senha_forte
POSTGRES_METADATA_DB=postgres
```

3. Pasta de dados:

```bash
mkdir -p /docker-data/postgres-metadata
```

4. Suba este stack **antes** de Airflow, JupyterHub e Superset.

## Senha padrão / primeiro acesso

**Não há senha padrão de fábrica.** Usuário e senha são definidos no `.env` via `POSTGRES_METADATA_USER` e `POSTGRES_METADATA_PASSWORD`.

| Situacao | O que usar |
|----------|------------|
| Primeiro start (volume vazio) | Credenciais do `.env`; databases de apps criadas pelo `init-databases.sh` |
| Volume já existente sem as DBs de app | Crie `airflow_db`, `jupyterhub_db`, `superset_db` manualmente ou reprovisione com backup |
| Esqueceu a senha | Procedimento oficial de reset do Postgres no host; não apague o volume sem backup |

### Depois do primeiro acesso: troque a senha

1. Conecte com as credenciais do `.env`.
2. **Altere a senha** do usuário admin (ou crie usuários dedicados por app com privilégio mínimo).
3. Atualize o `.env` e as stacks dependentes (Airflow, JupyterHub, Superset) com a nova senha.
4. Reinicie os serviços que usam este banco apos a rotação.

Apps web (Airflow UI, etc.) tem senhas **separadas**; troca-las não altera esta senha do Postgres.

## Como subir

### Portainer (recomendado)

1. Stack `postgres-metadata`, compose desta pasta
2. Variaveis `POSTGRES_METADATA_USER`, `POSTGRES_METADATA_PASSWORD`, `POSTGRES_METADATA_DB`
3. Deploy e aguarde healthcheck verde

### CLI

```bash
docker compose -f databases/postgres-metadata/docker-compose.yml up -d
```

Verificar databases criadas (primeiro boot):

```bash
docker exec -it postgres-metadata psql -U admin -d postgres -c '\l'
```

## Volumes

| Host | Uso |
|------|-----|
| `/docker-data/postgres-metadata` | Dados do cluster (WAL, tabelas) |
| `./init-databases.sh` | Montado em `/docker-entrypoint-initdb.d/` (roda uma vez no volume vazio) |

## Produção

- Imagem pinada (`postgres:16`); teste upgrades antes de aplicar
- Backup periódico de `/docker-data/postgres-metadata`
- Restrinja acesso a `:5433` (firewall / VPN); apps na `data-net` não precisam da porta publicada
- Use senhas fortes e usuários com escopo mínimo por aplicativo quando possivel
