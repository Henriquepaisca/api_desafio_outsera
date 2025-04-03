# API Desafio Outsera

Este projeto é uma API desenvolvida com **FastAPI** para processar e servir dados a partir de um arquivo CSV e um banco de dados.

## 📌 **Requisitos**

Antes de iniciar, certifique-se de ter instalado:

- Python 3.9+
- Virtualenv (opcional, mas recomendado)
- PostgreSQL ou SQLite (se necessário)

## 🚀 **Instalação**

1. Clone o repositório:

```bash
    git clone https://github.com/Henriquepaisca/api-outsera.git
    cd api-outsera
```

2. Crie e ative um ambiente virtual (opcional, mas recomendado):

```bash
    python -m venv venv
    source venv/bin/activate  # Linux/macOS
    venv\Scripts\activate     # Windows
```

3. Instale as dependências:

```bash
    pip install -r requirements.txt
```


## ▶ **Rodando a API**

Para iniciar o servidor FastAPI, execute:

```bash
    uvicorn app.main:app --reload
```

A API estará disponível em:

🔗 **http://127.0.0.1:8000**

A documentação interativa pode ser acessada em:

- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Redoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## ✅ **Executando os Testes**

Para rodar os testes, utilize **pytest**:

```bash
    pytest -v
```

Se precisar forçar o caminho do projeto:

```bash
    PYTHONPATH=. pytest -v
```

## 📂 **Estrutura do Projeto**

```
api-outsera/
├── app/
│   ├── __init__.py
│   ├── main.py  # Arquivo principal da API
│   ├── database.py  # Configuração do banco
│   ├── models.py  # Definição dos modelos
├── static/
│   ├── data.csv  # Arquivo CSV usado pela API
├── tests/
│   ├── __init__.py
│   ├── test_main.py  # Testes da API
├── venv/  # Ambiente virtual (opcional)
├── requirements.txt  # Lista de dependências
├── pytest.ini  # Configuração do Pytest
├── README.md  # Este arquivo
```

## 🛠 **Tecnologias Utilizadas**

- [FastAPI](https://fastapi.tiangolo.com/)
- [Uvicorn](https://www.uvicorn.org/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Pandas](https://pandas.pydata.org/)
- [Pytest](https://docs.pytest.org/)

---

💡 **Dúvidas ou melhorias?** Fique à vontade para contribuir com o projeto!

