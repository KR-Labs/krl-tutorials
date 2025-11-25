"""
Jina Reader API Integration
High-success-rate article full-text extraction

Advantages over basic URL parsing:
- 85-95% success rate
- Handles JavaScript rendering, paywalls, dynamic content
- Returns clean markdown format
- Rate limiting built-in
- $29/month for 5,000 requests
"""

import requests
import pandas as pd
from typing import Dict, Optional
from datetime import datetime
import time
from tqdm import tqdm
import os

class JinaTextEnricher:
    """
    Fetch article full text using Jina Reader API

    Cost: $29/month for 5,000 requests
    Success rate: 85-95% (empirical)
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Jina Reader client

        Args:
            api_key: Jina API key (or set JINA_API_KEY environment variable)
        """
        self.api_key = api_key or os.environ.get('JINA_API_KEY')

        if not self.api_key:
            print("⚠️  Jina API key not found. Full-text enrichment will be skipped.")
            print("   To enable: Get API key at https://jina.ai/reader")
            print("   Then: export JINA_API_KEY='your-key-here'")
            self.enabled = False
            return

        self.enabled = True
        self.base_url = "https://r.jina.ai/"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "X-Return-Format": "markdown"
        }

        # Rate limiting (5 requests/second)
        self.min_request_interval = 0.2
        self.last_request_time = 0

        # Statistics
        self.total_requests = 0
        self.successful_requests = 0
        self.failed_requests = 0

        print("📰 Jina Reader initialized")
        print("   Rate limit: 5 requests/second")
        print("   Monthly quota: 5,000 requests ($29/month)")

    def fetch_article(self, url: str, timeout: int = 10) -> Dict:
        """
        Fetch full text for a single article

        Args:
            url: Article URL
            timeout: Request timeout in seconds

        Returns:
            dict with 'success', 'content', 'title', 'error' keys
        """

        if not self.enabled:
            return {
                'success': False,
                'content': '',
                'title': '',
                'error': 'Jina API key not configured',
                'url': url
            }

        # Rate limiting
        elapsed = time.time() - self.last_request_time
        if elapsed < self.min_request_interval:
            time.sleep(self.min_request_interval - elapsed)

        self.total_requests += 1

        try:
            response = requests.get(
                f"{self.base_url}{url}",
                headers=self.headers,
                timeout=timeout
            )

            self.last_request_time = time.time()

            if response.status_code == 200:
                # Jina returns text content directly
                content = response.text
                self.successful_requests += 1

                return {
                    'success': True,
                    'content': content,
                    'title': '',  # Would need to parse from content
                    'word_count': len(content.split()),
                    'url': url,
                    'fetched_at': datetime.now().isoformat()
                }
            else:
                self.failed_requests += 1
                return {
                    'success': False,
                    'content': '',
                    'title': '',
                    'error': f"HTTP {response.status_code}",
                    'url': url
                }

        except Exception as e:
            self.failed_requests += 1
            return {
                'success': False,
                'content': '',
                'title': '',
                'error': str(e),
                'url': url
            }

    def enrich_dataframe(
        self,
        df: pd.DataFrame,
        url_column: str = 'url',
        max_articles: Optional[int] = None,
        show_progress: bool = True
    ) -> pd.DataFrame:
        """
        Enrich DataFrame with full-text content

        Args:
            df: DataFrame with article URLs
            url_column: Name of URL column
            max_articles: Limit number of articles to enrich (for testing)
            show_progress: Show progress bar

        Returns:
            DataFrame with additional columns: full_text, word_count, fetch_success
        """

        if not self.enabled:
            print("⚠️  Jina Reader not enabled - skipping full-text enrichment")
            df['full_text'] = df.get('title', '')
            df['word_count'] = df['full_text'].str.split().str.len()
            df['fetch_success'] = False
            return df

        # Prepare URLs
        urls = df[url_column].dropna().unique()

        if max_articles:
            urls = urls[:max_articles]
            print(f"⚠️  Limited to {max_articles} articles for testing")

        print(f"\n📥 Enriching {len(urls):,} articles with full text...")
        print(f"   Estimated cost: ${(len(urls) / 5000 * 29):.2f}")
        print(f"   Estimated time: {(len(urls) * 0.2 / 60):.1f} minutes")

        # Fetch articles
        results = []

        iterator = tqdm(urls, desc="Fetching") if show_progress else urls

        for url in iterator:
            result = self.fetch_article(url)
            results.append(result)

        # Convert to DataFrame
        results_df = pd.DataFrame(results)

        # Merge with original DataFrame
        enriched_df = df.merge(
            results_df[['url', 'content', 'word_count', 'success']],
            left_on=url_column,
            right_on='url',
            how='left',
            suffixes=('', '_jina')
        )

        # Rename columns
        enriched_df = enriched_df.rename(columns={
            'content': 'full_text',
            'success': 'fetch_success'
        })

        # Fill missing full_text with title
        enriched_df['full_text'] = enriched_df['full_text'].fillna(enriched_df.get('title', ''))
        enriched_df['fetch_success'] = enriched_df['fetch_success'].fillna(False)

        # Statistics
        success_rate = self.successful_requests / self.total_requests if self.total_requests > 0 else 0
        avg_word_count = enriched_df[enriched_df['fetch_success'] == True]['word_count'].mean()

        print(f"\n✓ Enrichment complete")
        print(f"   Success rate: {success_rate:.1%} ({self.successful_requests}/{self.total_requests})")
        if avg_word_count > 0:
            print(f"   Average word count: {avg_word_count:.0f} words")
        print(f"   Failed: {self.failed_requests} articles")

        return enriched_df

    def get_statistics(self) -> Dict:
        """Get enrichment statistics"""
        return {
            'total_requests': self.total_requests,
            'successful': self.successful_requests,
            'failed': self.failed_requests,
            'success_rate': self.successful_requests / self.total_requests if self.total_requests > 0 else 0,
            'estimated_cost_usd': (self.total_requests / 5000) * 29
        }
