# Projeto Boilerplate Django

Projeto utilizado como base para novos projetos utilizando [Django](https://djangoproject.com).

O projeto utiliza autenticação com Codata SSO.

## Iniciar novo projeto

Crie um *fork* do projeto pelo GitCodata (https://gitcodata.pb.gov.br/help/user/project/repository/forking_workflow.md)

Ou

Clone o projeto e reinicialize o repositório local:

```shell
# clonar projeto
git clone https://gitcodata.pb.gov.br/seed/django novo-projeto
cd novo-projeto

# remover dados do git
rm -r .git

# inicializar novo repositório git
git init

# definir repositório remoto do novo projeto
git remote add origin https://gitcodata.pb.gov.br/<grupo>/<projeto>.git
```

## Utilização

```shell
# Criar virtualenv
python -m venv .venv
source .venv/bin/activate

# instalar dependências de desenvolvimento
pip install -r requirements-dev.txt

# sincronizar dependências com pip-tools (https://github.com/jazzband/pip-tools/)
pip-sync

# copiar arquivo de variáveis de ambiente
cp .env.example .env
```

### Executar com Docker Compose

O boilerplate disponibiliza um docker-compose.yml para executar o projeto,
juntamente com um banco de dados Postgres e uma instância do Keycloak já
configurada para importar um realm de teste.

Após executar o `docker-compose up`, será possível acessar o sistema em
`http://localhost:8000` e efetuar autenticar com as credenciais:

| CPF         | Senha     |
|-------------|-----------|
| 00000000000 | codata123 |


### Adicionar nova dependência

Para adicionar uma nova dependência, adicione ao `requirements.in` e execute `pip-compile` para atualizar o
`requirements.txt`, então `pip-sync` para sincronizar o venv

```shell
# após atualizar o requirements.in
pip-compile
pip-sync
```