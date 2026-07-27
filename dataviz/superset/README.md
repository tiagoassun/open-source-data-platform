# Apache Superset

Business Intelligence (BI) conectado as fontes na `data-net`. Imagem custom com drivers Postgres, MySQL/MariaDB, MongoDB e S3/MinIO. Metadados em `postgres-metadata` / `superset_db`.

Documentação oficial: https://superset.apache.org/docs/intro

## Papel na plataforma

- Dashboards e exploracao SQL sobre bancos da plataforma
- Admin bootstrap idempotente no entrypoint
- Config gerada em `/docker-data/superset/pythonpath`

## Acesso

| O que | Endereço |
|-------|----------|
| UI web | `http://{IP_DO_SERVIDOR}:8088` |
| Na data-net | `http://superset:8088` |
| Usuário admin | `SUPERSET_ADMIN_USERNAME` (padrão `admin`) |
| Senha admin | `SUPERSET_ADMIN_PASSWORD` no `.env` |

## Pré-requisitos

1. Stack `postgres-metadata` saudável (`superset_db` criada no primeiro boot)
2. Rede externa `data-net`
3. Arquivo `.env` (copie de `.env.example`):

```env
POSTGRES_METADATA_USER=admin
POSTGRES_METADATA_PASSWORD=sua_senha_metadata
SUPERSET_SECRET_KEY=sua_chave_secreta_longa
SUPERSET_ADMIN_USERNAME=admin
SUPERSET_ADMIN_EMAIL=admin@example.com
SUPERSET_ADMIN_PASSWORD=sua_senha_superset
```

Gerar `SUPERSET_SECRET_KEY`:

```bash
openssl rand -base64 42
```

4. **Build da imagem** antes do stack no Portainer:

```bash
docker compose -f dataviz/superset/docker-compose.yml build
```

5. Pastas:

```bash
mkdir -p /docker-data/superset/pythonpath
```

## Senha padrão / primeiro acesso

**Não há senha padrão de fábrica.** O entrypoint cria o admin apenas se o usuário ainda não existir, usando:

- `SUPERSET_ADMIN_USERNAME` (padrão `admin`)
- `SUPERSET_ADMIN_EMAIL`
- `SUPERSET_ADMIN_PASSWORD` do `.env`

| Mito | Realidade |
|------|-----------|
| `admin` / `admin` | Não existe salvo se você definiu no `.env` |
| Senha no compose | Não ha; vem do `.env` / variáveis da stack |

`SUPERSET_SECRET_KEY` e obrigatória para sessoes e assinaturas em produção.

### Depois do primeiro login: troque a senha

1. Entre na UI com credenciais do `.env`.
2. **Altere a senha** do admin (Settings / Security / List Users ou fluxo de perfil).
3. O entrypoint **não** redefine senha de usuário existente ao reiniciar.
4. Crie usuários com roles minimas (Gamma/Analyst) para consumo de dashboards.

## Como subir

### Portainer (recomendado)

1. Build no host (ver pré-requisitos)
2. Stack `superset`, compose desta pasta
3. Variaveis do `.env.example`
4. Deploy; primeiro boot pode levar alguns minutos (`db upgrade`)

### CLI

```bash
docker compose -f dataviz/superset/docker-compose.yml build
docker compose -f dataviz/superset/docker-compose.yml up -d
```

## Volumes

| Host | Uso |
|------|-----|
| `/docker-data/superset` | Home do Superset (cache, uploads) |
| `/docker-data/superset/pythonpath` | `superset_config.py` gerado |

## Produção

- Imagem pinada `tiagoassun/superset:4.1.1`; sem `--reload` / debugger
- Não exponha `:8088` sem TLS e controle de acesso
- Rotacione `SUPERSET_SECRET_KEY` com plano (invalida sessoes)
- Conecte fontes de dados com credenciais dedicadas, não root dos bancos
