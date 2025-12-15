# Jogo da Forca - instâncias locais

Requisitos:
- Python 3.10+

Instalação:

```powershell
python -m pip install -r requirements.txt
```

Executando localmente:

```powershell
# inicia a aplicação (modo dev)
python run.py

# ou (usando flask CLI)
$env:FLASK_APP = "run:create_app"
flask run
```

Criar banco de dados SQLite:

```powershell
# usando o comando CLI registrado no app
flask create-db
```

Migrações (Flask-Migrate):

```powershell
# inicializa a pasta de migrações (faça uma vez)
flask db init
# cria uma nova migração
flask db migrate -m "initial"
# aplica migrações ao banco
flask db upgrade
```

Populando dados de exemplo (seed):

```powershell
# cria tabelas e insere usuários e palavras de exemplo
flask seed-db
```

Observações:
- Configure `DATABASE_URL` e `FORCA_SECRET` se desejar alterar o banco ou a chave secreta.
- As rotas principais estão em `forca_app/routes` e os modelos em `forca_app/models`.
