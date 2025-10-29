"""Test Supabase connection and list tables."""

import os
import sys

# Load environment variables from .env file
try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    print("⚠️  Install python-dotenv: uv pip install python-dotenv")

from supabase import create_client

print("=" * 60)
print("Supabase Connection Test")
print("=" * 60)

# Get credentials
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("\n❌ Error: Missing credentials")
    print("\nMake sure .env file contains:")
    print("SUPABASE_URL=https://your-project.supabase.co")
    print("SUPABASE_KEY=your-service-role-key")
    sys.exit(1)

print(f"\n✓ URL: {SUPABASE_URL}")
print(f"✓ Key: {SUPABASE_KEY[:20]}...")

# Try to connect
try:
    client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("\n✓ Connected to Supabase!")
except Exception as e:
    print(f"\n❌ Connection failed: {e}")
    sys.exit(1)

# Check if tables exist
print("\n⏳ Checking tables...")
tables_to_check = ["search_results", "parsed_content", "fake_detection_results"]

for table_name in tables_to_check:
    try:
        response = client.table(table_name).select("*").limit(0).execute()
        print(f"   ✓ {table_name} - exists")
    except Exception as e:
        error_msg = str(e)
        if "relation" in error_msg.lower() and "does not exist" in error_msg.lower():
            print(f"   ❌ {table_name} - not found")
            print(f"      Run migration: see docs/SUPABASE_USAGE.md")
        else:
            print(f"   ⚠️  {table_name} - error: {error_msg[:50]}")

print("\n" + "=" * 60)
print("Connection test complete!")
print("=" * 60)
