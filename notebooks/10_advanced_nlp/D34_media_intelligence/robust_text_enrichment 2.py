"""
Robust Text Enrichment with Multi-Method Fallback
Fixes Jina Reader 10% success rate → Target 85%+

Fallback Chain:
1. Jina Reader API (fast, clean)
2. Newspaper3k (handles paywalls better)
3. Trafilatura (excellent for news sites)
4. BeautifulSoup (last resort, manual parsing)
5. Title fallback (if all else fails)
"""

import os
import time
import requests
from typing import Optional, Dict
import pandas as pd
from tqdm import tqdm

# Method-specific imports (install as needed)
try:
    from newspaper import Article
    NEWSPAPER_AVAILABLE = True
except ImportError:
    NEWSPAPER_AVAILABLE = False

try:
    import trafilatura
    TRAFILATURA_AVAILABLE = True
except ImportError:
    TRAFILATURA_AVAILABLE = False

from bs4 import BeautifulSoup


class RobustTextEnricher:
    """
    Multi-method text enrichment with graceful degradation

    Success Targets:
    - Jina Reader: 50-60% (fast, clean, but hits paywalls)
    - Newspaper3k: +20-25% (better paywall handling)
    - Trafilatura: +10-15% (good for news)
    - BeautifulSoup: +5% (last resort)
    - Total: 85-90%+ success rate
    """

    def __init__(self, jina_api_key: Optional[str] = None):
        """
        Initialize text enricher with multiple fallback methods

        Args:
            jina_api_key: Optional Jina API key (uses env var if not provided)
        """
        self.jina_api_key = jina_api_key or os.environ.get('JINA_API_KEY')
        self.jina_enabled = bool(self.jina_api_key)

        # User agents for rotation (avoid blocking)
        self.user_agents = [
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
        ]
        self.current_ua_idx = 0

        # Statistics tracking
        self.stats = {
            'total_attempts': 0,
            'jina_success': 0,
            'newspaper_success': 0,
            'trafilatura_success': 0,
            'beautifulsoup_success': 0,
            'title_fallback': 0,
            'total_failures': 0
        }

        print("🔧 Robust Text Enricher Initialized")
        print(f"   Jina Reader: {'✅ Enabled' if self.jina_enabled else '❌ Disabled'}")
        print(f"   Newspaper3k: {'✅ Available' if NEWSPAPER_AVAILABLE else '❌ Not installed'}")
        print(f"   Trafilatura: {'✅ Available' if TRAFILATURA_AVAILABLE else '❌ Not installed'}")
        print(f"   BeautifulSoup: ✅ Available (built-in)")

    def _get_next_user_agent(self) -> str:
        """Rotate user agents to avoid blocking"""
        ua = self.user_agents[self.current_ua_idx]
        self.current_ua_idx = (self.current_ua_idx + 1) % len(self.user_agents)
        return ua

    def _try_jina_reader(self, url: str) -> Optional[str]:
        """Method 1: Jina Reader API (50-60% success)"""
        if not self.jina_enabled:
            return None

        try:
            response = requests.get(
                f'https://r.jina.ai/{url}',
                headers={
                    'Authorization': f'Bearer {self.jina_api_key}',
                    'X-Return-Format': 'text'
                },
                timeout=10
            )

            if response.status_code == 200:
                text = response.text.strip()
                if len(text) > 200:  # Minimum viable article
                    self.stats['jina_success'] += 1
                    return text

            # Rate limit handling
            if response.status_code == 429:
                time.sleep(2)  # Wait before next attempt

        except Exception:
            pass  # Silent fail, try next method

        return None

    def _try_newspaper3k(self, url: str) -> Optional[str]:
        """Method 2: Newspaper3k (+20-25% success)"""
        if not NEWSPAPER_AVAILABLE:
            return None

        try:
            article = Article(url)
            article.download()
            article.parse()

            text = article.text.strip()
            if len(text) > 200:
                self.stats['newspaper_success'] += 1
                return text

        except Exception:
            pass

        return None

    def _try_trafilatura(self, url: str) -> Optional[str]:
        """Method 3: Trafilatura (+10-15% success)"""
        if not TRAFILATURA_AVAILABLE:
            return None

        try:
            downloaded = trafilatura.fetch_url(url)
            if downloaded:
                text = trafilatura.extract(downloaded)
                if text and len(text) > 200:
                    self.stats['trafilatura_success'] += 1
                    return text

        except Exception:
            pass

        return None

    def _try_beautifulsoup(self, url: str) -> Optional[str]:
        """Method 4: BeautifulSoup (+5% success)"""
        try:
            headers = {'User-Agent': self._get_next_user_agent()}
            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')

                # Remove script and style elements
                for script in soup(["script", "style"]):
                    script.decompose()

                # Try common content containers
                content = None
                for selector in ['article', '.article-content', '.post-content', 'main', '.content']:
                    element = soup.select_one(selector)
                    if element:
                        content = element.get_text()
                        break

                # Fallback to body
                if not content:
                    content = soup.get_text()

                # Clean up text
                lines = (line.strip() for line in content.splitlines())
                chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                text = '\n'.join(chunk for chunk in chunks if chunk)

                if len(text) > 200:
                    self.stats['beautifulsoup_success'] += 1
                    return text

        except Exception:
            pass

        return None

    def enrich_article(self, url: str, title: str = "") -> Dict[str, any]:
        """
        Enrich a single article with full text using fallback chain

        Args:
            url: Article URL
            title: Article title (fallback if all methods fail)

        Returns:
            Dict with 'text', 'method', 'success', 'word_count'
        """
        self.stats['total_attempts'] += 1

        # Try each method in order
        methods = [
            ('jina', self._try_jina_reader),
            ('newspaper', self._try_newspaper3k),
            ('trafilatura', self._try_trafilatura),
            ('beautifulsoup', self._try_beautifulsoup)
        ]

        for method_name, method_func in methods:
            text = method_func(url)
            if text:
                return {
                    'text': text,
                    'method': method_name,
                    'success': True,
                    'word_count': len(text.split())
                }

        # All methods failed - use title fallback
        self.stats['title_fallback'] += 1
        return {
            'text': title,
            'method': 'title_fallback',
            'success': False,
            'word_count': len(title.split()) if title else 0
        }

    def enrich_dataframe(
        self,
        df: pd.DataFrame,
        url_column: str = 'url',
        title_column: str = 'title',
        max_articles: Optional[int] = None,
        show_progress: bool = True
    ) -> pd.DataFrame:
        """
        Enrich entire dataframe with full text

        Args:
            df: Input dataframe
            url_column: Column containing URLs
            title_column: Column containing titles (fallback)
            max_articles: Limit processing (for testing/cost control)
            show_progress: Show progress bar

        Returns:
            Dataframe with new columns: full_text, extraction_method, word_count
        """
        df_enriched = df.copy()

        # Limit articles if specified
        if max_articles:
            df_enriched = df_enriched.head(max_articles)
            print(f"📊 Limited to {max_articles} articles for enrichment")

        print(f"\n🔄 Enriching {len(df_enriched)} articles with full text...")

        # Initialize result columns
        df_enriched['full_text'] = None
        df_enriched['extraction_method'] = None
        df_enriched['word_count'] = 0

        # Process each article
        iterator = tqdm(df_enriched.iterrows(), total=len(df_enriched), desc="Enriching") if show_progress else df_enriched.iterrows()

        for idx, row in iterator:
            url = row[url_column]
            title = row[title_column] if title_column in df_enriched.columns else ""

            # Enrich article
            result = self.enrich_article(url, title)

            # Store results
            df_enriched.at[idx, 'full_text'] = result['text']
            df_enriched.at[idx, 'extraction_method'] = result['method']
            df_enriched.at[idx, 'word_count'] = result['word_count']

            # Rate limiting (be nice to servers)
            time.sleep(0.2)  # 200ms between requests

        return df_enriched

    def get_statistics(self) -> Dict[str, any]:
        """Get enrichment statistics"""
        total = self.stats['total_attempts']
        if total == 0:
            return {'success_rate': 0.0, 'message': 'No articles processed yet'}

        successful = (
            self.stats['jina_success'] +
            self.stats['newspaper_success'] +
            self.stats['trafilatura_success'] +
            self.stats['beautifulsoup_success']
        )

        return {
            'total_articles': total,
            'successful_extractions': successful,
            'success_rate': successful / total,
            'method_breakdown': {
                'jina': f"{self.stats['jina_success']} ({self.stats['jina_success']/total*100:.1f}%)",
                'newspaper': f"{self.stats['newspaper_success']} ({self.stats['newspaper_success']/total*100:.1f}%)",
                'trafilatura': f"{self.stats['trafilatura_success']} ({self.stats['trafilatura_success']/total*100:.1f}%)",
                'beautifulsoup': f"{self.stats['beautifulsoup_success']} ({self.stats['beautifulsoup_success']/total*100:.1f}%)",
                'title_fallback': f"{self.stats['title_fallback']} ({self.stats['title_fallback']/total*100:.1f}%)"
            }
        }

    def print_statistics(self):
        """Print formatted statistics"""
        stats = self.get_statistics()

        print("\n" + "="*60)
        print("📊 TEXT ENRICHMENT STATISTICS")
        print("="*60)

        if 'message' in stats:
            print(f"\n{stats['message']}")
        else:
            print(f"\nTotal Articles: {stats['total_articles']}")
            print(f"Successful Extractions: {stats['successful_extractions']}")
            print(f"Success Rate: {stats['success_rate']:.1%}")

            print(f"\n🔍 Method Breakdown:")
            for method, count in stats['method_breakdown'].items():
                print(f"   {method.capitalize()}: {count}")

        print("="*60)
