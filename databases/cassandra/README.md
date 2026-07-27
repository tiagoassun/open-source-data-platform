# Apache Cassandra

Banco wide-column **on-demand**, single-node neste compose. Consumo relevante de RAM e disco.

Documentação: https://cassandra.apache.org/doc/

## Papel na plataforma

- Fonte Cassandra/CQL para integrações
- DNS interno: `cassandra:9042`

## Acesso

| O que | Endereço |
|-------|----------|
| CQL (host) | `{IP_DO_SERVIDOR}:9042` |
| Na data-net | `cassandra:9042` |
| Autenticação | **Não configurada** neste stack |

## Pré-requisitos

1. Rede externa `data-net`
2. Pasta de dados:

```bash
mkdir -p /docker-data/cassandra
```

3. **Não exige `.env`** neste compose (cluster name fixo no YAML).

## Senha padrão / primeiro acesso

**Não há usuário nem senha neste stack.** Autenticação Cassandra **não esta habilitada**; qualquer cliente na rede que alcance `:9042` pode conectar sem credenciais.

| Situacao | O que fazer |
|----------|-------------|
| Uso interno na data-net | Aceitavel apenas com firewall restrito e rede confiavel |
| Produção exposta | **Não use assim**; habilite `PasswordAuthenticator` e roles antes de expor |

Não há "primeiro login" web. Conecte com `cqlsh`:

```bash
docker exec -it cassandra cqlsh
```

Se precisar de senha em produção, estenda o compose com variáveis de auth do Cassandra e documente no Kanboard antes de subir.

## Como subir

### Portainer (recomendado)

1. Stack `cassandra`, compose desta pasta
2. Deploy (sem variáveis obrigatorias)

### CLI

```bash
docker compose -f databases/cassandra/docker-compose.yml up -d
```

## Volumes

| Host | Uso |
|------|-----|
| `/docker-data/cassandra` | SSTables e dados |

## Produção

- Single-node **não e HA**; para cluster real configure seeds, DC, RF
- Habilite autenticação e TLS antes de qualquer exposição além da rede interna
- Pin de imagem; backup de snapshot
- Restrinja `:9042` no firewall
