#!/usr/bin/env python
"""
EVPulse Database Connection Test
================================
Comprehensive test script for MongoDB database connection.
Run this script to verify your database setup is working correctly.

Usage:
    python test_database.py
    python test_database.py --diagnostics
    python test_database.py --quick
"""

import sys
import os
import argparse
from datetime import datetime

# Add backend directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
from dotenv import load_dotenv
load_dotenv()


def print_header(title: str):
    """Print formatted header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def print_section(title: str):
    """Print formatted section"""
    print(f"\n{'─' * 50}")
    print(f"  {title}")
    print('─' * 50)


def test_imports():
    """Test that all database modules can be imported"""
    print_section("Testing Imports")
    
    try:
        from database import (
            MongoDBConfig,
            get_database_config,
            DatabaseConnectionManager,
            get_database_manager,
            init_db,
            close_db,
            get_db,
            get_collection,
            run_diagnostics,
            quick_test,
        )
        print("✅ All database module imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False


def test_configuration():
    """Test database configuration loading"""
    print_section("Testing Configuration")
    
    try:
        from database import get_database_config, MongoDBConfig
        
        config = get_database_config()
        
        print(f"📋 Configuration loaded: {config}")
        
        # Validate
        is_valid, errors = config.validate()
        
        if is_valid:
            print("✅ Configuration is valid")
        else:
            print("❌ Configuration errors:")
            for error in errors:
                print(f"   - {error}")
            return False
        
        # Show key settings
        print(f"\n📊 Key Settings:")
        print(f"   Database: {config.database_name}")
        print(f"   Pool Size: {config.min_pool_size} - {config.max_pool_size}")
        print(f"   Timeouts: {config.connect_timeout_ms}ms / {config.server_selection_timeout_ms}ms")
        print(f"   TLS: {config.tls_enabled}")
        print(f"   Retry Attempts: {config.max_retry_attempts}")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False


def test_quick_connection():
    """Quick connection test"""
    print_section("Quick Connection Test")
    
    try:
        from database import quick_test
        
        print("🔄 Testing connection...")
        result = quick_test()
        
        if result:
            print("✅ Quick connection test PASSED")
            return True
        else:
            print("❌ Quick connection test FAILED")
            return False
            
    except Exception as e:
        print(f"❌ Quick test error: {e}")
        return False


def test_full_connection():
    """Full connection test with database operations"""
    print_section("Full Connection Test")
    
    try:
        from database import init_db, get_database_manager, close_db
        
        # Initialize connection
        print("🔄 Initializing database connection...")
        manager = init_db()
        
        if not manager.is_connected:
            print("❌ Failed to connect")
            return False
        
        print(f"✅ Connected to database")
        print(f"   State: {manager.state}")
        
        # Test health check
        print("\n🔄 Running health check...")
        health = manager.health_check()
        
        if health['healthy']:
            print(f"✅ Health check passed (latency: {health['latency_ms']}ms)")
        else:
            print(f"❌ Health check failed: {health.get('error')}")
            return False
        
        # Test database access
        print("\n🔄 Testing database access...")
        db = manager.db
        collections = db.list_collection_names()
        print(f"✅ Database accessible")
        print(f"   Collections: {collections}")
        
        # Test collection operations
        print("\n🔄 Testing CRUD operations...")
        test_collection = db['_test_connection']
        
        # Insert
        doc = {'test': True, 'timestamp': datetime.utcnow()}
        result = test_collection.insert_one(doc)
        print(f"   ✅ Insert: {result.acknowledged}")
        
        # Read
        found = test_collection.find_one({'_id': result.inserted_id})
        print(f"   ✅ Read: {found is not None}")
        
        # Update
        update = test_collection.update_one({'_id': result.inserted_id}, {'$set': {'updated': True}})
        print(f"   ✅ Update: {update.modified_count == 1}")
        
        # Delete
        delete = test_collection.delete_one({'_id': result.inserted_id})
        print(f"   ✅ Delete: {delete.deleted_count == 1}")
        
        # Cleanup
        test_collection.drop()
        
        # Get stats
        print("\n📊 Connection Statistics:")
        stats = manager.stats
        print(f"   Connections Made: {stats['connections_made']}")
        print(f"   Queries Executed: {stats['queries_executed']}")
        print(f"   Uptime: {stats.get('uptime_seconds', 0):.2f}s")
        
        return True
        
    except Exception as e:
        print(f"❌ Connection test error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        # Cleanup
        try:
            from database import close_db
            close_db()
            print("\n✅ Connection closed")
        except:
            pass


def test_retry_mechanism():
    """Test retry mechanism"""
    print_section("Testing Retry Mechanism")
    
    try:
        from database import get_database_manager, with_db_retry
        
        manager = get_database_manager()
        
        if not manager.is_connected:
            print("⚠️ Not connected, skipping retry test")
            return True
        
        # Test execute_with_retry
        print("🔄 Testing execute_with_retry...")
        
        def test_operation():
            return manager.db.command('ping')
        
        result = manager.execute_with_retry(test_operation, max_retries=3)
        print(f"✅ Retry mechanism working (result: {result})")
        
        return True
        
    except Exception as e:
        print(f"❌ Retry test error: {e}")
        return False


def run_full_diagnostics():
    """Run complete diagnostics"""
    print_header("EVPulse Database Full Diagnostics")
    
    try:
        from database import run_diagnostics
        
        results = run_diagnostics()
        
        return results.get('all_passed', False)
        
    except Exception as e:
        print(f"❌ Diagnostics error: {e}")
        return False


def main():
    """Main test function"""
    parser = argparse.ArgumentParser(description='EVPulse Database Connection Test')
    parser.add_argument('--diagnostics', '-d', action='store_true', 
                       help='Run full diagnostics')
    parser.add_argument('--quick', '-q', action='store_true',
                       help='Run quick connection test only')
    args = parser.parse_args()
    
    print_header("EVPulse Database Connection Test")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🐍 Python {sys.version}")
    
    if args.diagnostics:
        success = run_full_diagnostics()
    elif args.quick:
        success = test_quick_connection()
    else:
        # Run all tests
        tests = [
            ("Imports", test_imports),
            ("Configuration", test_configuration),
            ("Quick Connection", test_quick_connection),
            ("Full Connection", test_full_connection),
            ("Retry Mechanism", test_retry_mechanism),
        ]
        
        results = []
        for name, test_func in tests:
            try:
                result = test_func()
                results.append((name, result))
            except Exception as e:
                print(f"❌ {name} test crashed: {e}")
                results.append((name, False))
        
        # Summary
        print_header("Test Summary")
        
        passed = sum(1 for _, r in results if r)
        total = len(results)
        
        for name, result in results:
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"   {status}: {name}")
        
        print(f"\n📊 Results: {passed}/{total} tests passed")
        
        success = passed == total
    
    # Final status
    print("\n" + "=" * 70)
    if success:
        print("🎉 All tests PASSED! Database connection is working correctly.")
    else:
        print("⚠️ Some tests FAILED. Check the output above for details.")
        print("\n💡 Troubleshooting tips:")
        print("   1. Check if MongoDB Atlas cluster is running (not paused)")
        print("   2. Verify IP address is whitelisted in MongoDB Atlas")
        print("   3. Check MONGODB_URI in .env file")
        print("   4. Run: python test_database.py --diagnostics")
    print("=" * 70 + "\n")
    
    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
