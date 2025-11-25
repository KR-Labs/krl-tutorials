"""
Causal Bias Detection
Deconfounded media bias analysis using propensity score matching

Novel Contribution:
- Traditional: Correlation between outlet + coverage tone
- Our innovation: Isolate causal editorial bias from legitimate newsworthiness
- Method: Propensity score weighting to control for confounders

Confounders:
- Event severity (major strike vs minor dispute)
- Geographic location (coastal vs inland, urban vs rural)
- Timing (news cycle, other events)
- Article length (comprehensive vs brief)

Use Case:
Distinguish true bias from justified coverage differences:
- Outlet A covers strike negatively because it was violent (justified)
- Outlet B covers similar strike negatively despite being peaceful (bias)
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from typing import Dict, List, Tuple
import warnings
warnings.filterwarnings('ignore')

class CausalBiasDetector:
    """
    Detect editorial bias using causal inference methods

    This is advanced functionality - requires causal inference understanding
    """

    def __init__(self):
        """Initialize causal bias detector"""

        print("🔬 Initializing Causal Bias Detector...")
        print("   Method: Propensity Score Matching + Inverse Probability Weighting")

        self.propensity_model = None
        self.scaler = StandardScaler()

        print("✓ Causal bias detector ready")

    def prepare_confounders(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Extract confounding variables that affect both treatment and outcome

        Treatment: Outlet choice (which outlet covers the story)
        Outcome: Coverage sentiment
        Confounders: Event characteristics that legitimately affect both

        Args:
            df: DataFrame with articles

        Returns:
            DataFrame with confounder features
        """

        confounders = df.copy()

        # Confounder 1: Event severity (from sentiment + keywords)
        severity_keywords = ['violence', 'clash', 'shutdown', 'crisis', 'emergency']
        confounders['event_severity'] = confounders['full_text'].apply(
            lambda x: sum(1 for kw in severity_keywords if kw in str(x).lower()) if pd.notna(x) else 0
        )

        # Confounder 2: Geographic region (affects local vs national coverage)
        coastal_states = ['CA', 'NY', 'FL', 'WA', 'OR', 'MA', 'CT', 'NJ']
        confounders['is_coastal'] = confounders.get('state_code', pd.Series()).apply(
            lambda x: 1 if x in coastal_states else 0
        )

        # Confounder 3: Timing (weekend vs weekday)
        confounders['is_weekend'] = pd.to_datetime(confounders['date']).dt.dayofweek.isin([5, 6]).astype(int)

        # Confounder 4: Article length (comprehensive vs brief)
        if 'word_count' in confounders.columns:
            max_words = confounders['word_count'].max()
            confounders['word_count_normalized'] = confounders['word_count'] / max_words if max_words > 0 else 0
        else:
            confounders['word_count_normalized'] = 0

        # Confounder 5: Has official statement (credibility)
        official_keywords = ['official', 'spokesperson', 'statement', 'announced']
        confounders['has_official_source'] = confounders['full_text'].apply(
            lambda x: 1 if pd.notna(x) and any(kw in str(x).lower() for kw in official_keywords) else 0
        )

        return confounders

    def estimate_propensity_scores(
        self,
        df: pd.DataFrame,
        treatment_col: str = 'source',
        confounder_cols: List[str] = None
    ) -> pd.DataFrame:
        """
        Estimate propensity scores: P(Treatment | Confounders)

        Treatment = Outlet assignment (which outlet covered the story)
        Propensity score = Probability of being covered by this outlet
                          given event characteristics

        Args:
            df: DataFrame with confounders
            treatment_col: Column indicating treatment (outlet)
            confounder_cols: List of confounder columns

        Returns:
            DataFrame with propensity scores added
        """

        if confounder_cols is None:
            confounder_cols = [
                'event_severity', 'is_coastal', 'is_weekend',
                'word_count_normalized', 'has_official_source'
            ]

        print(f"\n🎯 Estimating propensity scores...")
        print(f"   Treatment: {treatment_col}")
        print(f"   Confounders: {', '.join(confounder_cols)}")

        # Prepare features
        X = df[confounder_cols].fillna(0)
        X_scaled = self.scaler.fit_transform(X)

        df_with_scores = df.copy()

        # Calculate propensity scores for top outlets
        top_outlets = df[treatment_col].value_counts().head(10).index

        for outlet in top_outlets:
            # Binary treatment: this outlet vs others
            y = (df[treatment_col] == outlet).astype(int)

            if y.sum() < 5:  # Need at least 5 examples
                continue

            try:
                # Fit propensity model
                prop_model = LogisticRegression(max_iter=1000, random_state=42)
                prop_model.fit(X_scaled, y)

                # Predict propensity scores
                prop_scores = prop_model.predict_proba(X_scaled)[:, 1]

                # Clip extreme values
                prop_scores = np.clip(prop_scores, 0.01, 0.99)

                df_with_scores[f'propensity_{outlet}'] = prop_scores
            except:
                continue

        print(f"✓ Propensity scores estimated for {len(top_outlets)} outlets")

        return df_with_scores

    def calculate_ipw_weights(
        self,
        df: pd.DataFrame,
        outlet: str,
        treatment_col: str = 'source'
    ) -> np.ndarray:
        """
        Calculate Inverse Probability Weighting (IPW) weights

        IPW weights balance the confounders between treated and control groups

        Formula:
        - Treated group: 1 / propensity_score
        - Control group: 1 / (1 - propensity_score)

        Args:
            df: DataFrame with propensity scores
            outlet: Outlet to analyze
            treatment_col: Column indicating treatment

        Returns:
            Array of IPW weights
        """

        prop_col = f'propensity_{outlet}'

        if prop_col not in df.columns:
            raise ValueError(f"Propensity scores not found for {outlet}")

        is_treated = (df[treatment_col] == outlet).astype(int)
        prop_scores = df[prop_col]

        # IPW formula
        weights = np.where(
            is_treated == 1,
            1 / prop_scores,
            1 / (1 - prop_scores)
        )

        # Stabilize extreme weights
        weights = np.clip(weights, 0.1, 10)

        return weights

    def estimate_causal_bias(
        self,
        df: pd.DataFrame,
        outlet: str,
        outcome_col: str = 'sentiment_deep_score',
        treatment_col: str = 'source'
    ) -> Dict:
        """
        Estimate causal editorial bias for an outlet

        Compares:
        - Observed coverage sentiment (confounded)
        - Deconfounded coverage sentiment (causal effect)

        Args:
            df: DataFrame with propensity scores and outcomes
            outlet: Outlet to analyze
            outcome_col: Sentiment score column
            treatment_col: Column indicating treatment

        Returns:
            dict with bias estimates
        """

        try:
            # Calculate IPW weights
            weights = self.calculate_ipw_weights(df, outlet, treatment_col)

            # Treatment indicator
            is_treated = (df[treatment_col] == outlet).astype(int)

            # Outcomes
            outcomes = df[outcome_col].fillna(0)

            # Weighted means
            treated_mean = np.average(
                outcomes[is_treated == 1],
                weights=weights[is_treated == 1]
            )

            control_mean = np.average(
                outcomes[is_treated == 0],
                weights=weights[is_treated == 0]
            )

            # Average Treatment Effect (ATE)
            # Positive = outlet more negative than justified
            # Negative = outlet more positive than justified
            causal_bias = treated_mean - control_mean

            # Observed difference (confounded)
            observed_treated = outcomes[is_treated == 1].mean()
            observed_control = outcomes[is_treated == 0].mean()
            observed_diff = observed_treated - observed_control

            # Confounding = Observed - Causal
            confounding_effect = observed_diff - causal_bias

            return {
                'outlet': outlet,
                'causal_bias': float(causal_bias),
                'observed_difference': float(observed_diff),
                'confounding_effect': float(confounding_effect),
                'treated_articles': int(is_treated.sum()),
                'control_articles': int((~is_treated.astype(bool)).sum()),
                'interpretation': self._interpret_bias(causal_bias)
            }
        except Exception as e:
            return {
                'outlet': outlet,
                'causal_bias': 0.0,
                'observed_difference': 0.0,
                'confounding_effect': 0.0,
                'treated_articles': 0,
                'control_articles': 0,
                'interpretation': f'Error: {str(e)}'
            }

    def _interpret_bias(self, bias_score: float) -> str:
        """Interpret bias score"""

        if abs(bias_score) < 0.05:
            return "No significant editorial bias detected"
        elif bias_score > 0.2:
            return "Strong negative editorial bias (coverage more negative than justified)"
        elif bias_score > 0.05:
            return "Moderate negative editorial bias"
        elif bias_score < -0.2:
            return "Strong positive editorial bias (coverage more positive than justified)"
        elif bias_score < -0.05:
            return "Moderate positive editorial bias"
        else:
            return "Minimal bias"

    def analyze_all_outlets(
        self,
        df: pd.DataFrame,
        min_articles: int = 10,
        treatment_col: str = 'source',
        outcome_col: str = 'sentiment_deep_score'
    ) -> pd.DataFrame:
        """
        Analyze causal bias for all outlets with sufficient coverage

        Args:
            df: DataFrame with propensity scores
            min_articles: Minimum articles required
            treatment_col: Column indicating treatment
            outcome_col: Sentiment score column

        Returns:
            DataFrame with bias estimates for each outlet
        """

        print(f"\n🔬 Analyzing causal bias for all outlets...")

        # Get outlets with sufficient coverage
        outlet_counts = df[treatment_col].value_counts()
        outlets_to_analyze = outlet_counts[outlet_counts >= min_articles].index

        print(f"   Analyzing {len(outlets_to_analyze)} outlets with ≥{min_articles} articles")

        results = []

        for outlet in outlets_to_analyze:
            bias_estimate = self.estimate_causal_bias(df, outlet, outcome_col, treatment_col)
            results.append(bias_estimate)

        results_df = pd.DataFrame(results)
        if len(results_df) > 0:
            results_df = results_df.sort_values('causal_bias', key=abs, ascending=False)

        print(f"\n✓ Bias analysis complete for {len(results_df)} outlets")

        return results_df
