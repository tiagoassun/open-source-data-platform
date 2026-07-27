from airflow import DAG
from airflow.decorators import task
from datetime import datetime
import json
import os
import subprocess

BASE_DAGS_FOLDER = "/opt/airflow/dags"
REPOS_CONFIG_PATH = os.path.join(BASE_DAGS_FOLDER, "_sync_git_all_repos", "repos.json")


def get_repos():
    """Lê a lista de repositórios do arquivo JSON."""
    if os.path.exists(REPOS_CONFIG_PATH):
        try:
            with open(REPOS_CONFIG_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Erro ao ler repos.json: {e}")
            return []
    return []


with DAG(
    "_sync_git_all_repos",
    start_date=datetime(2026, 2, 20),
    schedule="*/5 * * * *",
    catchup=False,
    tags=["admin", "infrastructure", "gitops"],
    doc_md="""
    ### DAG de Sincronização GitOps
    Esta DAG automatiza a atualização de todos os repositórios de DAGs da plataforma.
    Ela lê o arquivo `repos.json`, injeta as credenciais de ambiente (`GIT_USER` e `GIT_TOKEN`)
    e realiza o `git clone` ou `git pull` conforme necessário.
    """,
) as dag:
    for repo in get_repos():
        repo_name = repo["nome"]

        @task(task_id=f"sync_{repo_name}")
        def sync_repo_task(current_repo=repo):
            dest_path = os.path.join(BASE_DAGS_FOLDER, current_repo["nome"])

            git_user = os.environ.get("GIT_USER", "")
            git_token = os.environ.get("GIT_TOKEN", "")

            raw_url = current_repo["url"].replace("https://", "").replace("http://", "")
            protocol = "https" if current_repo["url"].startswith("https") else "http"

            if git_user and git_token:
                authenticated_url = f"{protocol}://{git_user}:{git_token}@{raw_url}"
            else:
                authenticated_url = current_repo["url"]

            if not os.path.exists(dest_path):
                print(f"[NOVO REPO] Clonando: {current_repo['nome']}...")
                result = subprocess.run(
                    ["git", "clone", "-b", current_repo["branch"], authenticated_url, dest_path],
                    capture_output=True,
                    text=True,
                )
                if result.returncode != 0:
                    raise RuntimeError(f"Erro ao clonar: {result.stderr}")
            else:
                print(f"[ATUALIZAÇÃO] Sincronizando: {current_repo['nome']}...")
                subprocess.run(
                    ["git", "-C", dest_path, "remote", "set-url", "origin", authenticated_url],
                    check=True,
                )
                result = subprocess.run(
                    ["git", "-C", dest_path, "pull", "origin", current_repo["branch"]],
                    capture_output=True,
                    text=True,
                )
                if result.returncode != 0:
                    raise RuntimeError(f"Erro ao atualizar: {result.stderr}")

        sync_repo_task()
