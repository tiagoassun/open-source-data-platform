# MariaDB LTS

Banco relacional MySQL-compatível **on-demand**. Porta no host `3307` para não conflitar com o stack MySQL (`3306`).

Documentação da imagem: https://hub.docker.com/_/mariadb

## Papel na plataforma

- Fonte MariaDB para integrações e testes de compatibilidade
- DNS interno: `mariadb:3306`

## Acesso

| O que | Endereço |
|-------|----------|
| Host | `{IP_DO_SERVIDOR}:3307` |
| Na data-net | `mariadb:3306` |
| Usuário root | `root` |
| Senha root | `MARIADB_ROOT_PASSWORD` no `.env` |
| Database inicial | `MARIADB_DATABASE` no `.env` |

## Pré-requisitos

1. Rede externa `data-net`
2. Arquivo `.env` nesta pasta:

```env
MARIADB_ROOT_PASSWORD=sua_senha_forte
MARIADB_DATABASE=nome_do_banco
```

3. Pasta de dados:

```bash
mkdir -p /docker-data/mariadb
```

## Senha padrão / primeiro acesso

**Não há senha padrão de fábrica.** A senha do `root` e `MARIADB_ROOT_PASSWORD` do `.env` no primeiro boot.

| Situacao | O que usar |
|----------|------------|
| Volume novo | `root` + senha do `.env` |
| Volume existente | Senha da inicialização original |

### Depois do primeiro login: troque a senha

1. Conecte como `root`.
2. **Altere a senha** e crie usuários de aplicação.
3. Atualize conexões e `.env` apos rotação.

## Como subir

### Portainer (recomendado)

1. Stack `mariadb`, compose desta pasta
2. Variaveis `MARIADB_ROOT_PASSWORD` e `MARIADB_DATABASE`
3. Deploy

### CLI

```bash
docker compose -f databases/mariadb/docker-compose.yml up -d
```

## Volumes

| Host | Uso |
|------|-----|
| `/docker-data/mariadb` | Dados do servidor |

## Produção

- Pin de imagem (`mariadb:lts`)
- Backup e restricao de `:3307` no firewall
- Usuarios dedicados por workload
