from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from datetime import timedelta
import os

app = Flask(__name__)

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///storage.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configuração do JWT
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'sua-chave-secreta-aqui')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

# Inicialização das extensões
db = SQLAlchemy(app)
jwt = JWTManager(app)

# Importação dos modelos e rotas
from models import User, Order
from routes import auth_bp, orders_bp

# Registro dos blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(orders_bp)

# Criação das tabelas
with app.app_context():
    db.create_all() 