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


## 🚀 Como Iniciar

### 1. Criar a Rede Unificada
Todas as ferramentas comunicam-se através da rede `data-net`.

```bash
chmod +x scripts/create_network.sh
./scripts/create_network.sh
```


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
* **Volumes:** Dados persistidos em `/docker-data/portainer/`


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
* **Volumes:** Dados e credenciais persistidos no host em `/docker-data/cloudflare/`.
* **Restart:** Configurado como `unless-stopped` para respeitar interrupções manuais.


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
* **Volumes:** Dados persistidos no host em `/docker-data/minio/`.
* **Restart:** Configurado como `unless-stopped`.


---
---


### 5. Bancos de Dados (Relacionais, NoSQL e Search)
A arquitetura contempla um ecossistema completo para suportar metadados, consultas analíticas (OLAP) e simular um ambiente de dados do mundo real com diversas fontes de ingestão para o laboratório.

---

#### 5.1. PostgreSQL Colunar (Analytics / Hydra)
Banco de dados colunar (utilizando a engine Hydra) focado em alta performance para análises de dados e agregações.
* **Pré-requisito:** Arquivo `.env` em `databases/postgres-columnar/` com `POSTGRES_USER`, `POSTGRES_PASSWORD` e `POSTGRES_DB`.

**🚀 Opção A: Deploy via Portainer (Recomendado)**
1. Crie uma stack nomeada `postgres-columnar`.
2. Aponte para o arquivo `databases/postgres-columnar/docker-compose.yml`.
3. Preencha as variáveis de ambiente e faça o deploy.

**💻 Opção B: Deploy Manual via Terminal**
```bash
docker compose -f databases/postgres-columnar/docker-compose.yml up -d
```
* **Acesso Externo na Mesma Rede:** `{IP_DO_SERVIDOR}:5432` 
* **Volumes:** `/docker-data/postgres-columnar/`

---

#### 5.2. PostgreSQL (Metadata)
Responsável por armazenar o estado e as configurações das aplicações da plataforma (Airflow, Superset, etc.).
* **Pré-requisito:** Arquivo `.env` em `databases/postgres-metadata/` com `POSTGRES_USER`, `POSTGRES_PASSWORD` e `POSTGRES_DB`.

**🚀 Opção A: Deploy via Portainer (Recomendado)**
1. Crie uma stack nomeada `postgres-metadata`.
2. Aponte para o arquivo `databases/postgres-metadata/docker-compose.yml`.
3. Preencha as variáveis de ambiente e faça o deploy.

**💻 Opção B: Deploy Manual via Terminal**
```bash
docker compose -f databases/postgres-metadata/docker-compose.yml up -d
```
* **Acesso Externo na Mesma Rede:** `{IP_DO_SERVIDOR}:5433` (Nota: Mapeado na porta 5433 para evitar conflito com o Colunar).
* **Volumes:** `/docker-data/postgres-metadata/`

---

#### 5.3. MySQL
Banco de dados relacional clássico para simular sistemas transacionais (OLTP).
* **Pré-requisito:** Arquivo `.env` em `databases/mysql/` com `MYSQL_ROOT_PASSWORD` e `MYSQL_DATABASE`.

**🚀 Opção A: Deploy via Portainer** (Mesmo padrão: Stack `mysql`, apontar repo/arquivo, injetar variáveis).
**💻 Opção B: Deploy Manual via Terminal**
```bash
docker compose -f databases/mysql/docker-compose.yml up -d
```
* **Acesso Externo na Mesma Rede:** `{IP_DO_SERVIDOR}:3306`
* **Volumes:** `/docker-data/mysql/`

---

#### 5.4. MariaDB
Fork open-source do MySQL, excelente para testes de compatibilidade.
* **Pré-requisito:** Arquivo `.env` em `databases/mariadb/` com `MARIADB_ROOT_PASSWORD` e `MARIADB_DATABASE`.

**🚀 Opção A: Deploy via Portainer** (Mesmo padrão: Stack `mariadb`, apontar repo/arquivo, injetar variáveis).
**💻 Opção B: Deploy Manual via Terminal**
```bash
docker compose -f databases/mariadb/docker-compose.yml up -d
```
* **Acesso Externo na Mesma Rede:** `{IP_DO_SERVIDOR}:3307` (Nota: Mapeado na porta 3307 para evitar conflito com o MySQL).
* **Volumes:** `/docker-data/mariadb/`

