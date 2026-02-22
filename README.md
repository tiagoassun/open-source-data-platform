# Open Source Data Platform

Uma plataforma de dados moderna e modular, construída inteiramente com ferramentas de código aberto e orquestrada via Docker. Este projeto serve como um laboratório completo para práticas de Engenharia de Dados.

## 🏗️ Arquitetura da Plataforma

A plataforma é dividida em camadas lógicas:

* **Management:** Portainer (Gestão de Containers)
* **Networking:** Cloudflare Tunnel
* **Storage:** MinIO (Object Storage S3)
* **Databases:** PostgreSQL (Metadata) e PostgreSQL + Hydra (Analytics)
* **Workspace:** JupyterHub
* **Orchestration:** Apache Airflow
* **Dataviz:** Apache Superset


---
---
---


## 🚀 Como Iniciar

### 1. Criar a Rede Unificada
Todas as ferramentas comunicam-se através da rede `data-net`.

```bash
chmod +x scripts/create_network.sh
./scripts/create_network.sh
```


---
---
---


### 2. Subir o Gerenciamento (Portainer)
O Portainer deve ser o primeiro container a ser levantado.

> **💡 Nota sobre o Deploy (Portainer vs Terminal):** > O Portainer é a base do nosso gerenciamento e, por isso, é o único container que obrigatoriamente deve ser iniciado via linha de comando. **Todos os próximos serviços desta plataforma** devem, idealmente, ser criados e gerenciados via interface gráfica do Portainer (na seção *Stacks*).

Estando na pasta raiz do repositório, execute o comando abaixo:

**Comandos:**
```bash
docker compose -f management/portainer/docker-compose.yml up -d
```

**Detalhes Técnicos:**
* **Acesso:** https://{IP_DO_SERVIDOR}:9443
* **Rede:** Utiliza a rede externa `data-net`
* **Volumes:** Dados persistidos em `/docker-data/portainer`


---
---
---


### 3. Expor a Plataforma (Cloudflare Tunnel)
Para acessar os serviços externamente com segurança (HTTPS) e sem necessidade de abrir portas no servidor, utilizamos o Cloudflare Tunnel.

> No entanto, para fins de reprodutibilidade e contingência, as instruções manuais via terminal sempre estarão documentadas abaixo.

**Pré-requisito:**
Crie um arquivo `.env` dentro da pasta `networking/cloudflare/` com o token gerado no painel do Cloudflare Zero Trust:
```env
CLOUDFLARE_TOKEN=seu_token_aqui
```

**🚀 Opção A: Deploy via Portainer (Recomendado)**
1. Acesse o Portainer em `https://{IP_DO_SERVIDOR}:9443` e vá em **Stacks** > **Add stack**.
2. Nomeie como `cloudflare-tunnel`.
3. Selecione o método (Upload, Repository, etc.) e aponte para o arquivo `networking/cloudflare/docker-compose.yml`.
4. Na seção *Environment variables*, adicione a variável `CLOUDFLARE_TOKEN` com o seu token.
5. Clique em **Deploy the stack**.

**💻 Opção B: Deploy Manual via Terminal**
Estando na pasta raiz do repositório, execute o comando abaixo:
```bash
docker compose -f networking/cloudflare/docker-compose.yml up -d
```

**Detalhes Técnicos:**
* **Rede:** Utiliza a rede externa `data-net` para enxergar os outros containers.
* **Volumes:** Dados e credenciais persistidos no host em `/docker-data/cloudflare`.
* **Restart:** Configurado como `unless-stopped` para respeitar interrupções manuais.


---
---
---


### 4. Armazenamento de Objetos / Object Storage (MinIO)
O MinIO atua como o nosso Object Storage, fornecendo armazenamento de alta performance compatível com o Amazon S3 para guardarmos nossos arquivos brutos, dados processados e backups.

**Pré-requisito:**
Crie um arquivo `.env` dentro da pasta `storage/minio/` com as credenciais de acesso de administrador desejadas:
```env
MINIO_ROOT_USER=admin
MINIO_ROOT_PASSWORD=sua_senha_forte_aqui
```

**🚀 Opção A: Deploy via Portainer (Recomendado)**
1. Acesse o Portainer e vá em **Stacks** > **Add stack**.
2. Nomeie como `minio`.
3. Selecione o método (Upload, Repository, etc.) e aponte para o arquivo `storage/minio/docker-compose.yml`.
4. Adicione as variáveis `MINIO_ROOT_USER` e `MINIO_ROOT_PASSWORD` na seção *Environment variables*.
5. Clique em **Deploy the stack**.

**💻 Opção B: Deploy Manual via Terminal**
Estando na pasta raiz do repositório, execute o comando abaixo:
```bash
docker compose -f storage/minio/docker-compose.yml up -d
```

**Detalhes Técnicos:**
* **Acesso UI (Console):** `http://{IP_DO_SERVIDOR}:9001`
* **Acesso API (S3):** `http://{IP_DO_SERVIDOR}:9000`
* **Rede:** Utiliza a rede externa `data-net`.
* **Volumes:** Dados persistidos no host em `/docker-data/minio`.
* **Restart:** Configurado como `unless-stopped`.