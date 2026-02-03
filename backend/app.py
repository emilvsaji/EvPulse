import os
from datetime import datetime
from flask import Flask, jsonify
from flask_cors import CORS
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager
from config import config

# Initialize extensions
mongo = PyMongo()
jwt = JWTManager()

def initialize_database():
    """Initialize database with sample data if collections are empty"""
    try:
        # Check if database is available by trying to access it
        if mongo.db is None:
            print("⚠️ Skipping database initialization - MongoDB not connected")
            return
            
        # Try to access a collection to test if connection is working
        mongo.db.users.find_one({}, limit=1)
        
        # Check if users collection exists and has data
        if mongo.db.users.count_documents({}) == 0:
            print("🌱 Initializing database with sample data...")
            
            # Import and run the database seeder
            import sys
            import os
            sys.path.append(os.path.join(os.path.dirname(__file__), 'scripts'))
            
            try:
                from seed_db import seed_database_data
                seed_database_data()
                print("✅ Database initialized with sample data successfully!")
            except ImportError:
                print("⚠️ Seeder not found, creating basic data...")
                create_basic_data()
        else:
            print("✅ Database already contains data")
            
    except Exception as e:
        print(f"⚠️ Database initialization failed: {e}")
        print("🚨 MongoDB connection not available - running in offline mode")

