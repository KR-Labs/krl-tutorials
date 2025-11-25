"""
Advanced Sentiment Analysis
Multi-level sentiment extraction from full-text articles

Improvements over basic sentiment on titles:
- Context-aware sentiment (full article vs headline)
- Aspect-based sentiment (policy, workers, companies)
- Sentiment trajectory detection
"""

from transformers import pipeline
import pandas as pd
import numpy as np
from typing import Dict, List
import warnings
warnings.filterwarnings('ignore')

class AdvancedSentimentAnalyzer:
    """
    Deep sentiment analysis using transformer models

    Capabilities:
    - Overall article sentiment
    - Aspect-based sentiment (policy, workers, management)
    - Sentiment trajectory (does article sentiment shift?)
    """

    def __init__(self, model_name: str = "cardiffnlp/twitter-roberta-base-sentiment-latest"):
        """Initialize sentiment analysis pipeline"""

        print("🎭 Initializing Advanced Sentiment Analyzer...")
        print(f"   Loading transformer model: {model_name}")

        try:
            self.sentiment_pipeline = pipeline(
                "sentiment-analysis",
                model=model_name,
                max_length=512,
                truncation=True
            )
            self.enabled = True
        except Exception as e:
            print(f"⚠️  Failed to load sentiment model: {e}")
            print("   Sentiment analysis will be skipped")
            self.enabled = False
            return

        # Aspect keywords for aspect-based sentiment
        self.aspect_keywords = {
            'workers': ['worker', 'employee', 'union', 'labor', 'staff', 'workforce'],
            'management': ['management', 'company', 'employer', 'corporation', 'executive'],
            'policy': ['policy', 'regulation', 'law', 'legislation', 'government'],
            'economy': ['economy', 'economic', 'wage', 'salary', 'income', 'cost']
        }

        print("✓ Sentiment analyzer ready")

    def analyze_text(self, text: str, chunk_size: int = 500) -> Dict:
        """
        Analyze sentiment of full text

        For long articles, analyzes in chunks and aggregates

        Args:
            text: Article full text
            chunk_size: Words per chunk (transformer has 512 token limit)

        Returns:
            dict with overall sentiment and trajectory
        """

        if not self.enabled or not text or len(str(text).strip()) < 10:
            return {
                'overall_sentiment': 'neutral',
                'overall_score': 0.0,
                'confidence': 0.0,
                'trajectory': 'stable'
            }

        # Split into chunks
        words = str(text).split()
        chunks = [
            ' '.join(words[i:i+chunk_size])
            for i in range(0, len(words), chunk_size)
        ]

        # Analyze each chunk
        chunk_sentiments = []

        for chunk in chunks:
            try:
                result = self.sentiment_pipeline(chunk)[0]

                # Convert to numeric score (-1 to 1)
                label = result['label'].lower()
                score_map = {'negative': -1, 'neutral': 0, 'positive': 1}
                score = score_map.get(label, 0) * result['score']

                chunk_sentiments.append({
                    'label': label,
                    'score': score,
                    'confidence': result['score']
                })
            except:
                continue

        if not chunk_sentiments:
            return {
                'overall_sentiment': 'neutral',
                'overall_score': 0.0,
                'confidence': 0.0,
                'trajectory': 'stable'
            }

        # Aggregate sentiment
        avg_score = np.mean([s['score'] for s in chunk_sentiments])
        avg_confidence = np.mean([s['confidence'] for s in chunk_sentiments])

        # Determine overall label
        if avg_score > 0.1:
            overall_label = 'positive'
        elif avg_score < -0.1:
            overall_label = 'negative'
        else:
            overall_label = 'neutral'

        # Detect sentiment trajectory
        if len(chunk_sentiments) >= 3:
            first_third = np.mean([s['score'] for s in chunk_sentiments[:len(chunk_sentiments)//3]])
            last_third = np.mean([s['score'] for s in chunk_sentiments[-len(chunk_sentiments)//3:]])

            if last_third - first_third > 0.2:
                trajectory = 'improving'
            elif first_third - last_third > 0.2:
                trajectory = 'declining'
            else:
                trajectory = 'stable'
        else:
            trajectory = 'stable'

        return {
            'overall_sentiment': overall_label,
            'overall_score': float(avg_score),
            'confidence': float(avg_confidence),
            'trajectory': trajectory,
            'chunk_count': len(chunk_sentiments)
        }

    def analyze_aspects(self, text: str) -> Dict[str, float]:
        """
        Aspect-based sentiment analysis

        Extracts sentiment for specific aspects:
        - Workers/unions
        - Management/companies
        - Policy/regulation
        - Economy/wages

        Args:
            text: Article full text

        Returns:
            dict of {aspect: sentiment_score}
        """

        if not self.enabled or not text:
            return {aspect: 0.0 for aspect in self.aspect_keywords.keys()}

        aspect_sentiments = {}
        text_str = str(text)

        for aspect, keywords in self.aspect_keywords.items():
            # Find sentences mentioning this aspect
            sentences = text_str.split('.')
            relevant_sentences = [
                sent for sent in sentences
                if any(kw in sent.lower() for kw in keywords)
            ]

            if not relevant_sentences:
                aspect_sentiments[aspect] = 0.0
                continue

            # Analyze sentiment of relevant sentences
            aspect_text = '. '.join(relevant_sentences[:5])  # Max 5 sentences

            try:
                result = self.sentiment_pipeline(aspect_text[:512])[0]
                label = result['label'].lower()
                score_map = {'negative': -1, 'neutral': 0, 'positive': 1}
                score = score_map.get(label, 0) * result['score']
                aspect_sentiments[aspect] = float(score)
            except:
                aspect_sentiments[aspect] = 0.0

        return aspect_sentiments

    def analyze_dataframe(
        self,
        df: pd.DataFrame,
        text_column: str = 'full_text',
        analyze_aspects: bool = True
    ) -> pd.DataFrame:
        """
        Analyze sentiment for entire DataFrame

        Args:
            df: DataFrame with full text
            text_column: Column containing article text
            analyze_aspects: Whether to perform aspect-based analysis

        Returns:
            DataFrame with sentiment columns added
        """

        if not self.enabled:
            print("⚠️  Sentiment analyzer not enabled - skipping")
            return df

        print(f"\n🎭 Analyzing sentiment for {len(df):,} articles...")

        # Overall sentiment
        sentiments = df[text_column].apply(self.analyze_text)

        df['sentiment_deep'] = sentiments.apply(lambda x: x['overall_sentiment'])
        df['sentiment_deep_score'] = sentiments.apply(lambda x: x['overall_score'])
        df['sentiment_confidence'] = sentiments.apply(lambda x: x['confidence'])
        df['sentiment_trajectory'] = sentiments.apply(lambda x: x['trajectory'])

        # Aspect-based sentiment
        if analyze_aspects:
            print("   Extracting aspect-based sentiment...")
            aspects = df[text_column].apply(self.analyze_aspects)

            for aspect in self.aspect_keywords.keys():
                df[f'sentiment_{aspect}'] = aspects.apply(lambda x: x.get(aspect, 0.0))

        # Summary statistics
        print(f"\n✓ Sentiment analysis complete")
        print(f"   Distribution:")
        print(df['sentiment_deep'].value_counts().to_string())

        if analyze_aspects:
            print(f"\n   Average aspect sentiments:")
            for aspect in self.aspect_keywords.keys():
                avg = df[f'sentiment_{aspect}'].mean()
                print(f"      {aspect.capitalize()}: {avg:+.3f}")

        return df
