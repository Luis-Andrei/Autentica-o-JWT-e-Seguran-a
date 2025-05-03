# API de Pedidos com JWT

Esta é uma API de pedidos que utiliza JWT para autenticação e autorização.

## Requisitos

- Python 3.8+
- pip

## Instalação

1. Clone o repositório
2. Crie um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```
3. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Executando a API

```bash
python app.py
```

A API estará disponível em `http://localhost:5000`

## Endpoints

### Autenticação

- `POST /register`
  - Registra um novo usuário
  - Body: `{"username": "usuario", "password": "senha"}`

- `POST /login`
  - Autentica um usuário e retorna o token JWT
  - Body: `{"username": "usuario", "password": "senha"}`

### Pedidos

- `GET /orders`
  - Lista todos os pedidos do usuário autenticado
  - Requer token JWT no header: `Authorization: Bearer <token>`

- `POST /orders`
  - Cria um novo pedido
  - Requer token JWT no header: `Authorization: Bearer <token>`
  - Body: `{"description": "Descrição do pedido"}`
  - 
