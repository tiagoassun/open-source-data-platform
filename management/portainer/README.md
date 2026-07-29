# Portainer CE

Gestão visual dos containers e stacks Docker desta plataforma.

O Portainer é o **primeiro** serviço a subir, e o único que sobe **obrigatoriamente via terminal**. Depois dele, os demais serviços sobem como **Stacks** na UI.

Documentação oficial: [https://docs.portainer.io/](https://docs.portainer.io/)

## Para que serve

- Interface HTTPS para operar Docker no host (containers, imagens, redes, volumes, stacks)
- Ponto único de deploy dos outros serviços deste repositório
- Persistência de usuários, stacks e configurações em `/docker-data/portainer`

## O que precisa antes

1. Rede externa `data-net` criada (ver README da raiz e `_scripts/create_network.sh`)
2. Docker Engine + Docker Compose no host
3. Pasta de dados no host:

```bash
mkdir -p /docker-data/portainer
```

## Como subir

Único serviço desta plataforma que **deve** iniciar pela CLI (não pela própria UI de Stacks):

```bash
# Na raiz do repositório
docker compose -f management/portainer/docker-compose.yml up -d
```

Acompanhar:

```bash
docker compose -f management/portainer/docker-compose.yml ps
docker logs -f portainer
```

## Acesso


| O que                    | Endereço                        |
| ------------------------ | ------------------------------- |
| UI HTTPS                 | `https://{IP_DO_SERVIDOR}:9443` |
| Edge / tunnel (opcional) | porta `8000` no host            |


O certificado HTTPS é **autoassinado** por padrão: o browser vai alertar (avançar / aceitar o risco). Em produção, coloque TLS na frente (reverse proxy / Cloudflare Tunnel) e restrinja o acesso pela rede.

## Primeiro acesso (criar o admin)

### Senha padrão?

**Não há senha padrão.** Com este `docker-compose.yml`, o Portainer CE **não** sobe com usuário/senha de fábrica.


| Mito                           | Realidade neste projeto |
| ------------------------------ | ----------------------- |
| `admin` / `admin`              | Não existe              |
| `admin` / `portainer`          | Não existe              |
| Qualquer senha fixa no compose | Não há                  |


Na **primeira** vez (volume `/docker-data/portainer` vazio), **você** define o administrador na UI. Essa senha que você criar **é** a senha do ambiente - não há outra escondida.

### Passo a passo

1. Suba o container (`docker compose ... up -d`) e espere ficar rodando.
2. Abra `https://{IP_DO_SERVIDOR}:9443` no browser (aceite o aviso do certificado autoassinado se aparecer).
3. Na tela de setup, **crie o primeiro administrador**:
  - **Username:** por padrão sugere `admin` (pode alterar)
  - **Password:** defina agora; mínimo **12 caracteres** (e as regras que a tela listar)
4. Guarde essa senha com o mesmo rigor de uma conta **root** do servidor: admin no Portainer controla o Docker deste host via `docker.sock`.
5. Em versões recentes do Portainer, a tela de criação do admin pode pedir um **código de confirmação** (setup token). Isso é uma proteção anti-bot: o Portainer gera esse código nos **logs do container**. Se a UI pedir, rode no host:

```bash
docker logs portainer 2>&1 | grep -i setup_token
```

Copie o valor que aparecer e cole na UI. Se a tela **não** pedir o token, ignore este passo.

1. Depois do admin criado, o **Environment Wizard** aparece. Com o socket montado, o ambiente **local** (Docker deste host) costuma ser detectado automaticamente. Avance com **Get Started** (ou adicione outros environments depois).

### Depois do primeiro login: troque / rotacione a senha

Mesmo tendo sido **você** quem definiu a senha no setup:

1. Entre no Portainer com o usuário admin criado.
2. Vá em **My account** (ou equivalente no menu do usuário) e **altere a senha** para uma senha forte, única deste ambiente.
3. Em produção: use gerenciador de senhas; não compartilhe a conta admin; crie usuários com perfil menor para o dia a dia, se fizer sentido.

Não deixe a senha do setup "provisória" para sempre - trate a troca (ou a confirmação de que a senha do setup já é a definitiva e forte) como parte de colocar o serviço em uso.

### Acessos seguintes

- Login em `https://{IP_DO_SERVIDOR}:9443` com o usuário e a senha atuais (a do setup ou a que você trocou depois).
- Se esquecer a senha: não há reset "mágico" pela UI sem acesso ao host; use o procedimento oficial da documentação do Portainer e **não** apague `/docker-data/portainer` sem backup.

### Se a tela de criar admin não aparecer

- O volume `/docker-data/portainer` **já tem** um admin de uma instalação anterior: use esse usuário/senha (ainda assim, **troque a senha** se não tiver certeza de quem a conhece).
- Ou o container ainda não subiu / a porta 9443 não está acessível: confira `docker ps` e `docker logs portainer`.

### Senha pré-definida no deploy (opcional, automação)**token**

Este `docker-compose.yml` **não** pré-configura senha (fluxo na UI).

Para automação (IaC), o Portainer aceita na **primeira** criação do admin flags como `--admin-password-file` ou `--admin-password` (hash bcrypt). Depois do primeiro boot isso **não** redefine a senha. Se usar esse caminho: documente onde a senha ficou, faça o primeiro login e **troque a senha** na UI. Detalhes: [CLI](https://docs.portainer.io/advanced/cli) e [initial setup](https://docs.portainer.io/start/install-ce/server/setup).

## O que o compose faz

Arquivo: `docker-compose.yml`

### Imagem

- `portainer/portainer-ce:2.27.9` (versão fixa da imagem)
- Evite `:latest` em produção: uma atualização sem versão fixa pode mudar comportamento

### Restart

- `unless-stopped`: sobe após reboot do host, mas respeita um `docker stop` manual

### Portas


| Host | Container | Uso                               |
| ---- | --------- | --------------------------------- |
| 9443 | 9443      | UI web HTTPS (use esta)           |
| 8000 | 8000      | Canal do **Portainer Edge Agent** |


Sobre a porta **8000**:

- Não é a interface web
- Serve para hosts **remotos** com Edge Agent instalado aparecerem neste Portainer
- Em um único servidor, essa porta é opcional; pode remover o mapeamento se não for usar Edge
- Não é "Portainer falando com outro Portainer": nos outros hosts roda o **agent**; este Portainer é o painel central

### Volumes


| Host                     | Container              | Uso                                  |
| ------------------------ | ---------------------- | ------------------------------------ |
| `/var/run/docker.sock`   | `/var/run/docker.sock` | Controle do Docker Engine deste host |
| `/docker-data/portainer` | `/data`                | Usuários, stacks, settings           |


**Docker socket (`docker.sock`):**

No Linux, o Docker Engine expõe sua API local nesse arquivo. Ao montar o socket dentro do container, o Portainer envia comandos ao daemon **deste mesmo host** (criar/parar containers, stacks, logs, etc.).

Quem tem admin no Portainer tem poder quase equivalente a root nesta máquina. Proteja a conta, a URL e a rede de acesso.

**Volume `/data`:**

Se você recriar o container do Portainer sem apagar `/docker-data/portainer`, usuários e stacks permanecem.

### Rede

- `data-net` (externa): o Portainer enxerga os outros containers da plataforma pelo nome na rede Docker

## Operação em produção

- Restrinja quem acessa `:9443` (firewall, VPN, Zero Trust, reverse proxy)
- Não exponha `:9443` na internet sem autenticação forte e TLS adequado
- Prefira Stacks no Portainer para os demais serviços; reserve a CLI para Portainer, emergências e builds de imagem
- Backup periódico de `/docker-data/portainer`
- Ao atualizar a imagem, fixe a nova tag no compose, teste e só então aplique

## Atualizar / recriar

Neste projeto a imagem está com **versão fixa** (ex.: `portainer/portainer-ce:2.27.9` no compose). O `pull` só baixa **essa** tag; não atualiza sozinho para uma versão mais nova.

Para subir de versão:

1. Edite a tag no `docker-compose.yml` (ex.: `2.27.9` -> `2.28.0`).
2. Rode:

```bash
docker compose -f management/portainer/docker-compose.yml pull
docker compose -f management/portainer/docker-compose.yml up -d
```

Se você **não** mudar a tag antes, o `pull`/`up` só recria o mesmo `2.27.9` (útil para recriar o container, não para atualizar).

## Parar

```bash
docker compose -f management/portainer/docker-compose.yml stop
# ou remover o container (dados em /docker-data/portainer permanecem):
docker compose -f management/portainer/docker-compose.yml down
```

## Próximos passos

Depois do Portainer no ar, suba os outros serviços como Stacks. Ordem sugerida e visão geral: README na raiz. Detalhes de cada ferramenta: `README.md` na pasta do serviço.