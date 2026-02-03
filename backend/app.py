"""
EVPulse Flask Application
=========================
Main Flask application with advanced MongoDB database integration.
"""

import os
import logging
from datetime import datetime
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('evpulse')

# Initialize JWT
jwt = JWTManager()


def create_app(config_name: str = None) -> Flask:
    """
    Application factory for creating Flask app.
    
    Args:
        config_name: Configuration name ('development', 'production', 'testing')
    
    Returns:
        Configured Flask application
    """
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    # Create Flask app
    app = Flask(__name__)
    
    # Load configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 86400))
    app.config['JWT_TOKEN_LOCATION'] = ['headers']
    app.config['JWT_HEADER_NAME'] = 'Authorization'
    app.config['JWT_HEADER_TYPE'] = 'Bearer'
    
    # Initialize CORS
    CORS(app, origins=['http://localhost:5173', 'http://localhost:3000'], supports_credentials=True)
    
    # Initialize JWT
    jwt.init_app(app)
    
    # Initialize database connection
    db_initialized = _initialize_database(app)
    
    # Store database status in app config
    app.config['DATABASE_INITIALIZED'] = db_initialized
    
    # Register blueprints
    _register_blueprints(app)
    
    # Register routes
    _register_routes(app)
    
    return app


def _initialize_database(app: Flask) -> bool:
    """
    Initialize database connection with the new advanced database module.
    
    Args:
        app: Flask application instance
    
    Returns:
        bool: True if database initialized successfully
    """
    logger.info("=" * 60)
    logger.info("🔗 Initializing EVPulse Database Connection")
    logger.info("=" * 60)
    
    try:
        # Import the new database module
        from database import (
            init_db, 
            get_database_manager, 
            quick_test,
            run_diagnostics,
            MongoDBConfig,
            get_database_config
        )
        
        # Get configuration
        config = get_database_config()
        
        # Validate configuration
        is_valid, errors = config.validate()
        if not is_valid:
            logger.error("❌ Database configuration errors:")
            for error in errors:
                logger.error(f"   - {error}")
            return False
        
        logger.info(f"📋 Configuration: {config}")
        
        # Quick connection test first
        logger.info("🧪 Running quick connection test...")
        if quick_test():
            logger.info("✅ Quick test passed!")
        else:
            logger.warning("⚠️ Quick test failed, running full diagnostics...")
            diagnostics = run_diagnostics()
            if not diagnostics.get('all_passed', False):
                logger.error("❌ Diagnostics failed. Check suggestions above.")
                return False
        
        # Initialize the database connection
        logger.info("🚀 Establishing database connection...")
        manager = init_db(config)
        
        if manager.is_connected:
            logger.info("✅ Database connection established successfully!")
            
            # Get database stats
            db = manager.db
            collections = db.list_collection_names()
            logger.info(f"📂 Database: {config.database_name}")
            logger.info(f"📁 Collections: {collections}")
            
            # Initialize sample data if needed
            _initialize_sample_data(manager)
            
            # Store manager reference
            app.config['DB_MANAGER'] = manager
            
            return True
        else:
            logger.error("❌ Failed to establish database connection")
            return False
            
    except ImportError as e:
        logger.error(f"❌ Database module import error: {e}")
        logger.error("Make sure the 'database' package is in the backend directory")
        return False
        
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")
        
        # Run diagnostics to help troubleshoot
        try:
            from database import run_diagnostics
            logger.info("🔍 Running diagnostics to identify the issue...")
            run_diagnostics()
        except:
            pass
        
        return False


def _initialize_sample_data(manager) -> None:
    """
    Initialize database with sample data if collections are empty.
    
    Args:
        manager: Database connection manager
    """
    try:
        db = manager.db
        
        # Check if users exist
        user_count = db.users.count_documents({})
        
        if user_count == 0:
            logger.info("🌱 Database is empty, seeding with sample data...")
            
            # Try to run the seeder script
            try:
                import sys
                import os
                sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'scripts'))
                from seed_db import seed_database_data
                seed_database_data()
                logger.info("✅ Sample data seeded successfully!")
            except ImportError:
                logger.warning("⚠️ Seeder script not found, creating basic users...")
                _create_basic_users(db)
            except Exception as e:
                logger.warning(f"⚠️ Seeder failed: {e}, creating basic users...")
                _create_basic_users(db)
        else:
            logger.info(f"✅ Database already contains {user_count} user(s)")
            
    except Exception as e:
        logger.warning(f"⚠️ Sample data initialization failed: {e}")


