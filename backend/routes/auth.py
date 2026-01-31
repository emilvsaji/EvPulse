from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app import mongo
from models.user import User
from bson import ObjectId

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    """User login endpoint"""
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'success': False, 'error': 'Email and password are required'}), 400
        
        # Find user by email
        user_data = mongo.db.users.find_one({'email': email})
        
        if not user_data:
            return jsonify({'success': False, 'error': 'Invalid email or password'}), 401
        
        # Verify password
        if not User.check_password(password, user_data['password']):
            return jsonify({'success': False, 'error': 'Invalid email or password'}), 401
        
        # Create user object and generate token
        user = User.from_dict(user_data)
        access_token = create_access_token(identity=str(user_data['_id']))
        
        return jsonify({
            'success': True,
            'user': user.to_safe_dict(),
            'token': access_token
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@auth_bp.route('/register', methods=['POST'])
def register():
    """User registration endpoint"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['email', 'password', 'name']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'success': False, 'error': f'{field} is required'}), 400
        
        # Check if user already exists
        existing_user = mongo.db.users.find_one({'email': data['email']})
        if existing_user:
            return jsonify({'success': False, 'error': 'Email already registered'}), 400
        
        # Create new user
        user = User(
            email=data['email'],
            password=data['password'],
            name=data['name'],
            role=data.get('role', 'user'),
            phone=data.get('phone'),
            vehicle=data.get('vehicle'),
            company=data.get('company')
        )
        
        result = mongo.db.users.insert_one(user.to_dict())
        user.id = str(result.inserted_id)
        
        # Generate token
        access_token = create_access_token(identity=user.id)
        
        return jsonify({
            'success': True,
            'user': user.to_safe_dict(),
            'token': access_token
        }), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get current authenticated user"""
    try:
        user_id = get_jwt_identity()
        user_data = mongo.db.users.find_one({'_id': ObjectId(user_id)})
        
        if not user_data:
            return jsonify({'success': False, 'error': 'User not found'}), 404
        
        user = User.from_dict(user_data)
        return jsonify({'success': True, 'user': user.to_safe_dict()})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@auth_bp.route('/update-profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """Update user profile"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        # Fields that can be updated
        allowed_fields = ['name', 'phone', 'avatar', 'vehicle', 'company']
        update_data = {k: v for k, v in data.items() if k in allowed_fields}
        
        if not update_data:
            return jsonify({'success': False, 'error': 'No valid fields to update'}), 400
        
        result = mongo.db.users.update_one(
            {'_id': ObjectId(user_id)},
            {'$set': update_data}
        )
        
        if result.modified_count == 0:
            return jsonify({'success': False, 'error': 'User not found or no changes made'}), 404
        
        # Get updated user
        user_data = mongo.db.users.find_one({'_id': ObjectId(user_id)})
        user = User.from_dict(user_data)
        
        return jsonify({'success': True, 'user': user.to_safe_dict()})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@auth_bp.route('/change-password', methods=['PUT'])
@jwt_required()
def change_password():
    """Change user password"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        current_password = data.get('currentPassword')
        new_password = data.get('newPassword')
        
        if not current_password or not new_password:
            return jsonify({'success': False, 'error': 'Current and new password are required'}), 400
        
        user_data = mongo.db.users.find_one({'_id': ObjectId(user_id)})
        
        if not user_data:
            return jsonify({'success': False, 'error': 'User not found'}), 404
        
        # Verify current password
        if not User.check_password(current_password, user_data['password']):
            return jsonify({'success': False, 'error': 'Current password is incorrect'}), 401
        
        # Update password
        new_hashed = User._hash_password(new_password)
        mongo.db.users.update_one(
            {'_id': ObjectId(user_id)},
            {'$set': {'password': new_hashed}}
        )
        
        return jsonify({'success': True, 'message': 'Password changed successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
