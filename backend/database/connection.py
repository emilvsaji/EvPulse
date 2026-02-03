"""
EVPulse Database Connection Manager
===================================
Advanced MongoDB connection manager with:
- Connection pooling
- Automatic retry with exponential backoff
- Health monitoring
- Graceful reconnection
- Thread-safe singleton pattern
"""

import time
import threading
import logging
import atexit
from datetime import datetime
from typing import Optional, Dict, Any, Callable, TypeVar, ParamSpec
from functools import wraps
from contextlib import contextmanager

from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from pymongo.errors import (
    ServerSelectionTimeoutError,
    ConnectionFailure,
    AutoReconnect,
    NetworkTimeout,
    OperationFailure,
)

from .config import MongoDBConfig, get_database_config
from .exceptions import (
    DatabaseException,
    ConnectionError,
    ConnectionTimeoutError,
    AuthenticationError,
    ServerSelectionError,
    DatabaseNotInitializedError,
    RetryExhaustedError,
    ConfigurationError,
    classify_pymongo_error,
)

# Type variables for generic retry decorator
P = ParamSpec('P')
T = TypeVar('T')

# Configure logging
logger = logging.getLogger('evpulse.database')


class ConnectionState:
    """Enum-like class for connection states"""
    DISCONNECTED = "disconnected"
    CONNECTING = "connecting"
    CONNECTED = "connected"
    RECONNECTING = "reconnecting"
    ERROR = "error"


