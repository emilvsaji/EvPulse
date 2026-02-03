"""
EVPulse Database Diagnostics Module
===================================
Comprehensive diagnostic tools for debugging MongoDB connection issues.
Provides detailed logging, connection testing, and troubleshooting information.
"""

import sys
import socket
import time
import platform
import ssl
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple
import logging

# Configure logging for diagnostics
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('evpulse.database.diagnostics')


class DiagnosticResult:
    """Container for diagnostic test results"""
    
    def __init__(self, name: str):
        self.name = name
        self.passed = False
        self.message = ""
        self.details: Dict[str, Any] = {}
        self.duration_ms: float = 0
        self.error: Optional[str] = None
        self.suggestions: List[str] = []
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "passed": self.passed,
            "message": self.message,
            "details": self.details,
            "duration_ms": round(self.duration_ms, 2),
            "error": self.error,
            "suggestions": self.suggestions
        }
    
    def __str__(self) -> str:
        status = "✅ PASS" if self.passed else "❌ FAIL"
        return f"{status} {self.name}: {self.message}"


class DatabaseDiagnostics:
    """
    Comprehensive database diagnostic tool.
    Run various tests to identify connection issues.
    """
    
    def __init__(self, uri: str, database_name: str = "evpulse"):
        self.uri = uri
        self.database_name = database_name
        self.results: List[DiagnosticResult] = []
    
    def run_all_diagnostics(self) -> Dict[str, Any]:
        """
        Run all diagnostic tests and return comprehensive results.
        """
        print("\n" + "=" * 70)
        print("🔍 EVPulse MongoDB Connection Diagnostics")
        print("=" * 70)
        print(f"📅 Timestamp: {datetime.now().isoformat()}")
        print(f"🐍 Python: {sys.version}")
        print(f"💻 Platform: {platform.platform()}")
        print("=" * 70 + "\n")
        
        # Run all tests
        self._test_environment()
        self._test_uri_parsing()
        self._test_dns_resolution()
        self._test_network_connectivity()
        self._test_ssl_support()
        self._test_pymongo_import()
        self._test_basic_connection()
        self._test_connection_with_tls_options()
        self._test_database_access()
        self._test_collection_operations()
        
        # Generate summary
        return self._generate_summary()
    
    def _test_environment(self) -> DiagnosticResult:
        """Test Python environment and dependencies"""
        result = DiagnosticResult("Environment Check")
        start = time.time()
        
        try:
            result.details["python_version"] = sys.version
            result.details["platform"] = platform.platform()
            result.details["architecture"] = platform.architecture()
            
            # Check Python version compatibility
            version_info = sys.version_info
            if version_info.major >= 3 and version_info.minor >= 8:
                result.passed = True
                result.message = f"Python {version_info.major}.{version_info.minor} is compatible"
            else:
                result.passed = False
                result.message = f"Python {version_info.major}.{version_info.minor} may have compatibility issues"
                result.suggestions.append("Upgrade to Python 3.8 or higher")
            
        except Exception as e:
            result.passed = False
            result.error = str(e)
            result.message = f"Environment check failed: {e}"
        
        result.duration_ms = (time.time() - start) * 1000
        self.results.append(result)
        print(result)
        return result
    
    def _test_uri_parsing(self) -> DiagnosticResult:
        """Test URI format and parsing"""
        result = DiagnosticResult("URI Parsing")
        start = time.time()
        
        try:
            from urllib.parse import urlparse, parse_qs
            
            # Mask password for logging
            masked_uri = self._mask_uri(self.uri)
            result.details["masked_uri"] = masked_uri
            
            # Check URI format
            if self.uri.startswith("mongodb+srv://"):
                result.details["connection_type"] = "SRV (DNS Seedlist)"
            elif self.uri.startswith("mongodb://"):
                result.details["connection_type"] = "Standard"
            else:
                result.passed = False
                result.error = "Invalid URI scheme"
                result.message = "URI must start with 'mongodb://' or 'mongodb+srv://'"
                result.suggestions.append("Check your MONGODB_URI environment variable")
                result.duration_ms = (time.time() - start) * 1000
                self.results.append(result)
                print(result)
                return result
            
            # Parse URI components
            parsed = urlparse(self.uri)
            result.details["has_username"] = bool(parsed.username)
            result.details["has_password"] = bool(parsed.password)
            result.details["host"] = parsed.hostname
            
            if parsed.username and parsed.password:
                result.passed = True
                result.message = "URI parsed successfully with credentials"
            else:
                result.passed = False
                result.message = "URI missing username or password"
                result.suggestions.append("Ensure URI contains username:password@")
            
        except Exception as e:
            result.passed = False
            result.error = str(e)
            result.message = f"URI parsing failed: {e}"
        
        result.duration_ms = (time.time() - start) * 1000
        self.results.append(result)
        print(result)
        return result
    
    def _test_dns_resolution(self) -> DiagnosticResult:
        """Test DNS resolution for MongoDB host"""
        result = DiagnosticResult("DNS Resolution")
        start = time.time()
        
        try:
            from urllib.parse import urlparse
            
            parsed = urlparse(self.uri)
            hostname = parsed.hostname
            
            if not hostname:
                result.passed = False
                result.message = "Could not extract hostname from URI"
                result.duration_ms = (time.time() - start) * 1000
                self.results.append(result)
                print(result)
                return result
            
            result.details["hostname"] = hostname
            
            # For SRV records, we need to resolve _mongodb._tcp.hostname
            if self.uri.startswith("mongodb+srv://"):
                import dns.resolver
                
                srv_hostname = f"_mongodb._tcp.{hostname}"
                result.details["srv_hostname"] = srv_hostname
                
                try:
                    srv_records = dns.resolver.resolve(srv_hostname, 'SRV')
                    servers = []
                    for record in srv_records:
                        servers.append(f"{record.target}:{record.port}")
                    
                    result.details["servers_found"] = len(servers)
                    result.details["servers"] = servers[:3]  # First 3 for brevity
                    result.passed = True
                    result.message = f"DNS SRV resolved: Found {len(servers)} server(s)"
                    
                except dns.resolver.NXDOMAIN:
                    result.passed = False
                    result.error = "SRV record not found"
                    result.message = "DNS SRV lookup failed - domain not found"
                    result.suggestions.append("Check if MongoDB Atlas cluster exists and is active")
                    result.suggestions.append("Verify the cluster hostname is correct")
                    
                except dns.resolver.NoAnswer:
                    result.passed = False
                    result.error = "No SRV records"
                    result.message = "No SRV records found for hostname"
                    result.suggestions.append("The MongoDB cluster may be paused or deleted")
                    
            else:
                # Standard connection - resolve hostname directly
                addresses = socket.getaddrinfo(hostname, 27017)
                result.details["addresses_found"] = len(addresses)
                result.passed = True
                result.message = f"DNS resolved: Found {len(addresses)} address(es)"
            
        except ImportError:
            # dnspython not installed - try basic resolution
            try:
                from urllib.parse import urlparse
                parsed = urlparse(self.uri)
                hostname = parsed.hostname
                ip = socket.gethostbyname(hostname.replace("_mongodb._tcp.", ""))
                result.details["resolved_ip"] = ip
                result.passed = True
                result.message = f"Basic DNS resolved to {ip}"
            except Exception as e:
                result.passed = False
                result.error = str(e)
                result.message = "DNS resolution failed (dnspython not installed)"
                result.suggestions.append("Install dnspython: pip install dnspython")
                
        except Exception as e:
            result.passed = False
            result.error = str(e)
            result.message = f"DNS resolution failed: {e}"
            result.suggestions.append("Check your internet connection")
            result.suggestions.append("Verify the MongoDB hostname is correct")
        
        result.duration_ms = (time.time() - start) * 1000
        self.results.append(result)
        print(result)
        return result
    
    def _test_network_connectivity(self) -> DiagnosticResult:
        """Test network connectivity to MongoDB ports"""
        result = DiagnosticResult("Network Connectivity")
        start = time.time()
        
        try:
            # Test connectivity to common MongoDB Atlas endpoints
            test_hosts = [
                ("cluster0.kdwdasn.mongodb.net", 27017),
            ]
            
            # Also try to extract host from URI
            from urllib.parse import urlparse
            parsed = urlparse(self.uri)
            if parsed.hostname:
                base_host = parsed.hostname.replace("_mongodb._tcp.", "")
                test_hosts.insert(0, (base_host, 27017))
            
            connectivity_results = []
            for host, port in test_hosts:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(5)
                    conn_result = sock.connect_ex((host, port))
                    sock.close()
                    
                    if conn_result == 0:
                        connectivity_results.append({"host": host, "port": port, "reachable": True})
                    else:
                        connectivity_results.append({"host": host, "port": port, "reachable": False, "error_code": conn_result})
                except socket.gaierror:
                    connectivity_results.append({"host": host, "port": port, "reachable": False, "error": "DNS failed"})
                except socket.timeout:
                    connectivity_results.append({"host": host, "port": port, "reachable": False, "error": "Timeout"})
                except Exception as e:
                    connectivity_results.append({"host": host, "port": port, "reachable": False, "error": str(e)})
            
            result.details["connectivity_tests"] = connectivity_results
            
            # Check if any host was reachable
            reachable = any(r.get("reachable", False) for r in connectivity_results)
            
            if reachable:
                result.passed = True
                result.message = "Network connectivity to MongoDB confirmed"
            else:
                result.passed = False
                result.message = "Cannot reach MongoDB servers"
                result.suggestions.append("Check if firewall is blocking port 27017")
                result.suggestions.append("Verify your IP is whitelisted in MongoDB Atlas")
                result.suggestions.append("Check if VPN/proxy is interfering")
            
        except Exception as e:
            result.passed = False
            result.error = str(e)
            result.message = f"Network test failed: {e}"
        
        result.duration_ms = (time.time() - start) * 1000
        self.results.append(result)
        print(result)
        return result
    
    def _test_ssl_support(self) -> DiagnosticResult:
        """Test SSL/TLS support"""
        result = DiagnosticResult("SSL/TLS Support")
        start = time.time()
        
        try:
            result.details["ssl_version"] = ssl.OPENSSL_VERSION
            result.details["default_verify_paths"] = ssl.get_default_verify_paths()._asdict()
            
            # Check available protocols
            result.details["has_tlsv1_2"] = hasattr(ssl, 'PROTOCOL_TLSv1_2')
            result.details["has_tlsv1_3"] = hasattr(ssl, 'PROTOCOL_TLS')
            
            # Try creating SSL context
            ctx = ssl.create_default_context()
            result.details["default_context_created"] = True
            
            # Check certifi if available
            try:
                import certifi
                result.details["certifi_path"] = certifi.where()
                result.details["certifi_available"] = True
            except ImportError:
                result.details["certifi_available"] = False
                result.suggestions.append("Install certifi for better SSL support: pip install certifi")
            
            result.passed = True
            result.message = f"SSL supported: {ssl.OPENSSL_VERSION}"
            
        except Exception as e:
            result.passed = False
            result.error = str(e)
            result.message = f"SSL check failed: {e}"
            result.suggestions.append("SSL/TLS may not be properly configured")
        
        result.duration_ms = (time.time() - start) * 1000
        self.results.append(result)
        print(result)
        return result
    
    def _test_pymongo_import(self) -> DiagnosticResult:
        """Test PyMongo import and version"""
        result = DiagnosticResult("PyMongo Import")
        start = time.time()
        
        try:
            import pymongo
            result.details["pymongo_version"] = pymongo.version
            
            from pymongo import MongoClient
            result.details["MongoClient_available"] = True
            
            # Check for optional dependencies
            try:
                import dns.resolver
                result.details["dnspython_available"] = True
            except ImportError:
                result.details["dnspython_available"] = False
                result.suggestions.append("Install dnspython for SRV support: pip install dnspython")
            
            result.passed = True
            result.message = f"PyMongo {pymongo.version} loaded successfully"
            
        except ImportError as e:
            result.passed = False
            result.error = str(e)
            result.message = "PyMongo not installed"
            result.suggestions.append("Install pymongo: pip install pymongo[srv]")
            
        except Exception as e:
            result.passed = False
            result.error = str(e)
            result.message = f"PyMongo import failed: {e}"
        
        result.duration_ms = (time.time() - start) * 1000
        self.results.append(result)
        print(result)
        return result
    
    def _test_basic_connection(self) -> DiagnosticResult:
        """Test basic MongoDB connection"""
        result = DiagnosticResult("Basic Connection")
        start = time.time()
        
        try:
            from pymongo import MongoClient
            
            client = MongoClient(
                self.uri,
                serverSelectionTimeoutMS=10000,
                connectTimeoutMS=10000,
            )
            
            # Test with ping
            client.admin.command('ping')
            
            result.details["connection_type"] = "basic"
            result.passed = True
            result.message = "Basic connection successful"
            
            client.close()
            
        except Exception as e:
            result.passed = False
            result.error = str(e)
            error_str = str(e).lower()
            
            if "timeout" in error_str or "serverselection" in error_str:
                result.message = "Connection timed out"
                result.suggestions.append("MongoDB Atlas cluster may be PAUSED - check Atlas dashboard")
                result.suggestions.append("Your IP may not be whitelisted - add 0.0.0.0/0 for testing")
                result.suggestions.append("Check network/firewall settings")
            elif "authentication" in error_str:
                result.message = "Authentication failed"
                result.suggestions.append("Check username and password in connection string")
                result.suggestions.append("Verify user has proper permissions")
            elif "ssl" in error_str or "certificate" in error_str:
                result.message = "SSL/TLS error"
                result.suggestions.append("Try connection with TLS options (next test)")
            else:
                result.message = f"Connection failed: {e}"
        
        result.duration_ms = (time.time() - start) * 1000
        self.results.append(result)
        print(result)
        return result
    
    def _test_connection_with_tls_options(self) -> DiagnosticResult:
        """Test MongoDB connection with various TLS options"""
        result = DiagnosticResult("TLS Connection Options")
        start = time.time()
        
        try:
            from pymongo import MongoClient
            
            # Try with relaxed TLS settings
            client = MongoClient(
                self.uri,
                serverSelectionTimeoutMS=10000,
                connectTimeoutMS=10000,
                tls=True,
                tlsAllowInvalidCertificates=True,
                tlsAllowInvalidHostnames=True,
            )
            
            client.admin.command('ping')
            
            result.details["tls_options"] = {
                "tls": True,
                "tlsAllowInvalidCertificates": True,
                "tlsAllowInvalidHostnames": True
            }
            result.passed = True
            result.message = "TLS connection successful with relaxed settings"
            
            client.close()
            
        except Exception as e:
            result.passed = False
            result.error = str(e)
            result.message = f"TLS connection failed: {e}"
            result.suggestions.append("Check if MongoDB Atlas requires specific TLS version")
        
        result.duration_ms = (time.time() - start) * 1000
        self.results.append(result)
        print(result)
        return result
    
    def _test_database_access(self) -> DiagnosticResult:
        """Test database access and permissions"""
        result = DiagnosticResult("Database Access")
        start = time.time()
        
        try:
            from pymongo import MongoClient
            
            client = MongoClient(
                self.uri,
                serverSelectionTimeoutMS=10000,
                connectTimeoutMS=10000,
                tls=True,
                tlsAllowInvalidCertificates=True,
            )
            
            # List databases
            databases = client.list_database_names()
            result.details["available_databases"] = databases
            
            # Access target database
            db = client[self.database_name]
            collections = db.list_collection_names()
            result.details["target_database"] = self.database_name
            result.details["collections"] = collections
            
            result.passed = True
            result.message = f"Database '{self.database_name}' accessible with {len(collections)} collection(s)"
            
            client.close()
            
        except Exception as e:
            result.passed = False
            result.error = str(e)
            result.message = f"Database access failed: {e}"
            
            if "not authorized" in str(e).lower():
                result.suggestions.append("User may not have permissions on this database")
                result.suggestions.append("Check user roles in MongoDB Atlas")
        
        result.duration_ms = (time.time() - start) * 1000
        self.results.append(result)
        print(result)
        return result
    
    def _test_collection_operations(self) -> DiagnosticResult:
        """Test basic collection operations (CRUD)"""
        result = DiagnosticResult("Collection Operations")
        start = time.time()
        
        try:
            from pymongo import MongoClient
            from bson import ObjectId
            
            client = MongoClient(
                self.uri,
                serverSelectionTimeoutMS=10000,
                connectTimeoutMS=10000,
                tls=True,
                tlsAllowInvalidCertificates=True,
            )
            
            db = client[self.database_name]
            test_collection = db["_diagnostic_test"]
            
            # Test insert
            test_doc = {
                "_id": ObjectId(),
                "test": True,
                "timestamp": datetime.utcnow(),
                "diagnostic": "EVPulse connection test"
            }
            insert_result = test_collection.insert_one(test_doc)
            result.details["insert_success"] = insert_result.acknowledged
            
            # Test read
            found_doc = test_collection.find_one({"_id": test_doc["_id"]})
            result.details["read_success"] = found_doc is not None
            
            # Test update
            update_result = test_collection.update_one(
                {"_id": test_doc["_id"]},
                {"$set": {"updated": True}}
            )
            result.details["update_success"] = update_result.modified_count == 1
            
            # Test delete (cleanup)
            delete_result = test_collection.delete_one({"_id": test_doc["_id"]})
            result.details["delete_success"] = delete_result.deleted_count == 1
            
            # Drop test collection
            test_collection.drop()
            
            result.passed = True
            result.message = "All CRUD operations successful"
            
            client.close()
            
        except Exception as e:
            result.passed = False
            result.error = str(e)
            result.message = f"Collection operations failed: {e}"
            
            if "not authorized" in str(e).lower():
                result.suggestions.append("User may not have write permissions")
        
        result.duration_ms = (time.time() - start) * 1000
        self.results.append(result)
        print(result)
        return result
    
    def _generate_summary(self) -> Dict[str, Any]:
        """Generate diagnostic summary"""
        passed = sum(1 for r in self.results if r.passed)
        failed = sum(1 for r in self.results if not r.passed)
        total = len(self.results)
        
        all_suggestions = []
        for r in self.results:
            all_suggestions.extend(r.suggestions)
        
        # Remove duplicates while preserving order
        unique_suggestions = list(dict.fromkeys(all_suggestions))
        
        summary = {
            "timestamp": datetime.now().isoformat(),
            "total_tests": total,
            "passed": passed,
            "failed": failed,
            "success_rate": f"{(passed/total)*100:.1f}%" if total > 0 else "0%",
            "all_passed": failed == 0,
            "results": [r.to_dict() for r in self.results],
            "suggestions": unique_suggestions,
        }
        
        # Print summary
        print("\n" + "=" * 70)
        print("📊 DIAGNOSTIC SUMMARY")
        print("=" * 70)
        print(f"Tests Passed: {passed}/{total} ({summary['success_rate']})")
        
        if failed > 0:
            print(f"\n❌ Failed Tests:")
            for r in self.results:
                if not r.passed:
                    print(f"   - {r.name}: {r.message}")
            
            if unique_suggestions:
                print(f"\n💡 Suggestions:")
                for i, suggestion in enumerate(unique_suggestions, 1):
                    print(f"   {i}. {suggestion}")
        else:
            print("\n✅ All tests passed! Database connection is working correctly.")
        
        print("=" * 70 + "\n")
        
        return summary
    
    @staticmethod
    def _mask_uri(uri: str) -> str:
        """Mask credentials in URI"""
        import re
        pattern = r'(mongodb(?:\+srv)?://[^:]+:)([^@]+)(@.*)'
        return re.sub(pattern, r'\1****\3', uri)


