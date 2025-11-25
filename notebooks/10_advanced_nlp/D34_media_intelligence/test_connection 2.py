"""
Test BigQuery connection and run a quick sample query
"""

import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.expanduser('~/khipu-credentials/gdelt-bigquery.json')

from gdelt_connector import GDELTConnector

def main():
    print("="*80)
    print("TESTING BIGQUERY CONNECTION")
    print("="*80)

    try:
        # Initialize connector
        connector = GDELTConnector()

        # Run test query
        print("\nRunning test query (labor strikes, last 3 days)...")
        df = connector.query_articles(
            topic='labor strikes',
            days_back=3,
            max_results=50
        )

        if len(df) == 0:
            print("\n⚠️  No results found. Try:")
            print("   - Broader search terms")
            print("   - Longer time range (days_back=7)")
            return

        # Show sample
        print("\n📊 Sample Results (first 5):")
        print(df[['date', 'title', 'location', 'latitude', 'longitude']].head().to_string(index=False))

        # Stats
        print(f"\n📈 Statistics:")
        print(f"   Total articles: {len(df)}")
        print(f"   Geolocated: {df['latitude'].notna().sum()} ({df['latitude'].notna().sum()/len(df)*100:.1f}%)")
        print(f"   Unique locations: {df['location'].nunique()}")
        print(f"   Unique sources: {df['source'].nunique()}")

        print("\n" + "="*80)
        print("✓ CONNECTION TEST PASSED")
        print("="*80)
        print("\nYou're ready to generate demos!")
        print("Run: python generate_demos.py")

    except Exception as e:
        print(f"\n❌ Connection test failed: {e}")
        print("\nTroubleshooting:")
        print("1. Verify credentials exist:")
        print("   ls -l ~/khipu-credentials/gdelt-bigquery.json")
        print("2. Verify environment variable:")
        print("   echo $GOOGLE_APPLICATION_CREDENTIALS")
        print("3. Re-run setup script:")
        print("   bash setup_bigquery.sh")

if __name__ == '__main__':
    main()