def create_basic_data():
    """Create basic data if seeder is not available"""
    from datetime import datetime
    from bson import ObjectId
    import bcrypt
    
    # Create sample users
    users_data = [
        {
            '_id': ObjectId(),
            'email': 'user@evpulse.com',
            'password': bcrypt.hashpw('user123'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            'name': 'John Doe',
            'role': 'user',
            'phone': '+1 234 567 8900',
            'vehicle': {
                'make': 'Tesla',
                'model': 'Model 3',
                'batteryCapacity': 75,
                'range': 350
            },
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        },
        {
            '_id': ObjectId(),
            'email': 'operator@evpulse.com',
            'password': bcrypt.hashpw('operator123'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            'name': 'Sarah Wilson',
            'role': 'operator',
            'phone': '+1 234 567 8901',
            'company': 'GreenCharge Inc.',
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        },
        {
            '_id': ObjectId(),
            'email': 'admin@evpulse.com',
            'password': bcrypt.hashpw('admin123'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            'name': 'Mike Anderson',
            'role': 'admin',
            'phone': '+1 234 567 8902',
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
    ]
    
    # Insert users
    mongo.db.users.insert_many(users_data)
    
    # Create sample stations
    stations_data = [
        {
            '_id': ObjectId(),
            'name': 'GreenCharge Hub',
            'address': '123 Electric Ave, Downtown',
            'city': 'San Francisco',
            'coordinates': {'lat': 37.7749, 'lng': -122.4194},
            'operator_id': str(users_data[1]['_id']),  # Operator user
            'status': 'available',
            'rating': 4.8,
            'total_reviews': 256,
            'amenities': ['WiFi', 'Restroom', 'Cafe', 'Parking'],
            'operating_hours': '24/7',
            'ports': [
                {'id': 1, 'type': 'Fast DC', 'power': 150, 'status': 'available', 'price': 0.35},
                {'id': 2, 'type': 'Fast DC', 'power': 150, 'status': 'busy', 'price': 0.35},
                {'id': 3, 'type': 'Normal AC', 'power': 22, 'status': 'available', 'price': 0.25},
                {'id': 4, 'type': 'Normal AC', 'power': 22, 'status': 'offline', 'price': 0.25}
            ],
            'pricing': {
                'normal': {'base': 0.25, 'peak': 0.32},
                'fast': {'base': 0.35, 'peak': 0.45}
            },
            'peak_hours': {'start': '18:00', 'end': '21:00'},
            'image': 'https://images.unsplash.com/photo-1593941707882-a5bba14938c7?w=400',
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        },
        {
            '_id': ObjectId(),
            'name': 'PowerGrid Station',
            'address': '456 Volt Street, Tech Park',
            'city': 'San Francisco',
            'coordinates': {'lat': 37.7849, 'lng': -122.4094},
            'operator_id': str(users_data[1]['_id']),  # Operator user
            'status': 'available',
            'rating': 4.6,
            'total_reviews': 189,
            'amenities': ['WiFi', 'Parking', 'Shop'],
            'operating_hours': '6:00 AM - 11:00 PM',
            'ports': [
                {'id': 5, 'type': 'Fast DC', 'power': 350, 'status': 'available', 'price': 0.45},
                {'id': 6, 'type': 'Fast DC', 'power': 350, 'status': 'available', 'price': 0.45},
                {'id': 7, 'type': 'Normal AC', 'power': 22, 'status': 'busy', 'price': 0.22}
            ],
            'pricing': {
                'normal': {'base': 0.22, 'peak': 0.28},
                'fast': {'base': 0.45, 'peak': 0.55}
            },
            'peak_hours': {'start': '17:00', 'end': '20:00'},
            'image': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400',
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        },
        {
            '_id': ObjectId(),
            'name': 'EcoCharge Plaza',
            'address': '789 Green Road, Mall Center',
            'city': 'San Francisco',
            'coordinates': {'lat': 37.7649, 'lng': -122.4294},
            'operator_id': str(users_data[1]['_id']),  # Operator user
            'status': 'busy',
            'rating': 4.4,
            'total_reviews': 134,
            'amenities': ['WiFi', 'Restroom', 'Parking', 'Shop'],
            'operating_hours': '24/7',
            'ports': [
                {'id': 8, 'type': 'Fast DC', 'power': 250, 'status': 'busy', 'price': 0.40},
                {'id': 9, 'type': 'Normal AC', 'power': 22, 'status': 'available', 'price': 0.20},
                {'id': 10, 'type': 'Normal AC', 'power': 22, 'status': 'available', 'price': 0.20}
            ],
            'pricing': {
                'normal': {'base': 0.20, 'peak': 0.25},
                'fast': {'base': 0.40, 'peak': 0.50}
            },
            'peak_hours': {'start': '16:00', 'end': '19:00'},
            'image': 'https://images.unsplash.com/photo-1593941707882-a5bba14938c7?w=400',
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
    ]
    
    # Insert stations
    mongo.db.stations.insert_many(stations_data)

def create_app(config_name=None):
    """Application factory"""
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    CORS(app, origins=['http://localhost:5173', 'http://localhost:3000'], supports_credentials=True)
    
    # Initialize MongoDB connection properly
    try:
        mongo.init_app(app)
        print("✅ MongoDB extension initialized")
    except Exception as e:
        print(f"⚠️ MongoDB initialization error: {e}")
    
    print("🔗 Attempting to connect to MongoDB Atlas (timeout: 5s)...")
    try:
        with app.app_context():
            # Test connection by trying to access the database with shorter timeout
            if mongo.db is not None:
                collections = mongo.db.list_collection_names()
                print("✅ MongoDB Atlas connected successfully!")
                print(f"📊 Found collections: {collections}")
                
                # Initialize database with sample data if empty
                initialize_database()
            else:
                print("⚠️ MongoDB connection not available")
                
    except Exception as e:
        print(f"⚠️ Initial connection test failed: {str(e)[:200]}...")
        print("🔄 Continuing with delayed initialization...")
        print("📝 The app will attempt to connect when API endpoints are called")
        print("\n📋 Possible causes:")
        print("   1. MongoDB Atlas cluster is PAUSED (most likely)")
        print("   2. IP address not whitelisted in Atlas Network Access")
        print("   3. SSL/TLS connection issues with Python 3.13")
        print("\n🔧 To fix:")
        print("   • Login to MongoDB Atlas: https://cloud.mongodb.com/")
        print("   • Resume the cluster if paused")
        print("   • Add 0.0.0.0/0 to Network Access IP whitelist")
        
        # Initialize sample data in background (will be skipped if mongo.db is None)
        try:
            with app.app_context():
                initialize_database()
                print("✅ Database initialization completed!")
        except Exception as init_error:
            print(f"⚠️ Database initialization deferred: {init_error}")
            print("🚨 Backend will run in offline mode - database operations will return errors")
    
    jwt.init_app(app)
    
    # Register blueprints
    from routes.auth import auth_bp
    from routes.stations import stations_bp
    from routes.sessions import sessions_bp
    from routes.bookings import bookings_bp
    from routes.transactions import transactions_bp
    from routes.reviews import reviews_bp
    from routes.notifications import notifications_bp
    from routes.admin import admin_bp
    from routes.operator import operator_bp
    from routes.users import users_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(stations_bp, url_prefix='/api/stations')
    app.register_blueprint(sessions_bp, url_prefix='/api/sessions')
    app.register_blueprint(bookings_bp, url_prefix='/api/bookings')
    app.register_blueprint(transactions_bp, url_prefix='/api/transactions')
    app.register_blueprint(reviews_bp, url_prefix='/api/reviews')
    app.register_blueprint(notifications_bp, url_prefix='/api/notifications')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(operator_bp, url_prefix='/api/operator')
    app.register_blueprint(users_bp, url_prefix='/api/users')
    
    # Health check endpoint
    @app.route('/api/health')
    def health_check():
        try:
            # Test database connection
            if mongo.db is not None:
                mongo.db.command('ping')
                db_status = 'connected'
                
                # Get database stats
                stats = {
                    'users': mongo.db.users.count_documents({}),
                    'stations': mongo.db.stations.count_documents({}),
                    'sessions': mongo.db.sessions.count_documents({}) if 'sessions' in mongo.db.list_collection_names() else 0
                }
            else:
                db_status = 'disconnected: mongo.db is None'
                stats = {}
        except Exception as e:
            db_status = f'disconnected: {str(e)}'
            stats = {}
            
        return {
            'status': 'healthy',
            'message': 'EVPulse API is running',
            'database': db_status,
            'collections': stats,
            'timestamp': datetime.now().isoformat()
        }
    
    # Simple test endpoint
    @app.route('/api/test')
    def test_endpoint():
        return {'success': True, 'message': 'Test endpoint working', 'timestamp': datetime.now().isoformat()}
    
    return app

if __name__ == '__main__':
    app = create_app()
    print("🚀 Starting EVPulse API server...")
    app.run(debug=True, port=5000, host='0.0.0.0', use_reloader=False)
