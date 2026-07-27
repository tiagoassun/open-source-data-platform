import os
import json

c = get_config()

# --- 1. DATABASE ---
c.JupyterHub.db_url = os.environ.get("DATABASE_URL")

# --- 2. AUTH (production-oriented) ---
c.JupyterHub.authenticator_class = "nativeauthenticator.NativeAuthenticator"
c.Authenticator.admin_users = {"admin"}
c.NativeAuthenticator.open_signup = False
c.NativeAuthenticator.allow_all = False
# Admins create users in the Hub UI; no public self-signup.

# --- 3. NETWORK ---
# hub_ip 0.0.0.0: Hub escuta em todas as interfaces (proxy + spawner na data-net)
# hub_connect_ip: nome DNS do container na data-net (notebooks usam isso para callback)
# bind_url: URL pública do proxy dentro do container (mapeada para host :8888)
c.JupyterHub.hub_ip = "0.0.0.0"
c.JupyterHub.hub_connect_ip = "jupyterhub"
c.JupyterHub.bind_url = "http://:8000"
c.DockerSpawner.use_internal_ip = True
c.DockerSpawner.network_name = "data-net"

# --- 4. SPAWNER ---
c.JupyterHub.spawner_class = "dockerspawner.DockerSpawner"
c.DockerSpawner.image = os.environ.get(
    "JUPYTERHUB_SPAWNER_IMAGE", "tiagoassun/mega-jupyter:latest"
)
c.DockerSpawner.remove = True
c.Spawner.http_timeout = int(os.environ.get("DOCKER_SPAWNER_HTTP_TIMEOUT", "600"))
c.Spawner.start_timeout = int(os.environ.get("JUPYTERHUB_HTTP_TIMEOUT", "600"))

# --- 5. PERSISTENCE (non-root notebook user) ---
notebook_dir = "/home/jovyan/work"
c.DockerSpawner.notebook_dir = notebook_dir
c.DockerSpawner.volumes = {
    "/docker-data/jupyterhub/users/{username}": notebook_dir,
}
c.DockerSpawner.environment = {
    "CHOWN_HOME": "yes",
    "CHOWN_HOME_OPTS": "-R",
}


# --- 6. LIFESTYLE HOOK ---
def pre_spawn_hook(spawner):
    username = spawner.user.name
    internal_user_path = f"/srv/jupyterhub/users/{username}"
    example_dir = os.path.join(internal_user_path, "_exemplos")
    git_dir = os.path.join(internal_user_path, "git")

    os.makedirs(example_dir, exist_ok=True)
    os.makedirs(git_dir, exist_ok=True)

    notebooks = {
        "spark_hello.ipynb": {
            "cells": [
                {
                    "cell_type": "code",
                    "metadata": {},
                    "source": [
                        "from pyspark.sql import SparkSession\n",
                        "import os\n",
                        "import getpass",
                    ],
                },
                {
                    "cell_type": "code",
                    "metadata": {},
                    "source": [
                        "spark = SparkSession.builder \\\n",
                        ' .appName("lab-spark") \\\n',
                        ' .config("spark.driver.memory", "2g") \\\n',
                        " .getOrCreate()",
                    ],
                },
                {
                    "cell_type": "code",
                    "metadata": {},
                    "source": [
                        "df = spark.range(0, 1_000_000)\n",
                        "print(f'Processed {df.count()} rows')",
                    ],
                },
            ],
            "metadata": {
                "kernelspec": {
                    "display_name": "Python 3 (ipykernel)",
                    "name": "python3",
                }
            },
            "nbformat": 4,
            "nbformat_minor": 5,
        },
        "r_hello.ipynb": {
            "cells": [
                {
                    "cell_type": "code",
                    "metadata": {},
                    "source": ['msg <- "Hello from R"\n', "print(msg)"],
                },
                {
                    "cell_type": "code",
                    "metadata": {},
                    "source": ["plot(sin(seq(0, 2*pi, length.out=100)))"],
                },
            ],
            "metadata": {"kernelspec": {"display_name": "R", "name": "ir"}},
            "nbformat": 4,
            "nbformat_minor": 5,
        },
    }

    for name, content in notebooks.items():
        file_path = os.path.join(example_dir, name)
        if not os.path.exists(file_path):
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(content, f, indent=1)

    os.system(f"chown -R 1000:1000 {internal_user_path}")


c.DockerSpawner.pre_spawn_hook = pre_spawn_hook
