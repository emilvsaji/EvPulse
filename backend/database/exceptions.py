"""
EVPulse Database Exceptions Module
==================================
Custom exception classes for comprehensive database error handling.
"""

from typing import Optional, Any, Dict


class DatabaseException(Exception):
    """Base exception for all database-related errors"""
    
    def __init__(
        self, 
        message: str, 
        error_code: Optional[str] = None,
        original_error: Optional[Exception] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message)
        self.message = message
        self.error_code = error_code or "DB_ERROR"
        self.original_error = original_error
        self.details = details or {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert exception to dictionary for API responses"""
        return {
            "error": self.error_code,
            "message": self.message,
            "details": self.details
        }
    
    def __str__(self) -> str:
        if self.original_error:
            return f"{self.message} (Original: {type(self.original_error).__name__}: {self.original_error})"
        return self.message


class ConnectionError(DatabaseException):
    """Raised when unable to establish database connection"""
    
    def __init__(
        self, 
        message: str = "Failed to connect to database",
        original_error: Optional[Exception] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=message,
            error_code="DB_CONNECTION_ERROR",
            original_error=original_error,
            details=details
        )


class ConnectionPoolExhaustedError(DatabaseException):
    """Raised when connection pool is exhausted"""
    
    def __init__(
        self, 
        message: str = "Database connection pool exhausted",
        pool_size: int = 0,
        active_connections: int = 0
    ):
        super().__init__(
            message=message,
            error_code="DB_POOL_EXHAUSTED",
            details={
                "pool_size": pool_size,
                "active_connections": active_connections
            }
        )


class ConnectionTimeoutError(DatabaseException):
    """Raised when connection times out"""
    
    def __init__(
        self, 
        message: str = "Database connection timed out",
        timeout_ms: int = 0,
        original_error: Optional[Exception] = None
    ):
        super().__init__(
            message=message,
            error_code="DB_CONNECTION_TIMEOUT",
            original_error=original_error,
            details={"timeout_ms": timeout_ms}
        )


class AuthenticationError(DatabaseException):
    """Raised when database authentication fails"""
    
    def __init__(
        self, 
        message: str = "Database authentication failed",
        original_error: Optional[Exception] = None
    ):
        super().__init__(
            message=message,
            error_code="DB_AUTH_ERROR",
            original_error=original_error
        )


class SSLError(DatabaseException):
    """Raised when SSL/TLS connection fails"""
    
    def __init__(
        self, 
        message: str = "SSL/TLS connection error",
        original_error: Optional[Exception] = None
    ):
        super().__init__(
            message=message,
            error_code="DB_SSL_ERROR",
            original_error=original_error
        )


class ServerSelectionError(DatabaseException):
    """Raised when no suitable server is found"""
    
    def __init__(
        self, 
        message: str = "No suitable database server found",
        original_error: Optional[Exception] = None
    ):
        super().__init__(
            message=message,
            error_code="DB_SERVER_SELECTION_ERROR",
            original_error=original_error
        )


class OperationError(DatabaseException):
    """Raised when a database operation fails"""
    
    def __init__(
        self, 
        message: str = "Database operation failed",
        operation: str = "unknown",
        collection: Optional[str] = None,
        original_error: Optional[Exception] = None
    ):
        super().__init__(
            message=message,
            error_code="DB_OPERATION_ERROR",
            original_error=original_error,
            details={
                "operation": operation,
                "collection": collection
            }
        )


class QueryError(DatabaseException):
    """Raised when a query execution fails"""
    
    def __init__(
        self, 
        message: str = "Query execution failed",
        query: Optional[Dict] = None,
        collection: Optional[str] = None,
        original_error: Optional[Exception] = None
    ):
        super().__init__(
            message=message,
            error_code="DB_QUERY_ERROR",
            original_error=original_error,
            details={
                "query": str(query)[:200] if query else None,  # Truncate for safety
                "collection": collection
            }
        )


class WriteError(DatabaseException):
    """Raised when a write operation fails"""
    
    def __init__(
        self, 
        message: str = "Write operation failed",
        collection: Optional[str] = None,
        write_concern: Optional[str] = None,
        original_error: Optional[Exception] = None
    ):
        super().__init__(
            message=message,
            error_code="DB_WRITE_ERROR",
            original_error=original_error,
            details={
                "collection": collection,
                "write_concern": write_concern
            }
        )


class TransactionError(DatabaseException):
    """Raised when a transaction fails"""
    
    def __init__(
        self, 
        message: str = "Transaction failed",
        transaction_id: Optional[str] = None,
        original_error: Optional[Exception] = None
    ):
        super().__init__(
            message=message,
            error_code="DB_TRANSACTION_ERROR",
            original_error=original_error,
            details={"transaction_id": transaction_id}
        )


class ConfigurationError(DatabaseException):
    """Raised when database configuration is invalid"""
    
    def __init__(
        self, 
        message: str = "Invalid database configuration",
        config_errors: Optional[list] = None
    ):
        super().__init__(
            message=message,
            error_code="DB_CONFIG_ERROR",
            details={"config_errors": config_errors or []}
        )


class NetworkError(DatabaseException):
    """Raised when network-related issues occur"""
    
    def __init__(
        self, 
        message: str = "Network error occurred",
        host: Optional[str] = None,
        port: Optional[int] = None,
        original_error: Optional[Exception] = None
    ):
        super().__init__(
            message=message,
            error_code="DB_NETWORK_ERROR",
            original_error=original_error,
            details={
                "host": host,
                "port": port
            }
        )


class DatabaseNotInitializedError(DatabaseException):
    """Raised when database is accessed before initialization"""
    
    def __init__(
        self, 
        message: str = "Database has not been initialized"
    ):
        super().__init__(
            message=message,
            error_code="DB_NOT_INITIALIZED"
        )


class RetryExhaustedError(DatabaseException):
    """Raised when all retry attempts have been exhausted"""
    
    def __init__(
        self, 
        message: str = "All retry attempts exhausted",
        attempts: int = 0,
        last_error: Optional[Exception] = None
    ):
        super().__init__(
            message=message,
            error_code="DB_RETRY_EXHAUSTED",
            original_error=last_error,
            details={"attempts": attempts}
        )


def classify_pymongo_error(error: Exception) -> DatabaseException:
    """
    Classify a PyMongo exception into our custom exception hierarchy.
    This helps with consistent error handling across the application.
    """
    from pymongo.errors import (
        ServerSelectionTimeoutError as PyMongoServerSelectionError,
        ConnectionFailure as PyMongoConnectionFailure,
        ConfigurationError as PyMongoConfigError,
        OperationFailure,
        WriteError as PyMongoWriteError,
        NetworkTimeout,
        AutoReconnect,
    )
    
    error_str = str(error).lower()
    
    # Server selection timeout
    if isinstance(error, PyMongoServerSelectionError):
        return ServerSelectionError(
            message="Could not find a suitable MongoDB server. Check if cluster is active and IP is whitelisted.",
            original_error=error
        )
    
    # Connection failures
    if isinstance(error, (PyMongoConnectionFailure, AutoReconnect)):
        if "authentication" in error_str or "auth" in error_str:
            return AuthenticationError(
                message="MongoDB authentication failed. Check username and password.",
                original_error=error
            )
        if "ssl" in error_str or "tls" in error_str or "certificate" in error_str:
            return SSLError(
                message="SSL/TLS connection error. Check certificate settings.",
                original_error=error
            )
        return ConnectionError(
            message="Failed to connect to MongoDB. Check connection settings.",
            original_error=error
        )
    
    # Configuration errors
    if isinstance(error, PyMongoConfigError):
        return ConfigurationError(
            message=f"MongoDB configuration error: {error}",
            config_errors=[str(error)]
        )
    
    # Network timeout
    if isinstance(error, NetworkTimeout):
        return ConnectionTimeoutError(
            message="MongoDB operation timed out",
            original_error=error
        )
    
    # Write errors
    if isinstance(error, PyMongoWriteError):
        return WriteError(
            message="MongoDB write operation failed",
            original_error=error
        )
    
    # Operation failures
    if isinstance(error, OperationFailure):
        if "authentication" in error_str:
            return AuthenticationError(
                message="MongoDB authentication failed",
                original_error=error
            )
        return OperationError(
            message=f"MongoDB operation failed: {error}",
            original_error=error
        )
    
    # Catch-all for unknown errors
    return DatabaseException(
        message=f"Database error: {error}",
        original_error=error
    )