def _create_basic_users(db) -> None:
    """
    Create basic test users.
    
    Args:
        db: Database instance
    """
    import bcrypt
    from bson import ObjectId
    
    users = [
        {
            '_id': ObjectId(),
            'email': 'admin@evpulse.com',
            'password': bcrypt.hashpw('admin123'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            'name': 'Admin User',
            'role': 'admin',
            'phone': '+1234567890',
            'is_active': True,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        },
        {
            '_id': ObjectId(),
            'email': 'operator@evpulse.com',
            'password': bcrypt.hashpw('operator123'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            'name': 'Station Operator',
            'role': 'operator',
            'phone': '+1234567891',
            'company': 'EV Solutions Inc',
            'is_active': True,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        },
        {
            '_id': ObjectId(),
            'email': 'user@evpulse.com',
            'password': bcrypt.hashpw('user123'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            'name': 'Test User',
            'role': 'user',
            'phone': '+1234567892',
            'vehicle': {'make': 'Tesla', 'model': 'Model 3', 'batteryCapacity': 75},
            'is_active': True,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
    ]
    
    db.users.insert_many(users)
    
    logger.info("✅ Created test users:")
    logger.info("   📧 admin@evpulse.com / admin123")
    logger.info("   📧 operator@evpulse.com / operator123")
    logger.info("   📧 user@evpulse.com / user123")


def _register_blueprints(app: Flask) -> None:
    """
    Register all Flask blueprints.
    
    Args:
        app: Flask application instance
    """
    try:
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
        
        logger.info("✅ All blueprints registered successfully")
        
    except ImportError as e:
        logger.error(f"❌ Failed to import blueprints: {e}")
        raise


def _register_routes(app: Flask) -> None:
    """
    Register application routes (health check, etc.).
    
    Args:
        app: Flask application instance
    """
    
    @app.route('/api/health')
    def health_check():
        """Health check endpoint with database status"""
        try:
            from database import get_database_manager
            
            manager = get_database_manager()
            
            if manager.is_connected:
                health = manager.health_check()
                stats = manager.stats
                
                # Get collection counts
                db = manager.db
                collection_stats = {}
                for collection in ['users', 'stations', 'sessions', 'bookings', 'transactions']:
                    try:
                        collection_stats[collection] = db[collection].count_documents({})
                    except:
                        collection_stats[collection] = 0
                
                return jsonify({
                    'status': 'healthy',
                    'message': 'EVPulse API is running',
                    'database': {
                        'status': 'connected',
                        'healthy': health.get('healthy', False),
                        'latency_ms': health.get('latency_ms'),
                        'state': manager.state,
                    },
                    'collections': collection_stats,
                    'stats': {
                        'uptime_seconds': stats.get('uptime_seconds', 0),
                        'queries_executed': stats.get('queries_executed', 0),
                        'reconnections': stats.get('reconnections', 0),
                    },
                    'timestamp': datetime.now().isoformat()
                })
            else:
                return jsonify({
                    'status': 'degraded',
                    'message': 'EVPulse API running but database not connected',
                    'database': {
                        'status': 'disconnected',
                        'state': manager.state,
                    },
                    'timestamp': datetime.now().isoformat()
                }), 503
                
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': str(e),
                'database': {'status': 'error'},
                'timestamp': datetime.now().isoformat()
            }), 500
    
    @app.route('/api/test')
    def test_endpoint():
        """Simple test endpoint"""
        return jsonify({
            'success': True,
            'message': 'EVPulse API test endpoint',
            'timestamp': datetime.now().isoformat()
        })
    
    @app.route('/api/db/status')
    def db_status():
        """Detailed database status endpoint"""
        try:
            from database import get_database_manager
            
            manager = get_database_manager()
            
            return jsonify({
                'connected': manager.is_connected,
                'state': manager.state,
                'stats': manager.stats,
                'health': manager.health_check() if manager.is_connected else None,
                'timestamp': datetime.now().isoformat()
            })
        except Exception as e:
            return jsonify({
                'connected': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }), 500
    
    @app.route('/api/db/diagnostics')
    def db_diagnostics():
        """Run database diagnostics"""
        try:
            from database import run_diagnostics
            results = run_diagnostics()
            return jsonify(results)
        except Exception as e:
            return jsonify({
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }), 500


# Global reference to the database for backward compatibility with routes
# This allows routes that use `from app import mongo` to continue working
class MongoProxy:
    """
    Proxy class for backward compatibility with flask-pymongo style access.
    Routes can use `mongo.db` as before.
    """
    
    @property
    def db(self):
        try:
            from database import get_db
            return get_db()
        except:
            return None
    
    @property
    def cx(self):
        try:
            from database import get_database_manager
            return get_database_manager().client
        except:
            return None


# Create mongo proxy for backward compatibility
mongo = MongoProxy()

# Mock data flag (set to False to use real database)
USE_MOCK_DATA = False


if __name__ == '__main__':
    app = create_app()
    
    print("\n" + "=" * 60)
    print("🚀 Starting EVPulse API Server")
    print("=" * 60)
    print("📍 Server: http://localhost:5000")
    print("📚 Health Check: http://localhost:5000/api/health")
    print("🔧 DB Status: http://localhost:5000/api/db/status")
    print("🔍 DB Diagnostics: http://localhost:5000/api/db/diagnostics")
    print("=" * 60 + "\n")
    
    app.run(debug=True, port=5000, host='0.0.0.0', use_reloader=False)
