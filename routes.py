from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import User, Order
from app import db

auth_bp = Blueprint('auth', __name__)
orders_bp = Blueprint('orders', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'Usuário já existe'}), 400
    
    user = User(username=data['username'])
    user.set_password(data['password'])
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'message': 'Usuário criado com sucesso'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    
    if user and user.check_password(data['password']):
        access_token = create_access_token(identity={
            'id': user.id,
            'username': user.username
        })
        return jsonify(access_token=access_token), 200
    
    return jsonify({'message': 'Credenciais inválidas'}), 401

@orders_bp.route('/orders', methods=['GET'])
@jwt_required()
def get_orders():
    current_user = get_jwt_identity()
    orders = Order.query.filter_by(user_id=current_user['id']).all()
    
    return jsonify([{
        'id': order.id,
        'description': order.description,
        'created_at': order.created_at.isoformat()
    } for order in orders]), 200

@orders_bp.route('/orders', methods=['POST'])
@jwt_required()
def create_order():
    current_user = get_jwt_identity()
    data = request.get_json()
    
    order = Order(
        description=data['description'],
        user_id=current_user['id']
    )
    
    db.session.add(order)
    db.session.commit()
    
    return jsonify({
        'id': order.id,
        'description': order.description,
        'created_at': order.created_at.isoformat()
    }), 201 