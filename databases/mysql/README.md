# MySQL 8

Banco relacional **on-demand**. Suba quando um pipeline ou integração precisar de fonte MySQL; não faz parte do core mínimo da plataforma.

Documentação da imagem: https://hub.docker.com/_/mysql

## Papel na plataforma

- Simular ou conectar sistemas OLTP MySQL
- DNS interno: `mysql:3306`

## Acesso

| O que | Endereço |
|-------|----------|
| Host | `{IP_DO_SERVIDOR}:3306` |
| Na data-net | `mysql:3306` |
| Usuário root | `root` |
| Senha root | `MYSQL_ROOT_PASSWORD` no `.env` |
| Database inicial | `MYSQL_DATABASE` no `.env` |

## Pré-requisitos

1. Rede externa `data-net`
2. Arquivo `.env` nesta pasta:

```env
MYSQL_ROOT_PASSWORD=sua_senha_forte
MYSQL_DATABASE=nome_do_banco
```

3. Pasta de dados:

```bash
mkdir -p /docker-data/mysql
```

## Senha padrão / primeiro acesso

**Não há senha padrão de fábrica.** A senha do usuário `root` e o valor de `MYSQL_ROOT_PASSWORD` no `.env` (ou variavel da stack) no primeiro boot.

| Situacao | O que usar |
|----------|------------|
| Volume novo | `root` + senha do `.env` |
| Volume existente | Senha com que o volume foi inicializado |

### Depois do primeiro acesso: troque a senha

1. Conecte como `root`.
2. **Altere a senha** (`ALTER USER 'root'@'%' ...`) e crie usuários de aplicação com privilégio mínimo.
3. Atualize pipelines e o `.env` se rotacionar credenciais.

## Como subir

### Portainer (recomendado)

1. Stack `mysql`, compose desta pasta
2. Variaveis `MYSQL_ROOT_PASSWORD` e `MYSQL_DATABASE`
3. Deploy

### CLI

```bash
docker compose -f databases/mysql/docker-compose.yml up -d
```

## Volumes

| Host | Uso |
|------|-----|
| `/docker-data/mysql` | Dados InnoDB |

## Produção

- Imagem pinada (`mysql:8.0`)
- Backup antes de upgrades
- Restrinja `:3306` no firewall
- Não use root em pipelines; crie usuário dedicado
