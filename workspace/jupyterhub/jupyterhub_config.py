import os
import json


c = get_config()

# --- 1. BANCO DE DADOS (PostgreSQL) ---
# O Python pega a URL mastigada pelo Docker Compose via variável de ambiente
c.JupyterHub.db_url = os.environ.get('DATABASE_URL')



# --- 2. AUTENTICAÇÃO ---
c.JupyterHub.authenticator_class = 'nativeauthenticator.NativeAuthenticator'
c.Authenticator.admin_users = {'admin'}
c.Authenticator.allowed_users = {'admin'}
c.NativeAuthenticator.open_signup = True
c.NativeAuthenticator.allow_all = True



# --- 3. REDE E CONEXÃO ---
c.JupyterHub.hub_ip = '0.0.0.0'
c.JupyterHub.hub_connect_ip = 'jupyterhub'
c.DockerSpawner.use_internal_ip = True
c.DockerSpawner.network_name = 'data-net'



# --- 4. SPAWNER (Gestão de Imagem e Timeouts) ---
c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'
c.DockerSpawner.image = 'tiagoassun/mega-jupyter:latest'
c.DockerSpawner.remove = True 
c.Spawner.http_timeout = 600
c.Spawner.start_timeout = 600



# --- 5. PERSISTÊNCIA E PERMISSÕES ---
c.DockerSpawner.extra_create_kwargs = {'user': 'root'}
c.DockerSpawner.environment = {
    "CHOWN_HOME": "yes",
    "CHOWN_HOME_OPTS": "-R",
    "GRANT_SUDO": "yes"
}
notebook_dir = '/home/jovyan/work'
c.DockerSpawner.notebook_dir = notebook_dir
c.DockerSpawner.volumes = {
    '/docker-data/jupyterhub/users/{username}': notebook_dir
}



# --- 6. LIFESTYLE HOOK (Versão Reforçada) ---
def pre_spawn_hook(spawner):
    import os
    import json

    username = spawner.user.name
    internal_user_path = f'/srv/jupyterhub/users/{username}'
    example_dir = os.path.join(internal_user_path, '_exemplos')
    git_dir = os.path.join(internal_user_path, 'git')

    os.system(f"mkdir -p {example_dir}")
    os.system(f"mkdir -p {git_dir}")

    notebooks = {
        'spark_hello.ipynb': {
            "cells": [
                {"cell_type": "code", "metadata": {}, "source": ["from pyspark.sql import SparkSession\n", "import os\n", "import getpass"]},
                {"cell_type": "code", "metadata": {}, "source": ["spark = SparkSession.builder \\\n", "    .appName(\"TesteHardwareTiago\") \\\n", "    .config(\"spark.driver.memory\", \"8g\") \\\n", "    .getOrCreate()"]},
                {"cell_type": "code", "metadata": {}, "source": ["df = spark.range(0, 10000000)\n", "print(f'📊 Processados {df.count()} registros!')"]}
            ],
            "metadata": {"kernelspec": {"display_name": "Python 3 (ipykernel)", "name": "python3"}},
            "nbformat": 4, "nbformat_minor": 5
        },
        'cpp_hello.ipynb': {
            "cells": [
                {"cell_type": "code", "metadata": {}, "source": ["#include <iostream>\n", "#include <vector>\n", "#include <string>"]},
                {"cell_type": "code", "metadata": {}, "source": ["std::string user = \"Tiago\";\n", "std::cout << \"Hello \" << user << \" de um notebook C++17!\" << std::endl;"]}
            ],
            "metadata": {"kernelspec": {"display_name": "C++17", "name": "xcpp17"}},
            "nbformat": 4, "nbformat_minor": 5
        },
        'rust_hello.ipynb': {
            "cells": [
                {"cell_type": "code", "metadata": {}, "source": ["let name = \"Tiago Assunção\";\n", "println!(\"Hello, {}! Rust está voando no i7.\", name);"]}
            ],
            "metadata": {"kernelspec": {"display_name": "Rust", "name": "rust"}},
            "nbformat": 4, "nbformat_minor": 5
        },
        'r_hello.ipynb': {
            "cells": [
                {"cell_type": "code", "metadata": {}, "source": ["msg <- \"Olá do R, Tiago!\"\n", "print(msg)"]},
                {"cell_type": "code", "metadata": {}, "source": ["plot(sin(seq(0, 2*pi, length.out=100)))"]}
            ],
            "metadata": {"kernelspec": {"display_name": "R", "name": "ir"}},
            "nbformat": 4, "nbformat_minor": 5
        }
    }

    for name, content in notebooks.items():
        file_path = os.path.join(example_dir, name)
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                json.dump(content, f, indent=1)
    
    os.system(f"chown -R 1000:1000 {internal_user_path}")

c.DockerSpawner.pre_spawn_hook = pre_spawn_hook



# --- 7. BIND API ---
c.JupyterHub.hub_bind_url = 'http://0.0.0.0:8081'