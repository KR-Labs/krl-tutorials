#!/usr/bin/env python3
"""
Debug script to test text enrichment on a single article
Run this to see the actual error messages
"""

import os
import sys
from robust_text_enrichment import RobustTextEnricher
from dotenv import load_dotenv

# Load environment
env_path = os.path.expanduser('~/Documents/GitHub/KRL/krl-tutorials/.env')
load_dotenv(env_path)

# Test URL (using a simple, publicly accessible article)
TEST_URL = "https://www.bbc.com/news/articles/c8xp3v4p43ko"
TEST_TITLE = "Test Article for Enrichment"

print("="*80)
print("TEXT ENRICHMENT DEBUG TEST")
print("="*80)
print()

# Check environment
print("1. Environment Check:")
print(f"   JINA_API_KEY: {'SET' if os.environ.get('JINA_API_KEY') else 'NOT SET'}")
if os.environ.get('JINA_API_KEY'):
    key = os.environ.get('JINA_API_KEY')
    print(f"   Key length: {len(key)} chars")
    print(f"   Key prefix: {key[:15]}...")
print()

# Initialize enricher
print("2. Initializing RobustTextEnricher...")
try:
    enricher = RobustTextEnricher()
    print("   ✅ Initialized successfully")
    print()
except Exception as e:
    print(f"   ❌ Initialization failed: {e}")
    sys.exit(1)

# Check available methods
print("3. Available Methods:")
methods = [m for m in dir(enricher) if not m.startswith('_') and 'enrich' in m.lower()]
for method in methods:
    print(f"   • {method}")
print()

# Test enrichment
print("4. Testing Text Enrichment:")
print(f"   URL: {TEST_URL}")
print(f"   Title: {TEST_TITLE}")
print()

try:
    result = enricher.enrich_article(url=TEST_URL, title=TEST_TITLE)

    print("   ✅ SUCCESS!")
    print(f"   Method used: {result.get('method', 'unknown')}")
    print(f"   Success: {result.get('success', False)}")
    print(f"   Word count: {result.get('word_count', 0)}")

    if 'text' in result:
        text = result['text']
        print(f"   Text length: {len(text)} chars")
        print()
        print("   First 300 characters:")
        print("   " + "-"*76)
        print(f"   {text[:300]}")
        print("   " + "-"*76)
    else:
        print("   ⚠️  No 'text' field in result")
        print(f"   Result keys: {list(result.keys())}")

except Exception as e:
    print(f"   ❌ ENRICHMENT FAILED")
    print(f"   Error type: {type(e).__name__}")
    print(f"   Error message: {str(e)}")
    print()

    # Full traceback
    import traceback
    print("   Full traceback:")
    print("   " + "-"*76)
    traceback.print_exc()
    print("   " + "-"*76)

print()
print("="*80)
print("DEBUG TEST COMPLETE")
print("="*80)
