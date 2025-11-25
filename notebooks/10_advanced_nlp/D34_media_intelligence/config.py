"""
Centralized Configuration for Media Intelligence Notebook

Provides configuration management with presets and auto-detection of paths.
"""

import os
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class NotebookConfig:
    """Centralized configuration for media intelligence notebook"""

    # Paths (auto-detect or use environment variables)
    project_root: Path = Path(__file__).parent
    env_path: Optional[Path] = None
    credentials_path: Optional[Path] = None
    output_dir: Optional[Path] = None

    # Analysis parameters
    topic: str = 'tariffs'
    days_back: int = 60  # Increased from 21 for better coverage (1,000-1,500 articles)
    max_articles: int = 2000  # Increased from 1,000 for statistical power

    # Clustering
    spatial_weight: float = 0.15
    distance_threshold: float = 0.5
    min_cluster_size: int = 2

    # Text enrichment
    enable_text_enrichment: bool = True
    max_articles_to_enrich: int = 800  # Increased from 500 to match larger dataset
    enrichment_strategy: str = 'stratified'  # 'random', 'stratified', 'all'

    # Sentiment analysis
    enable_advanced_sentiment: bool = True
    sentiment_threshold_method: str = 'adaptive'  # 'adaptive', 'fixed', 'keyword'

    # Causal analysis
    enable_causal_bias: bool = True
    min_articles_per_outlet: int = 2  # LOWERED from 5 to 2

    # Visualization
    enable_advanced_viz: bool = True

    def __post_init__(self):
        """Validate and setup configuration"""
        # Set output directory
        if self.output_dir is None:
            self.output_dir = self.project_root / 'outputs'

        # Create output directory
        self.output_dir.mkdir(exist_ok=True)

        # Auto-detect .env file
        if self.env_path is None:
            # Try common locations
            possible_env = [
                self.project_root / '.env',
                self.project_root.parent / '.env',
                self.project_root.parent.parent / '.env',
                Path.home() / 'Documents' / 'GitHub' / 'KRL' / 'krl-tutorials' / '.env'
            ]
            for path in possible_env:
                if path.exists():
                    self.env_path = path
                    break

        # Auto-detect credentials
        if self.credentials_path is None:
            # Try common locations
            possible_creds = [
                Path.home() / 'khipu-credentials' / 'gdelt-bigquery.json',
                Path.home() / '.config' / 'gcloud' / 'gdelt-bigquery.json',
                self.project_root / 'credentials' / 'gdelt-bigquery.json'
            ]
            for path in possible_creds:
                if path.exists():
                    self.credentials_path = path
                    break

        # Validate
        if self.env_path is None or not self.env_path.exists():
            print(f"⚠️  Warning: .env file not found")

        if self.credentials_path is None or not self.credentials_path.exists():
            print(f"⚠️  Warning: GCP credentials not found. BigQuery may fail.")

    def to_dict(self):
        """Export as dictionary"""
        result = {}
        for k, v in asdict(self).items():
            if isinstance(v, Path):
                result[k] = str(v)
            else:
                result[k] = v
        return result

    def display(self):
        """Print configuration summary"""
        print("=" * 80)
        print("🎛️  ANALYSIS CONFIGURATION")
        print("=" * 80)
        print(f"\n📊 Topic: '{self.topic}'")
        print(f"📅 Time Period: {self.days_back} days back")
        print(f"📈 Max Articles: {self.max_articles:,}")
        print(f"🎯 Spatial Weight (λ): {self.spatial_weight}")
        print(f"🔍 Distance Threshold: {self.distance_threshold}")
        print(f"\n🔧 Features:")
        print(f"   • Text Enrichment: {'✅ Enabled' if self.enable_text_enrichment else '❌ Disabled'}")
        if self.enable_text_enrichment:
            print(f"     - Max articles: {self.max_articles_to_enrich}")
            print(f"     - Strategy: {self.enrichment_strategy}")
        print(f"   • Advanced Sentiment: {'✅ Enabled' if self.enable_advanced_sentiment else '❌ Disabled'}")
        if self.enable_advanced_sentiment:
            print(f"     - Threshold method: {self.sentiment_threshold_method}")
        print(f"   • Causal Bias: {'✅ Enabled' if self.enable_causal_bias else '❌ Disabled'}")
        if self.enable_causal_bias:
            print(f"     - Min articles per outlet: {self.min_articles_per_outlet}")
        print(f"   • Advanced Viz: {'✅ Enabled' if self.enable_advanced_viz else '❌ Disabled'}")
        print(f"\n📁 Paths:")
        print(f"   • Project root: {self.project_root}")
        print(f"   • Output dir: {self.output_dir}")
        if self.env_path:
            print(f"   • .env file: {self.env_path}")
        if self.credentials_path:
            print(f"   • Credentials: {self.credentials_path}")
        print("=" * 80)


# ============================================================================
# PRESET CONFIGURATIONS
# ============================================================================

QUICK_DEMO = NotebookConfig(
    topic='housing affordability',
    days_back=7,
    max_articles=200,
    enable_text_enrichment=False,
    enable_advanced_sentiment=False,
    enable_causal_bias=False,
    enable_advanced_viz=True
)

STANDARD_ANALYSIS = NotebookConfig(
    topic='housing affordability',
    days_back=60,  # Increased from 21 to get 1,000-1,500 articles
    max_articles=2000,  # Increased from 1,000 for better statistical power
    max_articles_to_enrich=800,  # Increased proportionally
    enable_text_enrichment=True,
    enable_advanced_sentiment=True,
    enable_causal_bias=True,
    enable_advanced_viz=True
)

COMPREHENSIVE_RESEARCH = NotebookConfig(
    topic='tariffs',
    days_back=90,  # Increased from 30 for maximum coverage
    max_articles=5000,  # Increased from 2,000 for production-scale analysis
    max_articles_to_enrich=1500,  # Increased proportionally
    enable_text_enrichment=True,
    enable_advanced_sentiment=True,
    enable_causal_bias=True,
    enable_advanced_viz=True
)


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_config_from_preset(preset_name: str) -> NotebookConfig:
    """Get configuration from preset name"""
    presets = {
        'quick': QUICK_DEMO,
        'standard': STANDARD_ANALYSIS,
        'comprehensive': COMPREHENSIVE_RESEARCH
    }
    return presets.get(preset_name.lower(), STANDARD_ANALYSIS)


if __name__ == '__main__':
    # Test configuration
    print("Testing configuration system...\n")

    print("PRESET 1: Quick Demo")
    QUICK_DEMO.display()

    print("\n\nPRESET 2: Standard Analysis")
    STANDARD_ANALYSIS.display()

    print("\n\nPRESET 3: Comprehensive Research")
    COMPREHENSIVE_RESEARCH.display()