def run_diagnostics(uri: Optional[str] = None, database_name: str = "evpulse") -> Dict[str, Any]:
    """
    Run full database diagnostics.
    
    Args:
        uri: MongoDB connection URI. If not provided, reads from environment.
        database_name: Target database name.
    
    Returns:
        Dictionary with diagnostic results.
    """
    if uri is None:
        import os
        try:
            from dotenv import load_dotenv
            load_dotenv()
        except ImportError:
            pass
        uri = os.getenv('MONGODB_URI', '')
    
    if not uri:
        print("❌ ERROR: No MongoDB URI provided")
        print("Set MONGODB_URI environment variable or pass uri parameter")
        return {"error": "No MongoDB URI provided"}
    
    diagnostics = DatabaseDiagnostics(uri, database_name)
    return diagnostics.run_all_diagnostics()


def quick_test(uri: Optional[str] = None) -> bool:
    """
    Quick connection test - returns True if connection works.
    
    Args:
        uri: MongoDB connection URI. If not provided, reads from environment.
    
    Returns:
        bool: True if connection successful.
    """
    if uri is None:
        import os
        try:
            from dotenv import load_dotenv
            load_dotenv()
        except ImportError:
            pass
        uri = os.getenv('MONGODB_URI', '')
    
    if not uri:
        return False
    
    try:
        from pymongo import MongoClient
        
        client = MongoClient(
            uri,
            serverSelectionTimeoutMS=5000,
            connectTimeoutMS=5000,
            tls=True,
            tlsAllowInvalidCertificates=True,
        )
        client.admin.command('ping')
        client.close()
        return True
    except:
        return False


if __name__ == "__main__":
    # Run diagnostics when executed directly
    run_diagnostics()
