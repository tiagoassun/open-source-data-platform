# 1. Base com Python, R, Scala e PySpark
FROM jupyter/all-spark-notebook:latest

USER root

# 2. Dependências de Sistema Operacional (C/C++, Rust, Drivers de DB e Scraping)
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    cmake \
    libpq-dev \
    unixodbc-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Volta para o usuário jovyan (padrão do Jupyter) para instalar as coisas dele
USER ${NB_UID}

# 3. Instalando Kernel de C++ via Conda
RUN mamba install -y -c conda-forge xeus-cling && \
    mamba clean --all -f -y

# 4. Instalando Rust e o Kernel do Rust
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/home/jovyan/.cargo/bin:${PATH}"
RUN cargo install evcxr_jupyter && evcxr_jupyter --install

# 5. Instalando Bibliotecas Python gigantes
RUN pip install --no-cache-dir \
    # Data Science Clássico
    pandas numpy scipy matplotlib seaborn bokeh scikit-learn statsmodels sympy patsy sqlalchemy h5py tables \
    # Web Scraping
    beautifulsoup4 requests scrapy selenium playwright \
    # Redes Sociais e Mídias
    tweepy instaloader facebook-sdk praw discord.py spotipy linkedin-api pywhatkit python-telegram-bot google-api-python-client cinemagoer justwatch \
    # Inteligência Artificial
    google-generativeai openai anthropic \
    # Bancos de Dados
    boto3 psycopg2-binary pymysql cassandra-driver pymongo opensearch-py

# Instala os navegadores do Playwright para Scraping avançado
RUN playwright install chromium