import pytest
from app import app, db
from models import User, Order
import json

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    client = app.test_client()

    with app.app_context():
        db.create_all()
        yield client
        db.drop_all()

def test_register_user(client):
    response = client.post('/register', 
        json={'username': 'testuser', 'password': 'testpass'})
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['message'] == 'Usuário criado com sucesso'

def test_login_user(client):
    # Primeiro registra o usuário
    client.post('/register', 
        json={'username': 'testuser', 'password': 'testpass'})
    
    # Tenta fazer login
    response = client.post('/login', 
        json={'username': 'testuser', 'password': 'testpass'})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'access_token' in data

def test_create_order(client):
    # Registra e faz login
    client.post('/register', 
        json={'username': 'testuser', 'password': 'testpass'})
    login_response = client.post('/login', 
        json={'username': 'testuser', 'password': 'testpass'})
    token = json.loads(login_response.data)['access_token']

    # Cria um pedido
    response = client.post('/orders',
        json={'description': 'Test order'},
        headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 201
    data = json.loads(response.data)
    assert 'id' in data
    assert data['description'] == 'Test order'

def test_get_orders(client):
    # Registra e faz login
    client.post('/register', 
        json={'username': 'testuser', 'password': 'testpass'})
    login_response = client.post('/login', 
        json={'username': 'testuser', 'password': 'testpass'})
    token = json.loads(login_response.data)['access_token']

    # Cria um pedido
    client.post('/orders',
        json={'description': 'Test order'},
        headers={'Authorization': f'Bearer {token}'})

    # Busca os pedidos
    response = client.get('/orders',
        headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 1
    assert data[0]['description'] == 'Test order' 