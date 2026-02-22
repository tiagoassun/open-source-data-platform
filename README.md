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


---
---


### 6. Workspace de Data Science (JupyterHub)
Um ambiente de desenvolvimento multiusuário de altíssimo desempenho. Ele utiliza a técnica de "Docker Spawning", o que significa que cada usuário que faz login ganha **seu próprio container Docker isolado**, rodando uma imagem massivamente customizada com recursos pré-instalados para quase qualquer cenário de engenharia e ciência de dados.


#### 🛡️ Isolamento, Persistência e Boas Práticas
A arquitetura de containers por usuário traz algumas características essenciais para o uso diário:
* **Espaço Individual:** Cada usuário possui sua própria pasta persistente no servidor, mapeada fisicamente no host em `/docker-data/jupyterhub/users/{username}`. Todos os notebooks e arquivos salvos ali dentro estão seguros.
* **Ambiente Efêmero (Zera no Logout):** O container do usuário é destruído e recriado a cada ciclo de login/logout. Isso é excelente: se você quebrar o ambiente instalando dependências conflitantes, basta fazer logout e login novamente para ganhar um container limpo e 100% funcional.
* **⚠️ Regra de Ouro (Commit sempre!):** Como o container "zera" ao deslogar, qualquer configuração extra, instalação manual via `pip/apt-get` ou arquivo salvo *fora* da sua pasta de usuário será **perdido para sempre**. Mantenha seus códigos rigorosamente dentro da sua pasta mapeada e **faça commits frequentes no Git** para garantir seu progresso.


#### ✨ Estrutura Automática (Lifestyle Hook)
Para facilitar o início do trabalho, sempre que um usuário faz o login, o sistema executa um script automático que cria duas pastas essenciais dentro do seu diretório pessoal:
* **`git/`**: Uma pasta limpa e dedicada para você clonar seus repositórios e manter o controle de versão dos seus projetos de forma organizada.
* **`_exemplos/`**: Uma pasta contendo 4 notebooks já configurados para demonstrar o poder e os kernels do ambiente:
  1. `spark_hello.ipynb`: Um teste de processamento em memória utilizando PySpark e Python 3.
  2. `cpp_hello.ipynb`: Exemplo de código compilado e executado nativamente no kernel de C++17.
  3. `rust_hello.ipynb`: Exemplo de execução interativa utilizando o kernel de Rust.
  4. `r_hello.ipynb`: Exemplo de manipulação de mensagens e plotagem de gráficos utilizando R.


#### 🧰 O que tem dentro do Workspace?
A imagem base (`tiagoassun/mega-jupyter:latest`) foi construída para ser um "canivete suíço" absoluto, contendo:
* **Kernels Inclusos:** Python, R, Scala, PySpark, C++ (via xeus-cling), Rust (via evcxr_jupyter) e C (via jupyter-c-kernel).
* **Data Science:** `pandas`, `numpy`, `scipy`, `matplotlib`, `seaborn`, `bokeh`, `scikit-learn`, `statsmodels`, `sympy`, `patsy`, `sqlalchemy`, `h5py`, `tables` (pytables).
* **Web Scraping & Extração:** `beautifulsoup4`, `requests`, `scrapy`, `selenium` (com webdriver), `playwright`.
* **APIs Sociais/Web:** `tweepy`, `instaloader`, `facebook-sdk`, `praw`, `discord.py`, `spotipy`, `linkedin-api`, `pywhatkit`, `python-telegram-bot`, `google-api-python-client`, `cinemagoer`, `justwatch`.
* **APIs de IA:** `google-generativeai` (Gemini), `openai` (ChatGPT/DeepSeek), `anthropic`.
* **Drivers de Bancos de Dados:** `boto3` (MinIO/S3), `psycopg2-binary` (PostgreSQL), `oracledb` (Oracle), `pymysql` (MySQL/MariaDB), `pymssql` (SQL Server), `cassandra-driver`, `pymongo` (MongoDB), `opensearch-py`.


#### 🏗️ Arquitetura dos Arquivos
A configuração deste serviço é dividida em três pilares dentro da pasta `workspace/jupyterhub/`:
1. **`Dockerfile`:** Define a receita da imagem isolada dos usuários.
2. **`jupyterhub_config.py`:** O cérebro do sistema. Gerencia a autenticação, a conexão com o banco de metadados, a rede e o *Lifestyle Hook*.
3. **`docker-compose.yml`:** A infraestrutura principal que levanta o Hub e o conecta ao Docker do servidor host.


#### ⚠️ Pré-requisitos (Importante)
Este serviço possui **dependência direta** do container `postgres-metadata` para salvar usuários e sessões.
1. Acesse o seu banco de dados `postgres-metadata` e **crie um database vazio chamado `jupyterhub_db`**.
2. Gere uma chave de criptografia segura rodando `openssl rand -hex 32` no terminal Linux do servidor.
3. Crie o arquivo `.env` na pasta `workspace/jupyterhub/`:
   ```env
   JUPYTERHUB_CRYPT_KEY=cole_a_chave_gerada_aqui
   POSTGRES_METADATA_PASSWORD=senha_do_seu_banco_metadata
   ```
