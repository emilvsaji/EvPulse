"""
EVPulse Database Package
========================
Advanced MongoDB database connection module with robust error handling,
connection pooling, health monitoring, and comprehensive diagnostics.

Usage:
    from database import init_db, get_db, get_collection
    
    # Initialize connection (call once at app startup)
    init_db()
    
    # Get database instance
    db = get_db()
    
    # Get a collection
    users = get_collection('users')
    
    # Or use the manager directly
    from database import get_database_manager
    manager = get_database_manager()
    
    # Health check
    health = manager.health_check()
    
    # Connection stats
    stats = manager.stats
"""

from .config import (
    MongoDBConfig,
    get_database_config,
    set_database_config,
    Environment,
)

from .connection import (
    DatabaseConnectionManager,
    get_database_manager,
    get_db,
    get_collection,
    init_db,
    close_db,
    with_db_retry,
    ConnectionState,
)

from .exceptions import (
    DatabaseException,
    ConnectionError,
    ConnectionPoolExhaustedError,
    ConnectionTimeoutError,
    AuthenticationError,
    SSLError,
    ServerSelectionError,
    OperationError,
    QueryError,
    WriteError,
    TransactionError,
    ConfigurationError,
    NetworkError,
    DatabaseNotInitializedError,
    RetryExhaustedError,
    classify_pymongo_error,
)

from .diagnostics import (
    DatabaseDiagnostics,
    DiagnosticResult,
    run_diagnostics,
    quick_test,
)

__all__ = [
    # Config
    'MongoDBConfig',
    'get_database_config',
    'set_database_config',
    'Environment',
    
    # Connection
    'DatabaseConnectionManager',
    'get_database_manager',
    'get_db',
    'get_collection',
    'init_db',
    'close_db',
    'with_db_retry',
    'ConnectionState',
    
    # Exceptions
    'DatabaseException',
    'ConnectionError',
    'ConnectionPoolExhaustedError',
    'ConnectionTimeoutError',
    'AuthenticationError',
    'SSLError',
    'ServerSelectionError',
    'OperationError',
    'QueryError',
    'WriteError',
    'TransactionError',
    'ConfigurationError',
    'NetworkError',
    'DatabaseNotInitializedError',
    'RetryExhaustedError',
    'classify_pymongo_error',
    
    # Diagnostics
    'DatabaseDiagnostics',
    'DiagnosticResult',
    'run_diagnostics',
    'quick_test',
]

__version__ = '2.0.0'
