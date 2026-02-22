# Open Source Data Platform

Uma plataforma de dados moderna e modular, construída inteiramente com ferramentas de código aberto e orquestrada via Docker. Este projeto serve como um laboratório completo para práticas de Engenharia de Dados.

## 🏗️ Arquitetura da Plataforma

A plataforma é dividida em camadas lógicas:

* **Management:** Portainer (Gestão de Containers)
* **Storage:** MinIO (Object Storage S3)
* **Databases:** PostgreSQL (Metadata) e PostgreSQL + Hydra (Analytics)
* **Workspace:** JupyterHub
* **Orchestration:** Apache Airflow
* **Dataviz:** Apache Superset
* **Networking:** Cloudflare Tunnel

---

## 🚀 Como Iniciar

### 1. Criar a Rede Unificada
Todas as ferramentas comunicam-se através da rede `data-net`.

```bash
chmod +x scripts/create_network.sh
./scripts/create_network.sh
```

### 2. Subir o Gerenciamento (Portainer)
O Portainer deve ser o primeiro container a ser levantado. Estando na pasta raiz do repositório, execute o comando abaixo:

**Comandos:**
```bash
docker compose -f management/portainer/docker-compose.yml up -d
```

**Detalhes Técnicos:**
* **Acesso:** https://{IP_DO_SERVIDOR}:9443
* **Rede:** Utiliza a rede externa `data-net`
* **Volumes:** Dados persistidos em `/docker-data/portainer`