"""
EVPulse Database Configuration Module
=====================================
Advanced configuration for MongoDB connection with environment-based settings.
Supports development, testing, and production environments.
"""

import os
from dataclasses import dataclass, field
from typing import Optional, Dict, Any
from enum import Enum


class Environment(Enum):
    """Application environment types"""
    DEVELOPMENT = "development"
    TESTING = "testing"
    PRODUCTION = "production"


@dataclass
class MongoDBConfig:
    """
    MongoDB Configuration with all connection parameters.
    Provides sensible defaults with full customization support.
    """
    # Connection URI - REQUIRED
    uri: str = ""
    
    # Database name
    database_name: str = "evpulse"
    
    # Connection Pool Settings
    min_pool_size: int = 5
    max_pool_size: int = 50
    max_idle_time_ms: int = 30000  # 30 seconds
    
    # Timeout Settings (in milliseconds)
    server_selection_timeout_ms: int = 30000  # 30 seconds
    connect_timeout_ms: int = 20000  # 20 seconds
    socket_timeout_ms: int = 30000  # 30 seconds
    
    # Retry Settings
    retry_writes: bool = True
    retry_reads: bool = True
    max_retry_attempts: int = 3
    retry_delay_seconds: float = 1.0
    retry_backoff_multiplier: float = 2.0
    
    # SSL/TLS Settings
    tls_enabled: bool = True
    tls_allow_invalid_certificates: bool = False
    tls_allow_invalid_hostnames: bool = False
    tls_ca_file: Optional[str] = None
    
    # Write Concern
    write_concern_w: str = "majority"
    write_concern_j: bool = True
    write_concern_wtimeout: int = 5000
    
    # Read Preference
    read_preference: str = "primaryPreferred"
    
    # Application Name (for monitoring)
    app_name: str = "EVPulse"
    
    # Compression
    compressors: list = field(default_factory=lambda: ["zstd", "snappy", "zlib"])
    
    # Health Check Settings
    heartbeat_frequency_ms: int = 10000  # 10 seconds
    
    # Debug Settings
    debug_mode: bool = False
    log_queries: bool = False
    
    @classmethod
    def from_environment(cls) -> 'MongoDBConfig':
        """
        Create configuration from environment variables.
        Environment variables take precedence over defaults.
        """
        # Load dotenv if available
        try:
            from dotenv import load_dotenv
            load_dotenv()
        except ImportError:
            pass
        
        # Get MongoDB URI - this is REQUIRED
        uri = os.getenv('MONGODB_URI', '')
        
        # Parse database name from URI if present, otherwise use env or default
        db_name = os.getenv('MONGODB_DATABASE', 'evpulse')
        
        # Determine environment
        env = os.getenv('FLASK_ENV', 'development').lower()
        is_production = env == 'production'
        is_development = env == 'development'
        
        return cls(
            uri=uri,
            database_name=db_name,
            
            # Pool settings - adjust based on environment
            min_pool_size=int(os.getenv('MONGODB_MIN_POOL_SIZE', '5' if is_production else '2')),
            max_pool_size=int(os.getenv('MONGODB_MAX_POOL_SIZE', '100' if is_production else '20')),
            max_idle_time_ms=int(os.getenv('MONGODB_MAX_IDLE_TIME_MS', '30000')),
            
            # Timeout settings
            server_selection_timeout_ms=int(os.getenv('MONGODB_SERVER_SELECTION_TIMEOUT_MS', '30000')),
            connect_timeout_ms=int(os.getenv('MONGODB_CONNECT_TIMEOUT_MS', '20000')),
            socket_timeout_ms=int(os.getenv('MONGODB_SOCKET_TIMEOUT_MS', '30000')),
            
            # Retry settings
            retry_writes=os.getenv('MONGODB_RETRY_WRITES', 'true').lower() == 'true',
            retry_reads=os.getenv('MONGODB_RETRY_READS', 'true').lower() == 'true',
            max_retry_attempts=int(os.getenv('MONGODB_MAX_RETRY_ATTEMPTS', '3')),
            retry_delay_seconds=float(os.getenv('MONGODB_RETRY_DELAY_SECONDS', '1.0')),
            retry_backoff_multiplier=float(os.getenv('MONGODB_RETRY_BACKOFF_MULTIPLIER', '2.0')),
            
            # SSL/TLS settings - be more permissive in development
            tls_enabled=os.getenv('MONGODB_TLS_ENABLED', 'true').lower() == 'true',
            tls_allow_invalid_certificates=os.getenv(
                'MONGODB_TLS_ALLOW_INVALID_CERTS', 
                'true' if is_development else 'false'
            ).lower() == 'true',
            tls_allow_invalid_hostnames=os.getenv(
                'MONGODB_TLS_ALLOW_INVALID_HOSTNAMES',
                'true' if is_development else 'false'
            ).lower() == 'true',
            tls_ca_file=os.getenv('MONGODB_TLS_CA_FILE'),
            
            # Write concern
            write_concern_w=os.getenv('MONGODB_WRITE_CONCERN_W', 'majority'),
            write_concern_j=os.getenv('MONGODB_WRITE_CONCERN_J', 'true').lower() == 'true',
            write_concern_wtimeout=int(os.getenv('MONGODB_WRITE_CONCERN_WTIMEOUT', '5000')),
            
            # Read preference
            read_preference=os.getenv('MONGODB_READ_PREFERENCE', 'primaryPreferred'),
            
            # App name
            app_name=os.getenv('MONGODB_APP_NAME', 'EVPulse'),
            
            # Health check
            heartbeat_frequency_ms=int(os.getenv('MONGODB_HEARTBEAT_FREQUENCY_MS', '10000')),
            
            # Debug settings
            debug_mode=os.getenv('MONGODB_DEBUG', 'true' if is_development else 'false').lower() == 'true',
            log_queries=os.getenv('MONGODB_LOG_QUERIES', 'false').lower() == 'true',
        )
    
    def get_connection_options(self) -> Dict[str, Any]:
        """
        Get PyMongo connection options dictionary.
        Returns all necessary options for MongoClient initialization.
        """
        options = {
            # Pool settings
            'minPoolSize': self.min_pool_size,
            'maxPoolSize': self.max_pool_size,
            'maxIdleTimeMS': self.max_idle_time_ms,
            
            # Timeouts
            'serverSelectionTimeoutMS': self.server_selection_timeout_ms,
            'connectTimeoutMS': self.connect_timeout_ms,
            'socketTimeoutMS': self.socket_timeout_ms,
            
            # Retry settings
            'retryWrites': self.retry_writes,
            'retryReads': self.retry_reads,
            
            # Application identification
            'appName': self.app_name,
            
            # Heartbeat
            'heartbeatFrequencyMS': self.heartbeat_frequency_ms,
            
            # Compression
            'compressors': self.compressors,
        }
        
        # TLS settings
        if self.tls_enabled:
            options['tls'] = True
            options['tlsAllowInvalidCertificates'] = self.tls_allow_invalid_certificates
            options['tlsAllowInvalidHostnames'] = self.tls_allow_invalid_hostnames
            
            if self.tls_ca_file:
                options['tlsCAFile'] = self.tls_ca_file
        
        return options
    
    def validate(self) -> tuple[bool, list[str]]:
        """
        Validate configuration settings.
        Returns (is_valid, list_of_errors).
        """
        errors = []
        
        if not self.uri:
            errors.append("MongoDB URI is required")
        elif not (self.uri.startswith('mongodb://') or self.uri.startswith('mongodb+srv://')):
            errors.append("MongoDB URI must start with 'mongodb://' or 'mongodb+srv://'")
        
        if self.min_pool_size < 0:
            errors.append("min_pool_size must be >= 0")
        
        if self.max_pool_size < self.min_pool_size:
            errors.append("max_pool_size must be >= min_pool_size")
        
        if self.server_selection_timeout_ms < 1000:
            errors.append("server_selection_timeout_ms should be at least 1000ms")
        
        if self.max_retry_attempts < 0:
            errors.append("max_retry_attempts must be >= 0")
        
        return (len(errors) == 0, errors)
    
    def __repr__(self) -> str:
        """Safe string representation (hides URI credentials)"""
        masked_uri = self._mask_uri(self.uri)
        return f"MongoDBConfig(uri='{masked_uri}', database='{self.database_name}')"
    
    @staticmethod
    def _mask_uri(uri: str) -> str:
        """Mask credentials in URI for safe logging"""
        if not uri:
            return "<not set>"
        
        # Mask password in URI
        import re
        pattern = r'(mongodb(?:\+srv)?://[^:]+:)([^@]+)(@.*)'
        masked = re.sub(pattern, r'\1****\3', uri)
        return masked


# Global configuration instance
_config: Optional[MongoDBConfig] = None


def get_database_config() -> MongoDBConfig:
    """Get the global database configuration instance"""
    global _config
    if _config is None:
        _config = MongoDBConfig.from_environment()
    return _config


def set_database_config(config: MongoDBConfig) -> None:
    """Set a custom database configuration"""
    global _config
    _config = config
