#!/usr/bin/env python3
"""
Detailed debug - test each extraction method individually
"""

import os
from dotenv import load_dotenv

# Load environment
env_path = os.path.expanduser('~/Documents/GitHub/KRL/krl-tutorials/.env')
load_dotenv(env_path)

# Test with a real article from your dataset
import pandas as pd
from gdelt_connector import GDELTConnector

print("="*80)
print("DETAILED TEXT ENRICHMENT DEBUG")
print("="*80)
print()

# Load a few real URLs from your dataset
print("1. Loading real URLs from GDELT dataset...")
connector = GDELTConnector()
df = connector.query_articles(topic='housing affordability', days_back=7, max_results=10)
print(f"   Loaded {len(df)} articles")
print()

# Test on first article
test_url = df['url'].iloc[0]
test_title = df['title'].iloc[0]

print(f"2. Testing URL: {test_url}")
print(f"   Title: {test_title[:100]}...")
print()

# Initialize enricher manually to see each method
from robust_text_enrichment import RobustTextEnricher

enricher = RobustTextEnricher()

print("3. Testing Each Extraction Method:")
print("-" * 80)

# Method 1: Jina Reader
print("\n[Method 1] Jina Reader API")
try:
    result = enricher._try_jina_reader(test_url)
    if result:
        print(f"   ✅ SUCCESS - {len(result)} chars")
        print(f"   First 200 chars: {result[:200]}...")
    else:
        print(f"   ❌ FAILED - returned None")
except Exception as e:
    print(f"   ❌ EXCEPTION: {type(e).__name__}: {e}")

# Method 2: Newspaper3k
print("\n[Method 2] Newspaper3k")
try:
    result = enricher._try_newspaper3k(test_url)
    if result:
        print(f"   ✅ SUCCESS - {len(result)} chars")
        print(f"   First 200 chars: {result[:200]}...")
    else:
        print(f"   ❌ FAILED - returned None")
except Exception as e:
    print(f"   ❌ EXCEPTION: {type(e).__name__}: {e}")

# Method 3: Trafilatura
print("\n[Method 3] Trafilatura")
try:
    result = enricher._try_trafilatura(test_url)
    if result:
        print(f"   ✅ SUCCESS - {len(result)} chars")
        print(f"   First 200 chars: {result[:200]}...")
    else:
        print(f"   ❌ FAILED - returned None")
except Exception as e:
    print(f"   ❌ EXCEPTION: {type(e).__name__}: {e}")

# Method 4: BeautifulSoup
print("\n[Method 4] BeautifulSoup")
try:
    result = enricher._try_beautifulsoup(test_url)
    if result:
        print(f"   ✅ SUCCESS - {len(result)} chars")
        print(f"   First 200 chars: {result[:200]}...")
    else:
        print(f"   ❌ FAILED - returned None")
except Exception as e:
    print(f"   ❌ EXCEPTION: {type(e).__name__}: {e}")

print()
print("="*80)
print("DETAILED DEBUG COMPLETE")
print("="*80)
print()

# Check statistics
print("Enricher Statistics:")
print(enricher.stats)
