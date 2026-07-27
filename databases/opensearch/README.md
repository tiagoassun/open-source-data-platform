# OpenSearch

Motor de busca e analise distribuido (sucessor open source do Elasticsearch). Servico **on-demand**: suba quando precisar de indexacao ou busca full-text; consome RAM e exige ajuste no kernel do host.

Documentação oficial: https://opensearch.org/docs/

## Papel na plataforma

- Indice e busca para pipelines e integrações
- Seguranca habilitada (HTTPS + autenticação)
- DNS interno: `opensearch:9200` (HTTPS)

## Acesso

| O que | Endereço |
|-------|----------|
| API (host) | `https://{IP_DO_SERVIDOR}:9200` |
| Na data-net | `https://opensearch:9200` |
| Usuário | `admin` |
| Senha | Valor de `OPENSEARCH_PASSWORD` no `.env` |

Certificado HTTPS e **autoassinado** por padrão: clientes devem confiar ou usar `-k` / equivalente.

## Pré-requisitos

1. Rede externa `data-net`
2. **Host Linux** - aumentar `vm.max_map_count` (obrigatório):

```bash
sudo sysctl -w vm.max_map_count=262144
```

Para persistir apos reboot, inclua em `/etc/sysctl.conf` ou arquivo em `/etc/sysctl.d/`.

3. Arquivo `.env` nesta pasta (copie de `.env.example`):

```env
OPENSEARCH_PASSWORD=ChangeMe_OpenSearch1!
OPENSEARCH_JAVA_OPTS=-Xms1g -Xmx1g
```

4. Pasta de dados:

```bash
mkdir -p /docker-data/opensearch
```

## Senha padrão / primeiro acesso

**Não há senha padrão de fábrica genérica neste projeto.** Usuário fixo `admin`; senha inicial e **exatamente** `OPENSEARCH_PASSWORD` do `.env`, definida no primeiro boot via `OPENSEARCH_INITIAL_ADMIN_PASSWORD`.

Requisitos de complexidade da senha (OpenSearch Security):

- Minimo 8 caracteres
- Pelo menos uma maiúscula, uma minúscula, um dígito e um caractere especial
- Não pode ser senhas comuns da lista de bloqueio do OpenSearch

| Situacao | O que usar |
|----------|------------|
| Volume novo | `admin` + senha do `.env` (complexa) |
| Volume existente | Senha definida no primeiro boot; mudar só o `.env` não altera automaticamente |

### Depois do primeiro login: troque a senha

1. Acesse a API ou Dashboards (se configurado) com `admin` e a senha do `.env`.
2. **Altere a senha** do admin pelo mecanismo de segurança do OpenSearch ou reprovisione com procedimento documentado.
3. Atualize o `.env` e reinicie a stack se necessario.
4. Não reutilize a senha de exemplo do `.env.example` em produção.

## Como subir

### Portainer (recomendado)

1. Stack `opensearch`, compose desta pasta
2. Variavel `OPENSEARCH_PASSWORD` (e opcionalmente `OPENSEARCH_JAVA_OPTS`)
3. Deploy; primeiro boot pode levar vários minutos

### CLI

```bash
docker compose -f databases/opensearch/docker-compose.yml up -d
```

Teste rápido:

```bash
curl -sk -u admin:SUA_SENHA https://localhost:9200/_cluster/health
```

## Volumes

| Host | Uso |
|------|-----|
| `/docker-data/opensearch` | Indices e dados do cluster |

## Produção

- Ajuste `OPENSEARCH_JAVA_OPTS` conforme RAM disponivel
- Imagem pinada (`2.19.1`); planeje upgrades
- Não exponha `:9200` na internet sem TLS na borda e controle de acesso
- Backup de índices e volume; cluster single-node não e HA
