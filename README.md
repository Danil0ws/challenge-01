# Technical challenge Loja Integrada! - Cart API

Simple shopping cart api written in Python + Flask + SqlLite + UnitTest + Docker.

### :rocket: Tecnologias usadas

Este maravilindo projeto foi desenvolvido com as seguintes tecnologias:

- [Python](https://www.python.org/)
- [Flask](https://pypi.org/project/Flask/)
- [Flask-RESTful](https://www.npmjs.com/package/Flask-RESTful)
- [flask-expects-json](https://www.npmjs.com/package/flask-expects-json)
- [Sqlite3](https://www.sqlite.org/index.html)
- [UnitTest](https://docs.python.org/3/library/unittest.html)
- [Docker](https://www.docker.com/)

## :memo: API Documentation

The documentation can be found in our [Swagger](https://app.swaggerhub.com/apis-docs/Danil0ws/challenge-01/1.0.0)

### :white_check_mark: What is required

- [x] Adicionar um item no carrinho
- [x] Remover um item do carrinho
- [x] Atualizar a quantidade de um item no carrinho
- [x] Limpar o carrinho
- [x] Adicionar um cupom de desconto ao carrinho
- [x] Gerar totais e subtotais
- [x] Persistir o carrinho
- [x] Recuperar o carrinho
- [x] Retornar um JSON com o carrinho completo (para ser usado no frontend)

### :computer: How to run locally

Fork this repo and then clone it:
You'll need Python installed on your computer in order to build this app.

```
git clone https://github.com/Danil0ws/challenge-01.git challenge-01
cd challenge-01
```

Then just install dependencies

```
pip install --no-cache-dir -r requirements.txt
```

Then just run

```
python src/app.py
```

to start the development server on port `5000`. Your jsonbox instance will be running on `http://127.0.0.1:5000/`. Alternatively you can run the application using docker with `docker-compose up`.

## :test_tube: Testing

To run the library tests, use

```
python -m unittest -v
```

---

<p align="center">Feito com ❤️ e ☕ por <strong>Danilo Rodrigues</p>