---

#### 5.5. SQL Server
Banco de dados corporativo da Microsoft.
* **Pré-requisito:** Arquivo `.env` em `databases/sqlserver/` com `MSSQL_SA_PASSWORD` (mínimo 8 caracteres, complexidade exigida).

**🚀 Opção A: Deploy via Portainer** (Mesmo padrão: Stack `sqlserver`, apontar repo/arquivo, injetar variáveis).
**💻 Opção B: Deploy Manual via Terminal**
```bash
docker compose -f databases/sqlserver/docker-compose.yml up -d
```
* **Acesso Externo na Mesma Rede:** `{IP_DO_SERVIDOR}:1433`
* **Volumes:** `/docker-data/sqlserver/`

---

#### 5.6. Oracle (Free Slim)
Versão leve do Oracle Database voltada para containers e desenvolvimento.
* **Pré-requisito:** Arquivo `.env` em `databases/oracle/` com `ORACLE_PASSWORD`.

**🚀 Opção A: Deploy via Portainer** (Mesmo padrão: Stack `oracle`, apontar repo/arquivo, injetar variáveis).
**💻 Opção B: Deploy Manual via Terminal**
```bash
docker compose -f databases/oracle/docker-compose.yml up -d
```
* **Acesso Externo na Mesma Rede:** `{IP_DO_SERVIDOR}:1521`
* **Volumes:** `/docker-data/oracle/`

---

#### 5.7. MongoDB
Banco de dados NoSQL orientado a documentos.
* **Pré-requisito:** Arquivo `.env` em `databases/mongodb/` com `MONGO_USER` e `MONGO_PASSWORD`.

**🚀 Opção A: Deploy via Portainer** (Mesmo padrão: Stack `mongodb`, apontar repo/arquivo, injetar variáveis).
**💻 Opção B: Deploy Manual via Terminal**
```bash
docker compose -f databases/mongodb/docker-compose.yml up -d
```
* **Acesso Externo na Mesma Rede:** `{IP_DO_SERVIDOR}:27017`
* **Volumes:** `/docker-data/mongodb/`

---

#### 5.8. Cassandra
Banco de dados NoSQL colunar amplo, focado em altíssima disponibilidade.
* **Pré-requisito:** N/A (Variáveis mapeadas direto no compose para laboratório).

**🚀 Opção A: Deploy via Portainer** (Mesmo padrão: Stack `cassandra`, apontar repo/arquivo).
**💻 Opção B: Deploy Manual via Terminal**
```bash
docker compose -f databases/cassandra/docker-compose.yml up -d
```
* **Acesso Externo na Mesma Rede:** `{IP_DO_SERVIDOR}:9042`
* **Volumes:** `/docker-data/cassandra/`

---

#### 5.9. OpenSearch
Motor de busca e análise distribuído (sucessor open-source do Elasticsearch).
* **Aviso de Sistema (Host):** Antes de subir o container, o host Linux precisa ter o limite de áreas de memória mapeadas expandido. O OpenSearch utiliza `mmap` (Memory-Mapped Files) para carregar índices na RAM e realizar buscas ultrarrápidas, o que ultrapassa o limite padrão de segurança do kernel do Linux (65530). Sem esse ajuste, o container dá erro de memória e não inicia. Rode o comando abaixo diretamente no terminal do servidor host:
  ```bash
  sudo sysctl -w vm.max_map_count=262144
  ```
* **Pré-requisito:** Arquivo `.env` em `databases/opensearch/` com `OPENSEARCH_PASSWORD` (exige complexidade).

**🚀 Opção A: Deploy via Portainer** (Mesmo padrão: Stack `opensearch`, apontar repo/arquivo, injetar variáveis).
**💻 Opção B: Deploy Manual via Terminal**
```bash
docker compose -f databases/opensearch/docker-compose.yml up -d
```
* **Acesso Externo na Mesma Rede:** `{IP_DO_SERVIDOR}:9200`
* **Volumes:** `/docker-data/opensearch/`
