"""
MongoDB Atlas Connection Diagnostic Tool
Run this to identify connection issues
"""
import sys
import ssl
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, ConfigurationError
import certifi

# Connection string
MONGO_URI = "mongodb+srv://evpulse:evpulse2026@cluster0.kdwdasn.mongodb.net/evpulse?retryWrites=true&w=majority"

print("=" * 60)
print("MongoDB Atlas Connection Diagnostic")
print("=" * 60)
print(f"\n🐍 Python Version: {sys.version}")
print(f"📦 Certifi CA Bundle: {certifi.where()}")

# Test 1: Basic connection with default SSL
print("\n\n📋 Test 1: Basic Connection (Default SSL)")
print("-" * 60)
try:
    client = MongoClient(
        MONGO_URI,
        serverSelectionTimeoutMS=5000,
        connectTimeoutMS=5000
    )
    db = client.evpulse
    collections = db.list_collection_names()
    print("✅ SUCCESS! Connected to MongoDB Atlas")
    print(f"📊 Collections: {collections}")
    client.close()
except ServerSelectionTimeoutError as e:
    print(f"❌ TIMEOUT: Could not connect within 5 seconds")
    print(f"   Error: {str(e)[:200]}...")
except Exception as e:
    print(f"❌ ERROR: {type(e).__name__}")
    print(f"   Details: {str(e)[:200]}...")

# Test 2: Connection with SSL certificate validation disabled
print("\n\n📋 Test 2: Connection with SSL Validation Disabled")
print("-" * 60)
try:
    client = MongoClient(
        MONGO_URI,
        serverSelectionTimeoutMS=5000,
        connectTimeoutMS=5000,
        tls=True,
        tlsAllowInvalidCertificates=True
    )
    db = client.evpulse
    collections = db.list_collection_names()
    print("✅ SUCCESS! Connected with SSL validation disabled")
    print(f"📊 Collections: {collections}")
    client.close()
except ServerSelectionTimeoutError as e:
    print(f"❌ TIMEOUT: Could not connect within 5 seconds")
    print(f"   Error: {str(e)[:200]}...")
except Exception as e:
    print(f"❌ ERROR: {type(e).__name__}")
    print(f"   Details: {str(e)[:200]}...")

# Test 3: Direct connection (bypass SRV)
print("\n\n📋 Test 3: Direct Connection (Non-SRV)")
print("-" * 60)
direct_uri = "mongodb://evpulse:evpulse2026@ac-fatfhv9-shard-00-00.kdwdasn.mongodb.net:27017,ac-fatfhv9-shard-00-01.kdwdasn.mongodb.net:27017,ac-fatfhv9-shard-00-02.kdwdasn.mongodb.net:27017/evpulse?ssl=true&replicaSet=atlas-123abc-shard-0&authSource=admin&retryWrites=true&w=majority"
try:
    client = MongoClient(
        direct_uri,
        serverSelectionTimeoutMS=5000,
        connectTimeoutMS=5000,
        tls=True,
        tlsAllowInvalidCertificates=True
    )
    db = client.evpulse
    collections = db.list_collection_names()
    print("✅ SUCCESS! Connected via direct connection")
    print(f"📊 Collections: {collections}")
    client.close()
except Exception as e:
    print(f"❌ ERROR: {type(e).__name__}")
    print(f"   Details: {str(e)[:200]}...")

print("\n\n" + "=" * 60)
print("🔍 Diagnosis Summary")
print("=" * 60)
print("\n⚠️  If ALL tests failed with TIMEOUT:")
print("   1. ⏸️  MongoDB Atlas cluster is PAUSED")
print("      → Login to https://cloud.mongodb.com/")
print("      → Click on your cluster → Click 'Resume'")
print("\n   2. 🔒 IP Address not whitelisted")
print("      → Go to Network Access in Atlas")
print("      → Add IP Address: 0.0.0.0/0")
print("\n   3. 🌐 Network/Firewall blocking MongoDB")
print("      → Check firewall settings")
print("      → Ensure port 27017 is open")

print("\n⚠️  If tests failed with SSL/Certificate errors:")
print("   1. Python 3.13 compatibility issue")
print("      → Use Python 3.11 or 3.12 instead")
print("   2. Update packages:")
print("      → pip install --upgrade pymongo certifi")

print("\n✅ If Test 2 or 3 succeeded:")
print("   → Use tlsAllowInvalidCertificates=True in production config")
print("=" * 60)
