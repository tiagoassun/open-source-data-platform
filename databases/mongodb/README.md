# MongoDB

Banco NoSQL orientado a documentos, **on-demand**.

Documentação da imagem: https://hub.docker.com/_/mongo

## Papel na plataforma

- Fonte documental para pipelines e Superset
- DNS interno: `mongodb:27017`

## Acesso

| O que | Endereço |
|-------|----------|
| Host | `{IP_DO_SERVIDOR}:27017` |
| Na data-net | `mongodb:27017` |
| Usuário root | Valor de `MONGO_USER` no `.env` |
| Senha root | Valor de `MONGO_PASSWORD` no `.env` |

## Pré-requisitos

1. Rede externa `data-net`
2. Arquivo `.env` nesta pasta:

```env
MONGO_USER=admin
MONGO_PASSWORD=sua_senha_forte
```

3. Pasta de dados:

```bash
mkdir -p /docker-data/mongodb
```

## Senha padrão / primeiro acesso

**Não há senha padrão de fábrica.** Usuário e senha root são `MONGO_USER` e `MONGO_PASSWORD` do `.env`, aplicados no primeiro boot via `MONGO_INITDB_ROOT_USERNAME` / `MONGO_INITDB_ROOT_PASSWORD`.

| Situacao | O que usar |
|----------|------------|
| Volume novo | Credenciais do `.env` |
| Volume existente | Credenciais da inicialização original |

### Depois do primeiro acesso: troque a senha

1. Autentique com o usuário root do `.env`.
2. **Altere a senha** (`db.changeUserPassword`) e crie usuários por database com roles minimas.
3. Atualize pipelines e `.env` apos rotação.

## Como subir

### Portainer (recomendado)

1. Stack `mongodb`, compose desta pasta
2. Variaveis `MONGO_USER` e `MONGO_PASSWORD`
3. Deploy

### CLI

```bash
docker compose -f databases/mongodb/docker-compose.yml up -d
```

## Volumes

| Host | Uso |
|------|-----|
| `/docker-data/mongodb` | Dados (`/data/db`) |

## Produção

- Fixe tag da imagem (evite `:latest` em produção)
- Backup e restricao de `:27017`
- Habilite TLS e auth fina se expor além da rede interna
