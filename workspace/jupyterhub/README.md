# JupyterHub

Hub multi-usuário que **spawna** containers Docker isolados por usuário (DockerSpawner). Autenticação via **NativeAuthenticator**; signup público desligado. Metadados de usuários em `postgres-metadata` / `jupyterhub_db`.

Documentação: https://jupyterhub.readthedocs.io/

## Papel na plataforma

- Workspace interativo por usuário (container `tiagoassun/mega-jupyter:latest` por padrão)
- Persistência em `/docker-data/jupyterhub/users/{username}`
- Proxy na porta `8888` do host
- Acesso ao Docker do host para spawn (via `DOCKER_GID`)

## Acesso

| O que | Endereço |
|-------|----------|
| UI / login | `http://{IP_DO_SERVIDOR}:8888` |
| Na data-net | `http://jupyterhub:8000` (proxy interno) |

## Pré-requisitos

1. Stack `postgres-metadata` saudável (`jupyterhub_db` criada no primeiro boot)
2. Rede externa `data-net`
3. Arquivo `.env` (copie de `.env.example`):

```env
POSTGRES_METADATA_USER=admin
POSTGRES_METADATA_PASSWORD=sua_senha_metadata
JUPYTERHUB_CRYPT_KEY=sua_chave_hex_64
DOCKER_GID=983
```

Gerar `JUPYTERHUB_CRYPT_KEY`:

```bash
openssl rand -hex 32
```

4. **Build das imagens** no host (não use build pesado pelo Portainer):

```bash
docker build -t tiagoassun/mega-jupyter:latest -f workspace/jupyterhub/Dockerfile workspace/jupyterhub
docker compose -f workspace/jupyterhub/docker-compose.yml build
```

5. Pastas:

```bash
mkdir -p /docker-data/jupyterhub/users
```

## Senha padrão / primeiro acesso

**Não há senha padrão e não ha usuário criado automaticamente.** Configuração em `jupyterhub_config.py`:

- `NativeAuthenticator.open_signup = False` (sem auto-cadastro)
- `admin_users = {"admin"}` (usuário `admin` e administrador do Hub quando existir)

Você precisa **bootstrap** do primeiro usuário antes do uso normal.

### Opcao A: signup temporario (recomendado para primeiro admin)

1. Edite `jupyterhub_config.py` e defina `c.NativeAuthenticator.open_signup = True`.
2. Rebuild a imagem do hub e reinicie o stack.
3. Acesse `:8888`, cadastre o usuário `admin` com senha forte.
4. Volte `open_signup = False`, rebuild e reinicie.
5. **Altere a senha** do `admin` na UI se a inicial foi provisória.

### Opcao B: ferramentas admin / CLI

Com o Hub no ar, use comandos oficiais do JupyterHub para criar usuário (ex.: `jupyterhub spawn` / API admin / `nativeauthenticator` admin tools conforme versao). Defina senha no fluxo de criacao.

### Depois do primeiro login: troque a senha

1. Cada usuário deve usar senha forte única.
2. Admin cria demais usuários pela UI (Authorize and manage users) com signup fechado.
3. **Troque a senha** periodicamente e apos compartilhamento inadvertido.

Usuarios comuns **não** herdam senha do Postgres metadata; são contas separadas no Hub.

## Como subir

### Portainer (recomendado)

1. Build das imagens no host (ver pré-requisitos)
2. Stack `jupyterhub`, compose desta pasta
3. Variaveis do `.env.example`
4. Deploy

### CLI

```bash
docker compose -f workspace/jupyterhub/docker-compose.yml up -d
```

## Volumes e arquitetura

| Host | Uso |
|------|-----|
| `/docker-data/jupyterhub` | Estado do Hub |
| `/docker-data/jupyterhub/users/{username}` | Home persistente do notebook |
| `/var/run/docker.sock` | DockerSpawner |

Arquivos principais nesta pasta:

- `Dockerfile` - imagem do notebook spawnado
- `Dockerfile.hub` - imagem do Hub
- `jupyterhub_config.py` - auth, rede, spawner, lifestyle hook

### Comportamento do workspace spawnado

- Container do usuário e **efemero** (recriado no login); arquivos fora de `/home/jovyan/work` (mapeado para `users/{username}`) se perdem
- Hook inicial cria pastas `git/` e `_exemplos/` com notebooks de demonstração

## Produção

- `group_add: DOCKER_GID`; não relaxe permissoes do socket
- Restrinja `:8888` (Tunnel / VPN)
- Build da imagem `mega-jupyter` e demorado; pin tags
- Admin `admin` deve ser conta controlada; desligue signup público apos bootstrap
