# ==========================================
# Part 8: PARALLEL Text Enrichment with Caching
# ==========================================

import os
import re
import json
import hashlib
from concurrent.futures import ThreadPoolExecutor, as_completed
from robust_text_enrichment import RobustTextEnricher
from tqdm import tqdm

# CACHING SETUP
CACHE_DIR = "cache_enriched"
os.makedirs(CACHE_DIR, exist_ok=True)

def cache_key(url):
    return os.path.join(CACHE_DIR, hashlib.md5(url.encode()).hexdigest() + ".json")

def clean_extracted_text(text):
    """Remove common navigation and UI elements from extracted text"""
    if not isinstance(text, str):
        return text

    patterns = [
        r'Skip to Content.*?(?=\n|$)',
        r'Breadcrumb Trail Links.*?(?=\n|$)',
        r'Share this Story\s*:.*?(?=\n|$)',
        r'LATEST STORIES:.*?(?=\n|$)',
        r'Advertisement\s*\n',
        r'Subscribe.*?(?=\n|$)',
        r'Sign up for.*?(?=\n|$)',
        r'^\s*Home\s*News\s*Local News\s*',
        r'^\s*Menu\s*',
        r'^\s*Search\s*',
    ]

    for pattern in patterns:
        text = re.sub(pattern, '', text, flags=re.IGNORECASE | re.MULTILINE)

    text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)
    return text.strip()

def cached_extract(url, title, enricher):
    """Extract article with caching"""
    cache_file = cache_key(url)

    if os.path.exists(cache_file):
        try:
            with open(cache_file, 'r') as f:
                return json.load(f)
        except:
            os.remove(cache_file)

    try:
        result = enricher.enrich_row(url=url, title=title)
        with open(cache_file, 'w') as f:
            json.dump(result, f)
        return result
    except Exception as e:
        return {
            'full_text': title,
            'extraction_method': 'error',
            'word_count': len(title.split()),
            'error': str(e)
        }

def parallel_enrich(df, max_articles, enricher, max_workers=20):
    """Enrich with parallel processing"""
    rows = df.head(max_articles).to_dict('records')

    print(f"🚀 Enriching {len(rows)} articles with {max_workers} parallel workers...")
    print(f"   Cache directory: {CACHE_DIR}/")

    results = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(cached_extract, row['url'], row['title'], enricher): row
            for row in rows
        }

        with tqdm(total=len(futures), desc="Enriching") as pbar:
            for future in as_completed(futures):
                try:
                    result = future.result(timeout=10)
                    results.append(result)
                except Exception as e:
                    row = futures[future]
                    results.append({
                        'full_text': row['title'],
                        'extraction_method': 'timeout',
                        'word_count': len(row['title'].split()),
                        'error': str(e)
                    })
                finally:
                    pbar.update(1)

    return results

# Initialize enricher
enricher = RobustTextEnricher()

# Run enrichment
if ENABLE_TEXT_ENRICHMENT:
    cache_files = [f for f in os.listdir(CACHE_DIR) if f.endswith('.json')] if os.path.exists(CACHE_DIR) else []

    print(f"\n{'='*80}")
    print(f"📖 PARALLEL TEXT ENRICHMENT")
    print(f"{'='*80}")
    print(f"   Max articles: {MAX_ARTICLES_TO_ENRICH}")
    print(f"   Workers: 20 parallel")
    print(f"   Caching: Enabled")
    print(f"   Cached articles: {len(cache_files)}")

    enrichment_results = parallel_enrich(df, MAX_ARTICLES_TO_ENRICH, enricher, max_workers=20)

    df_enriched = df.head(MAX_ARTICLES_TO_ENRICH).copy()
    df_enriched['full_text'] = [r.get('full_text', '') for r in enrichment_results]
    df_enriched['extraction_method'] = [r.get('extraction_method', 'unknown') for r in enrichment_results]
    df_enriched['word_count'] = [r.get('word_count', 0) for r in enrichment_results]
    df_enriched['full_text'] = df_enriched['full_text'].apply(clean_extracted_text)
    df_enriched['text_for_clustering'] = df_enriched['full_text'].fillna(df_enriched['title'])

    success_count = (df_enriched['extraction_method'] != 'title_fallback').sum()
    success_rate = success_count / len(df_enriched) * 100
    avg_length = df_enriched['text_for_clustering'].str.len().mean()

    print(f"\n{'='*80}")
    print(f"📊 ENRICHMENT STATISTICS")
    print(f"{'='*80}")
    print(f"   Total articles: {len(df_enriched)}")
    print(f"   Successfully enriched: {success_count} ({success_rate:.1f}%)")
    print(f"   Average text length: {avg_length:.0f} characters")
    print(f"   Cache size: {len(cache_files)} files")

    method_counts = df_enriched['extraction_method'].value_counts()
    print(f"\n   Method Breakdown:")
    for method, count in method_counts.items():
        pct = count / len(df_enriched) * 100
        print(f"     • {method}: {count} ({pct:.1f}%)")

    print(f"\n✅ Text enrichment complete!")
    print(f"   Ready for adaptive weighting and clustering!")
else:
    print("\n⏭️  Text enrichment DISABLED")
    print("   Using titles only")
    df_enriched = df.copy()
    df_enriched['text_for_clustering'] = df_enriched['title']
    df_enriched['full_text'] = df_enriched['title']
    df_enriched['extraction_method'] = 'title_only'
    df_enriched['word_count'] = df_enriched['title'].str.split().str.len()
    print(f"✅ Using {len(df_enriched)} article titles for analysis")

print(f"\n{'='*80}")
