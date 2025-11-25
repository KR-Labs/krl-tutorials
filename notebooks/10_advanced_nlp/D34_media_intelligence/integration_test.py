"""
Integration Test for Media Intelligence Clustering Improvements
Run this in a Jupyter cell BEFORE running the full notebook

Usage:
    %run lean_validation/integration_test.py
"""

def run_integration_tests():
    """Run comprehensive integration tests for all phases"""

    print("="*80)
    print("🧪 MEDIA INTELLIGENCE CLUSTERING - INTEGRATION TEST")
    print("="*80)

    results = {
        'passed': 0,
        'failed': 0,
        'warnings': 0
    }

    # Test 1: Syndication Handler
    print("\n[1/5] Testing Syndication Handler...")
    try:
        from syndication_handler import SyndicationHandler
        handler = SyndicationHandler()

        # Test with dummy data
        import pandas as pd
        df_test = pd.DataFrame({
            'lambda_spatial': [0.0, 0.0, 0.15, 0.4],
            'title': ['Wire Story A', 'Wire Story B', 'Local Story C', 'Local Story D']
        })

        df_syn, df_local = handler.separate_content(df_test)

        assert len(df_syn) == 2, "Should have 2 syndicated articles"
        assert len(df_local) == 2, "Should have 2 local articles"

        print("   ✅ PASS - Syndication separation works")
        results['passed'] += 1
    except Exception as e:
        print(f"   ❌ FAIL - {str(e)}")
        results['failed'] += 1

    # Test 2: Cluster Filtering
    print("\n[2/5] Testing Cluster Filtering...")
    try:
        from spatial_clustering import SpatialClusterer
        import numpy as np

        clusterer = SpatialClusterer()

        # Test with dummy data
        df_clusters = pd.DataFrame({
            'title': [f'Article {i}' for i in range(30)],
            'latitude': np.random.uniform(30, 40, 30),
            'longitude': np.random.uniform(-120, -80, 30),
            'cluster': [0]*15 + [1]*10 + [2]*5  # 2 valid, 1 small
        })

        df_filtered = clusterer.filter_small_clusters(df_clusters, min_size=10)

        assert len(df_filtered) == 25, "Should keep 25 articles (remove 5)"
        assert len(df_filtered['cluster'].unique()) == 2, "Should have 2 clusters"

        print("   ✅ PASS - Cluster filtering works")
        results['passed'] += 1
    except Exception as e:
        print(f"   ❌ FAIL - {str(e)}")
        results['failed'] += 1

    # Test 3: Text Cleaning
    print("\n[3/5] Testing Text Cleaning...")
    try:
        from robust_text_enrichment import aggressive_text_cleaning

        # Need >100 chars for cleaning to trigger
        polluted = """Skip to Content
Breadcrumb Trail Links
Home News Local News

This is the actual article content that should be preserved.
It contains important information about the economic policy changes.
The analysis continues with detailed statistics and expert quotes.

Share this Story
Follow Us on Twitter
Subscribe now for unlimited access
"""
        cleaned = aggressive_text_cleaning(polluted)

        assert 'Skip to Content' not in cleaned, "Navigation should be removed"
        assert 'article content' in cleaned, "Content should be preserved"
        assert len(cleaned) < len(polluted), "Should reduce text length"

        print("   ✅ PASS - Text cleaning works")
        results['passed'] += 1
    except Exception as e:
        print(f"   ❌ FAIL - {str(e)}")
        results['failed'] += 1

    # Test 4: Comprehensive Metrics
    print("\n[4/5] Testing Comprehensive Metrics...")
    try:
        from clustering_metrics import ClusteringEvaluator

        evaluator = ClusteringEvaluator()

        # Test with dummy data
        embeddings = np.random.rand(50, 384)
        labels = np.random.randint(0, 3, 50)

        eval_results = evaluator.evaluate(None, embeddings, labels)

        assert 'silhouette_score' in eval_results, "Should have silhouette score"
        assert 'davies_bouldin' in eval_results, "Should have Davies-Bouldin"
        assert 'calinski_harabasz' in eval_results, "Should have Calinski-Harabasz"

        print("   ✅ PASS - Comprehensive metrics work")
        results['passed'] += 1
    except Exception as e:
        print(f"   ❌ FAIL - {str(e)}")
        results['failed'] += 1

    # Test 5: Robust Statistics
    print("\n[5/5] Testing Robust Statistics...")
    try:
        from robust_statistics import RobustStatistics

        robust_stats = RobustStatistics(n_bootstrap=100)  # Low count for speed

        # Test with dummy data
        data = np.random.randn(20)  # Small sample (n=20)
        point_est, ci_lower, ci_upper = robust_stats.bootstrap_ci(data)

        assert ci_lower < point_est < ci_upper, "CI should contain point estimate"
        assert ci_upper - ci_lower > 0, "CI should have positive width"

        print("   ✅ PASS - Bootstrap statistics work")
        results['passed'] += 1
    except Exception as e:
        print(f"   ❌ FAIL - {str(e)}")
        results['failed'] += 1

    # Summary
    print("\n" + "="*80)
    print("INTEGRATION TEST SUMMARY")
    print("="*80)
    print(f"✅ Passed: {results['passed']}/5")
    print(f"❌ Failed: {results['failed']}/5")

    if results['failed'] == 0:
        print("\n🎉 ALL INTEGRATION TESTS PASSED!")
        print("\nYou are ready to:")
        print("  1. Reload VSCode (Cmd+Shift+P → 'Developer: Reload Window')")
        print("  2. Run cells 0-9 to create df_enriched")
        print("  3. Integrate modules per IMPLEMENTATION_COMPLETE.md")
        print("  4. Run full notebook and validate improvements")
        return True
    else:
        print("\n⚠️  SOME TESTS FAILED - Review errors above")
        print("\nTroubleshooting:")
        print("  1. Ensure all modules are in lean_validation/ directory")
        print("  2. Check for import errors or missing dependencies")
        print("  3. Review VALIDATION_RESULTS.md for details")
        return False


# Auto-run if executed directly
if __name__ == "__main__":
    run_integration_tests()