4. **Construção da Imagem do Workspace (Apenas na primeira vez):**
   Você deve "fabricar" a imagem gigante do workspace na sua máquina antes de subir o Hub.
   
   > **💡 Atenção ao Build:** Como esta imagem compila pacotes pesados (como Rust e C++), o processo exige muito processamento e tempo. **Nunca tente fazer o build dessa imagem pelo Portainer**, pois a interface web provavelmente vai dar *timeout*. Faça a construção sempre via terminal para acompanhar os logs.

   Estando na pasta raiz do repositório, execute:
   ```bash
   docker build -t tiagoassun/mega-jupyter:latest -f workspace/jupyterhub/Dockerfile workspace/jupyterhub
   ```

**🚀 Opção A: Deploy do Hub via Portainer (Recomendado)**
Após a imagem ter sido construída no passo acima, você pode subir o serviço principal pelo Portainer.
1. Crie uma stack nomeada `jupyterhub`.
2. Aponte para o arquivo `workspace/jupyterhub/docker-compose.yml`.
3. Preencha as variáveis e faça o deploy.

**💻 Opção B: Deploy do Hub Manual via Terminal**
Estando na pasta raiz do repositório, execute:
```bash
docker compose -f workspace/jupyterhub/docker-compose.yml up -d
```

**Detalhes Técnicos:**
* **Acesso Externo:** `{IP_DO_SERVIDOR}:8888`
* **Rede:** Utiliza a `data-net` nativamente.
* **Volumes:** `/docker-data/jupyterhub/`


---
---


### 7. Orquestração de Dados (Apache Airflow)
Responsável por agendar, orquestrar e monitorar todos os pipelines de dados da plataforma. 

#### 🌟 Arquitetura Desacoplada (Solução Ouro: DockerOperator)
Para manter o Airflow leve e rápido, adotamos a arquitetura de orquestração isolada. O Airflow atua apenas como o **Maestro**, e não como o executor de processamento pesado. 
* **Execução via Docker:** O Airflow tem acesso direto ao *daemon* do Docker do host (`/var/run/docker.sock`).
* **Isolamento de Dependências:** Ele sobe containers efêmeros usando a imagem rica do JupyterHub (`tiagoassun/mega-jupyter:latest`), executa o código e destrói o container após o uso. Isso garante que as DAGs tenham acesso a todas as bibliotecas (Selenium, PySpark, Rust, etc.) sem inchar o Airflow.

#### 🔄 Sincronização Automática (GitOps)
A plataforma gerencia DAGs de forma dinâmica. A DAG administrativa `_sync_git_all_repos` monitora o arquivo `repos.json` e sincroniza repositórios externos a cada 1 minuto.
* **Segurança Total:** As URLs no `repos.json` são mantidas "limpas" (ex: `https://github.com/user/repo.git`). As credenciais de acesso são injetadas em tempo de execução via variáveis de ambiente (`GIT_USER` e `GIT_TOKEN`), permitindo que o projeto seja versionado no GitHub sem risco de vazamento de tokens.

**Exemplo de DAG com DockerOperator:**
```python
from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount
from datetime import datetime

with DAG('dag_solucao_ouro', start_date=datetime(2026, 1, 1), schedule_interval=None) as dag:

    tarefa = DockerOperator(
        task_id='rodar_processamento_isolado',
        image='tiagoassun/mega-jupyter:latest',
        command='python /app/seu_script.py',
        docker_url='unix://var/run/docker.sock',
        network_mode='data-net',
        auto_remove=True,
        mounts=[
            Mount(source='/docker-data/airflow/dags', target='/app', type='bind')
        ]
    )
    
    tarefa
```

#### ⚠️ Pré-requisitos (Importante)
Este serviço utiliza o banco central da plataforma (`postgres-metadata`).
1. Acesse o seu banco de dados `postgres-metadata` e **crie um database vazio chamado `airflow_db`**.
2. Crie o arquivo `.env` na pasta `orchestration/airflow/` (este arquivo **não** deve ser enviado ao GitHub):
   ```env
   POSTGRES_METADATA_PASSWORD=senha_do_seu_banco_metadata
   AIRFLOW_ADMIN_EMAIL=tiagoassunjob@outlook.com
   AIRFLOW_ADMIN_PASSWORD=sua_senha_web_airflow
   GIT_USER=seu_usuario_github
   GIT_TOKEN=seu_personal_access_token
   ```

**🚀 Opção A: Deploy via Portainer (Recomendado)**
1. Crie uma stack nomeada `airflow`.
2. Aponte para o arquivo `orchestration/airflow/docker-compose.yml`.
3. Preencha as variáveis de ambiente mapeadas no `.env` e faça o deploy.

**💻 Opção B: Deploy Manual via Terminal**
```bash
docker compose -f orchestration/airflow/docker-compose.yml up -d
```

**Detalhes Técnicos:**
* **Acesso Externo:** `{IP_DO_SERVIDOR}:8080`
* **Rede:** `data-net` (acesso a todos os bancos e serviços).
* **Volumes:** `/docker-data/airflow/` (Persistência de Dags, Logs e Plugins).