class DatabaseConnectionManager:
    """
    Singleton MongoDB Connection Manager.
    
    Provides a robust, thread-safe connection to MongoDB with:
    - Automatic connection pooling (handled by PyMongo)
    - Health monitoring
    - Graceful reconnection
    - Retry logic with exponential backoff
    """
    
    _instance: Optional['DatabaseConnectionManager'] = None
    _lock = threading.Lock()
    
    def __new__(cls):
        """Singleton pattern with thread-safe double-check locking"""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initialize the connection manager (only runs once due to singleton)"""
        if self._initialized:
            return
        
        self._client: Optional[MongoClient] = None
        self._db: Optional[Database] = None
        self._config: Optional[MongoDBConfig] = None
        self._state: str = ConnectionState.DISCONNECTED
        self._last_error: Optional[Exception] = None
        self._connection_time: Optional[datetime] = None
        self._health_check_interval: int = 30  # seconds
        self._health_check_thread: Optional[threading.Thread] = None
        self._stop_health_check = threading.Event()
        self._connection_lock = threading.RLock()
        self._stats = {
            'connections_made': 0,
            'connection_failures': 0,
            'reconnections': 0,
            'queries_executed': 0,
            'last_health_check': None,
            'health_check_failures': 0,
        }
        
        # Register cleanup on exit
        atexit.register(self._cleanup)
        
        self._initialized = True
        logger.info("DatabaseConnectionManager initialized")
    
    @property
    def is_connected(self) -> bool:
        """Check if currently connected to database"""
        return self._state == ConnectionState.CONNECTED and self._client is not None
    
    @property
    def state(self) -> str:
        """Get current connection state"""
        return self._state
    
    @property
    def db(self) -> Database:
        """
        Get the database instance.
        Raises DatabaseNotInitializedError if not connected.
        """
        if self._db is None:
            raise DatabaseNotInitializedError(
                "Database not initialized. Call connect() first."
            )
        return self._db
    
    @property
    def client(self) -> MongoClient:
        """
        Get the MongoDB client instance.
        Raises DatabaseNotInitializedError if not connected.
        """
        if self._client is None:
            raise DatabaseNotInitializedError(
                "Database not initialized. Call connect() first."
            )
        return self._client
    
    @property
    def stats(self) -> Dict[str, Any]:
        """Get connection statistics"""
        return {
            **self._stats,
            'state': self._state,
            'connection_time': self._connection_time.isoformat() if self._connection_time else None,
            'uptime_seconds': (datetime.utcnow() - self._connection_time).total_seconds() if self._connection_time else 0,
        }
    
    def connect(
        self, 
        config: Optional[MongoDBConfig] = None,
        auto_health_check: bool = True
    ) -> bool:
        """
        Establish connection to MongoDB.
        
        Args:
            config: Optional MongoDBConfig. Uses environment config if not provided.
            auto_health_check: Whether to start automatic health checking.
        
        Returns:
            bool: True if connection successful.
        
        Raises:
            ConfigurationError: If configuration is invalid.
            ConnectionError: If unable to connect.
        """
        with self._connection_lock:
            # If already connected with same config, return
            if self.is_connected and config is None:
                logger.debug("Already connected to database")
                return True
            
            # Get configuration
            self._config = config or get_database_config()
            
            # Validate configuration
            is_valid, errors = self._config.validate()
            if not is_valid:
                raise ConfigurationError(
                    message="Invalid database configuration",
                    config_errors=errors
                )
            
            self._state = ConnectionState.CONNECTING
            logger.info(f"Connecting to MongoDB: {self._config}")
            
            try:
                # Build connection options
                options = self._config.get_connection_options()
                
                # Create MongoDB client
                self._client = MongoClient(
                    self._config.uri,
                    **options
                )
                
                # Test connection with ping
                self._client.admin.command('ping')
                
                # Get database
                self._db = self._client[self._config.database_name]
                
                # Update state
                self._state = ConnectionState.CONNECTED
                self._connection_time = datetime.utcnow()
                self._stats['connections_made'] += 1
                self._last_error = None
                
                logger.info(f"✅ Successfully connected to MongoDB database: {self._config.database_name}")
                
                # Start health check if enabled
                if auto_health_check:
                    self._start_health_check()
                
                return True
                
            except Exception as e:
                self._state = ConnectionState.ERROR
                self._last_error = e
                self._stats['connection_failures'] += 1
                
                # Convert to our exception type
                db_error = classify_pymongo_error(e)
                logger.error(f"❌ Failed to connect to MongoDB: {db_error}")
                raise db_error
    
    def disconnect(self) -> None:
        """Gracefully disconnect from MongoDB"""
        with self._connection_lock:
            logger.info("Disconnecting from MongoDB...")
            
            # Stop health check
            self._stop_health_check.set()
            if self._health_check_thread and self._health_check_thread.is_alive():
                self._health_check_thread.join(timeout=5)
            
            # Close client
            if self._client:
                try:
                    self._client.close()
                except Exception as e:
                    logger.warning(f"Error closing MongoDB client: {e}")
            
            self._client = None
            self._db = None
            self._state = ConnectionState.DISCONNECTED
            self._connection_time = None
            
            logger.info("✅ Disconnected from MongoDB")
    
    def reconnect(self) -> bool:
        """
        Attempt to reconnect to MongoDB.
        Uses exponential backoff for retry attempts.
        """
        with self._connection_lock:
            self._state = ConnectionState.RECONNECTING
            self._stats['reconnections'] += 1
            
            logger.info("Attempting to reconnect to MongoDB...")
            
            # Close existing connection if any
            if self._client:
                try:
                    self._client.close()
                except:
                    pass
                self._client = None
                self._db = None
            
            # Retry connection
            max_attempts = self._config.max_retry_attempts if self._config else 3
            delay = self._config.retry_delay_seconds if self._config else 1.0
            backoff = self._config.retry_backoff_multiplier if self._config else 2.0
            
            last_error = None
            for attempt in range(max_attempts):
                try:
                    self._state = ConnectionState.CONNECTING
                    return self.connect(self._config, auto_health_check=True)
                except Exception as e:
                    last_error = e
                    logger.warning(f"Reconnection attempt {attempt + 1}/{max_attempts} failed: {e}")
                    
                    if attempt < max_attempts - 1:
                        time.sleep(delay)
                        delay *= backoff
            
            self._state = ConnectionState.ERROR
            raise RetryExhaustedError(
                message="Failed to reconnect after multiple attempts",
                attempts=max_attempts,
                last_error=last_error
            )
    
    def health_check(self) -> Dict[str, Any]:
        """
        Perform health check on the database connection.
        
        Returns:
            Dict with health check results.
        """
        result = {
            'timestamp': datetime.utcnow().isoformat(),
            'state': self._state,
            'healthy': False,
            'latency_ms': None,
            'error': None,
        }
        
        if not self._client:
            result['error'] = "No client connection"
            return result
        
        try:
            start = time.time()
            self._client.admin.command('ping')
            latency = (time.time() - start) * 1000
            
            result['healthy'] = True
            result['latency_ms'] = round(latency, 2)
            self._stats['last_health_check'] = datetime.utcnow()
            
        except Exception as e:
            result['healthy'] = False
            result['error'] = str(e)
            self._stats['health_check_failures'] += 1
            logger.warning(f"Health check failed: {e}")
        
        return result
    
    def _start_health_check(self) -> None:
        """Start background health check thread"""
        self._stop_health_check.clear()
        
        def health_check_loop():
            while not self._stop_health_check.is_set():
                try:
                    check = self.health_check()
                    if not check['healthy'] and self._state == ConnectionState.CONNECTED:
                        logger.warning("Health check failed, attempting reconnection...")
                        try:
                            self.reconnect()
                        except Exception as e:
                            logger.error(f"Reconnection failed: {e}")
                except Exception as e:
                    logger.error(f"Error in health check loop: {e}")
                
                self._stop_health_check.wait(self._health_check_interval)
        
        self._health_check_thread = threading.Thread(
            target=health_check_loop,
            daemon=True,
            name="mongodb-health-check"
        )
        self._health_check_thread.start()
        logger.debug("Started health check background thread")
    
    def _cleanup(self) -> None:
        """Cleanup resources on exit"""
        try:
            self.disconnect()
        except:
            pass
    
    def get_collection(self, name: str) -> Collection:
        """
        Get a collection from the database.
        
        Args:
            name: Collection name.
        
        Returns:
            PyMongo Collection object.
        """
        return self.db[name]
    
    def execute_with_retry(
        self,
        operation: Callable[[], T],
        max_retries: Optional[int] = None,
        retry_on: tuple = (AutoReconnect, NetworkTimeout, ConnectionFailure),
    ) -> T:
        """
        Execute a database operation with automatic retry.
        
        Args:
            operation: Callable that performs the database operation.
            max_retries: Maximum retry attempts (uses config default if None).
            retry_on: Tuple of exception types to retry on.
        
        Returns:
            Result of the operation.
        """
        max_attempts = max_retries or (self._config.max_retry_attempts if self._config else 3)
        delay = self._config.retry_delay_seconds if self._config else 1.0
        backoff = self._config.retry_backoff_multiplier if self._config else 2.0
        
        last_error = None
        for attempt in range(max_attempts):
            try:
                result = operation()
                self._stats['queries_executed'] += 1
                return result
            except retry_on as e:
                last_error = e
                logger.warning(f"Operation failed (attempt {attempt + 1}/{max_attempts}): {e}")
                
                if attempt < max_attempts - 1:
                    time.sleep(delay)
                    delay *= backoff
                    
                    # Check connection and reconnect if needed
                    if not self.is_connected:
                        try:
                            self.reconnect()
                        except:
                            pass
        
        raise RetryExhaustedError(
            message="Database operation failed after retries",
            attempts=max_attempts,
            last_error=last_error
        )
    
    @contextmanager
    def transaction(self):
        """
        Context manager for MongoDB transactions.
        Note: Requires MongoDB replica set.
        
        Usage:
            with db_manager.transaction() as session:
                collection.insert_one({...}, session=session)
                collection.update_one({...}, {...}, session=session)
        """
        if not self._client:
            raise DatabaseNotInitializedError()
        
        with self._client.start_session() as session:
            with session.start_transaction():
                yield session


# Retry decorator for database operations
def with_db_retry(
    max_retries: int = 3,
    retry_on: tuple = (AutoReconnect, NetworkTimeout, ConnectionFailure),
):
    """
    Decorator to add retry logic to database operations.
    
    Usage:
        @with_db_retry(max_retries=3)
        def my_db_operation():
            return db.collection.find_one({})
    """
    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            manager = get_database_manager()
            return manager.execute_with_retry(
                lambda: func(*args, **kwargs),
                max_retries=max_retries,
                retry_on=retry_on
            )
        return wrapper
    return decorator


# Global manager instance
_manager: Optional[DatabaseConnectionManager] = None


def get_database_manager() -> DatabaseConnectionManager:
    """Get the global database connection manager instance"""
    global _manager
    if _manager is None:
        _manager = DatabaseConnectionManager()
    return _manager


def get_db() -> Database:
    """
    Convenience function to get the database instance.
    Equivalent to get_database_manager().db
    """
    return get_database_manager().db


def get_collection(name: str) -> Collection:
    """
    Convenience function to get a collection.
    Equivalent to get_database_manager().get_collection(name)
    """
    return get_database_manager().get_collection(name)


def init_db(config: Optional[MongoDBConfig] = None) -> DatabaseConnectionManager:
    """
    Initialize database connection.
    
    Args:
        config: Optional MongoDBConfig. Uses environment config if not provided.
    
    Returns:
        DatabaseConnectionManager instance.
    """
    manager = get_database_manager()
    manager.connect(config)
    return manager


def close_db() -> None:
    """Close database connection"""
    manager = get_database_manager()
    manager.disconnect()
