# MinIO

Object Storage compatível com a API **S3**. Guarda arquivos brutos, dumps, artefatos de pipeline, backups e dados intermediários. Outros serviços na `data-net` usam o endpoint interno `http://minio:9000`.

Documentação oficial: https://min.io/docs/minio/container/index.html

## Papel na plataforma

- Armazenamento de objetos compartilhado (S3-compatível)
- Integracao com Airflow, Superset e pipelines via API ou console
- Persistência em `/docker-data/minio`

## Acesso

| O que | Endereço |
|-------|----------|
| API S3 | `http://{IP_DO_SERVIDOR}:9000` |
| Console web | `http://{IP_DO_SERVIDOR}:9001` |
| Na data-net | `http://minio:9000` |

## Pré-requisitos

1. Rede externa `data-net`
2. Arquivo `.env` nesta pasta (copie de `.env.example`):

```env
MINIO_ROOT_USER=admin
MINIO_ROOT_PASSWORD=sua_senha_forte_aqui
```

3. Pasta de dados:

```bash
mkdir -p /docker-data/minio
```

Requisitos tipicos da senha root: mínimo 8 caracteres (use senha longa em produção).

## Senha padrão / primeiro acesso

**Não há senha padrão de fábrica neste projeto.** O usuário e a senha root são **exatamente** os valores de `MINIO_ROOT_USER` e `MINIO_ROOT_PASSWORD` do `.env` (ou variáveis da stack) no **primeiro** start com volume vazio.

| Situacao | O que usar |
|----------|------------|
| Volume `/docker-data/minio` novo | User e senha definidos no `.env` |
| `minioadmin` / `minioadmin` (default de tutoriais genericos) | **Não** se aplica aqui, salvo se você colocou isso no `.env` |
| Volume já existente | Credenciais com que o volume foi inicializado; alterar só o `.env` **não** troca a senha automaticamente |

### Depois do primeiro login: troque a senha

1. Entre no Console (`:9001`) com o root do `.env`.
2. Crie usuários ou Access Keys com política mínima para Airflow e demais apps.
3. **Altere a senha do root** (ou pare de usar root no dia a dia) e atualize o cofre de segredos / `.env` se ainda precisar do root.
4. Não deixe senha "provisória" em produção.

## Como subir

### Portainer (recomendado)

1. Stack `minio`, compose desta pasta
2. Variaveis `MINIO_ROOT_USER` e `MINIO_ROOT_PASSWORD`
3. Deploy

### CLI

```bash
docker compose -f storage/minio/docker-compose.yml up -d
```

## Volumes

| Host | Uso |
|------|-----|
| `/docker-data/minio` | Buckets e objetos |

## Produção

- Prefira tag `RELEASE.YYYY-MM-DD...` em vez de `:latest`
- Não exponha `:9000` / `:9001` na internet sem TLS e controle de acesso (Cloudflare Tunnel, VPN, firewall)
- Backup periódico de `/docker-data/minio`
- Use políticas IAM / buckets dedicados por workload
