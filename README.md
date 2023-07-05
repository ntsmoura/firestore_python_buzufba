# Projeto de Laboratório de Bancos de Dados 
## :boom: Como rodar

Certifique-se de possuir uma base de dados firestore (gere uma chave privada para esta base) e Python 3.10 na sua máquina. 

Clone o repositório e mude para raiz dele.

```sh
# Copie o .settings.toml
$ cp .settings.toml .settings.local.toml

```
Coloque o arquivo json com sua chave privada na mesma pasta do repositório, e insira o nome deste na variável de ambiente "json_name" em "CRED".

Abre um terminal e baixe as dependências com Pipenv após instala-lo:

```sh
# Instale o pipenv
$ pip install pipenv
# Instale as dependências
$ pipenv install
# Abra o ambiente virtual
$ pipenv shell
# Rode o script sync.py ou async.py
$ pipenv run py async.py
```

O script irá executar os comandos em ordem.
