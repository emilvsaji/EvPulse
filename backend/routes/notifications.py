from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import mongo
from models.notification import Notification
from bson import ObjectId
from datetime import datetime

notifications_bp = Blueprint('notifications', __name__)

@notifications_bp.route('/user/<user_id>', methods=['GET'])
@jwt_required()
def get_user_notifications(user_id):
    """Get all notifications for a user"""
    try:
        notifications_data = list(mongo.db.notifications.find({'user_id': user_id}).sort('timestamp', -1))
        notifications = [Notification.from_dict(data).to_response_dict() for data in notifications_data]
        
        return jsonify({'success': True, 'data': notifications})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@notifications_bp.route('/<notification_id>/read', methods=['PUT'])
@jwt_required()
def mark_as_read(notification_id):
    """Mark a notification as read"""
    try:
        result = mongo.db.notifications.update_one(
            {'_id': ObjectId(notification_id)},
            {'$set': {'read': True}}
        )
        
        if result.modified_count == 0:
            return jsonify({'success': False, 'error': 'Notification not found'}), 404
        
        return jsonify({'success': True, 'message': 'Notification marked as read'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@notifications_bp.route('/user/<user_id>/read-all', methods=['PUT'])
@jwt_required()
def mark_all_as_read(user_id):
    """Mark all notifications as read for a user"""
    try:
        mongo.db.notifications.update_many(
            {'user_id': user_id, 'read': False},
            {'$set': {'read': True}}
        )
        
        return jsonify({'success': True, 'message': 'All notifications marked as read'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@notifications_bp.route('/<notification_id>', methods=['DELETE'])
@jwt_required()
def delete_notification(notification_id):
    """Delete a notification"""
    try:
        user_id = get_jwt_identity()
        
        notification = mongo.db.notifications.find_one({'_id': ObjectId(notification_id)})
        if not notification:
            return jsonify({'success': False, 'error': 'Notification not found'}), 404
        
        if notification['user_id'] != user_id:
            return jsonify({'success': False, 'error': 'Unauthorized'}), 403
        
        mongo.db.notifications.delete_one({'_id': ObjectId(notification_id)})
        
        return jsonify({'success': True, 'message': 'Notification deleted'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@notifications_bp.route('/user/<user_id>/unread-count', methods=['GET'])
@jwt_required()
def get_unread_count(user_id):
    """Get count of unread notifications"""
    try:
        count = mongo.db.notifications.count_documents({
            'user_id': user_id,
            'read': False
        })
        
        return jsonify({'success': True, 'data': {'count': count}})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
