# Cloudflare Tunnel

Expõe serviços da plataforma na internet com HTTPS, **sem abrir portas** no firewall ou roteador. O `cloudflared` abre um tunel de **saida** até a Cloudflare; você mapeia hostnames (Zero Trust) para containers na `data-net` (ex.: `http://airflow-webserver:8080`).

Documentação oficial: https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/

## Papel na plataforma

- Entrada pública (ou privada via Zero Trust) para Airflow, JupyterHub, Superset, MinIO, etc.
- TLS na borda da Cloudflare
- Os containers continuam apenas na rede interna `data-net`

## Acesso

| O que | Endereço |
|-------|----------|
| Tunel | Sem UI propria; trafego entra pelos hostnames configurados no painel Cloudflare |
| Apps atras do tunel | URLs que você publicar (ex.: `https://airflow.seudominio.com`) |

## Pré-requisitos

1. Conta Cloudflare + dominio no Zero Trust
2. Tunel criado no painel; copie o **token** do tunel
3. Rede externa `data-net` (ver README da raiz e `scripts/create_network.sh`)
4. Portainer no ar (recomendado) ou Docker Compose no host
5. Arquivo `.env` nesta pasta (copie de `.env.example`):

```env
CLOUDFLARE_TOKEN=seu_token_do_tunnel
```

6. Pasta de dados no host:

```bash
mkdir -p /docker-data/cloudflare
```

## Senha padrão / primeiro acesso

**Não há usuário ou senha neste container.** A autenticação do tunel e o **token** (`CLOUDFLARE_TOKEN` no `.env` ou variavel da stack). Acesso aos aplicativos publicados por tras do tunel usa as credenciais de **cada app** (Airflow, Superset, etc.), não do cloudflared.

- O token e **segredo**: não commitar no Git
- Se o token vazar: revogue ou rotacione no painel Cloudflare e atualize o `.env` / variáveis da stack
- Configure políticas Zero Trust (IdP, MFA) na Cloudflare para proteger URLs publicadas

Não há senha de usuário para "trocar" no cloudflared; trate a rotação do token como equivalente a troca de credencial de serviço.

## Como subir

### Portainer (recomendado)

1. **Stacks** -> **Add stack** -> nome `cloudflare-tunnel`
2. Aponte para `networking/cloudflare/docker-compose.yml` (repositorio ou upload)
3. Em *Environment variables*, defina `CLOUDFLARE_TOKEN`
4. **Deploy the stack**

### CLI

```bash
docker compose -f networking/cloudflare/docker-compose.yml up -d
```

Acompanhar:

```bash
docker compose -f networking/cloudflare/docker-compose.yml ps
docker logs -f cloudflared-tunnel
```

## Volumes

| Host | Container | Uso |
|------|-----------|-----|
| `/docker-data/cloudflare` | `/home/nonroot/.cloudflared` | Estado e credenciais locais do cloudflared, se aplicavel |

## Rede

- `data-net` (externa): resolve nomes como `airflow-webserver`, `superset`, `minio`

## Produção

- Prefira políticas Zero Trust (login corporativo) em vez de expor apps apenas com senha fraca
- Monitore o tunel no painel Cloudflare
- Fixe a imagem (`:latest` muda comportamento); use digest ou tag estavel quando estabilizar
- Não exponha serviços sensiveis sem camada extra de autenticação na borda
