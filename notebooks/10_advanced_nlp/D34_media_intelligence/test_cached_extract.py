#!/usr/bin/env python3
"""
Test the fixed cached_extract() function from Cell 9
"""

import os
import json
import hashlib
from dotenv import load_dotenv

# Load environment
env_path = os.path.expanduser('~/Documents/GitHub/KRL/krl-tutorials/.env')
load_dotenv(env_path)

from robust_text_enrichment import RobustTextEnricher

# Replicate the fixed cached_extract() function
def cache_key(url):
    """Generate cache key from URL"""
    return f"cache_enriched/{hashlib.md5(url.encode()).hexdigest()}.json"

def cached_extract(url, title, enricher):
    """Extract article with caching"""
    cache_file = cache_key(url)

    if os.path.exists(cache_file):
        try:
            with open(cache_file, 'r') as f:
                return json.load(f)
        except:
            os.remove(cache_file)

    # Call enrich_article - it returns dict with 'text', 'method', 'success', 'word_count'
    result = enricher.enrich_article(url=url, title=title)

    # Convert to our expected format
    adapted_result = {
        'full_text': result.get('text', title),
        'extraction_method': result.get('method', 'unknown'),
        'word_count': result.get('word_count', len(title.split())),
        'success': result.get('success', False)
    }

    # Cache the result
    try:
        with open(cache_file, 'w') as f:
            json.dump(adapted_result, f)
    except:
        pass  # Ignore cache write errors

    return adapted_result

# Test
print("="*80)
print("TESTING FIXED cached_extract() FUNCTION")
print("="*80)
print()

# Create cache directory
os.makedirs('cache_enriched', exist_ok=True)

# Initialize enricher
enricher = RobustTextEnricher()

# Test URL (from previous test)
test_url = "https://www.mpamag.com/us/specialty/wholesale/housing-affordability-crisis-answers-young-borrowers-want-from-mortgage-brokers/557693"
test_title = "Housing affordability crisis test"

print("1. Testing cached_extract() with real URL...")
result = cached_extract(test_url, test_title, enricher)

print(f"\n2. Result structure:")
print(f"   Keys: {list(result.keys())}")
print()

print(f"3. Result values:")
print(f"   ✓ full_text: {len(result['full_text'])} chars")
print(f"   ✓ extraction_method: {result['extraction_method']}")
print(f"   ✓ word_count: {result['word_count']}")
print(f"   ✓ success: {result['success']}")
print()

print(f"4. First 200 chars of full_text:")
print(f"   {result['full_text'][:200]}...")
print()

# Check expected behavior
if result['success'] and result['extraction_method'] != 'title_fallback':
    print("✅ SUCCESS: Article extracted and mapped correctly!")
    print(f"   Method used: {result['extraction_method']}")
    print(f"   Text quality: {result['word_count']} words")
else:
    print("❌ FAILED: Fell back to title")
    print(f"   Method: {result['extraction_method']}")

print()
print("="*80)
print("TEST COMPLETE")
print("="*80)
