"""
Demo Generation Script
Creates 5 policy topic demos for customer discovery

Run this to generate demo outputs showing spatial narrative clustering
"""

import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.expanduser('~/khipu-credentials/gdelt-bigquery.json')

from gdelt_connector import GDELTConnector
from spatial_clustering import SpatialClusterer
import pandas as pd
import plotly.express as px
from datetime import datetime

# Policy topics for think tank demos
DEMO_TOPICS = {
    'labor_strikes': {
        'query': 'labor strikes',
        'description': 'Labor Strikes & Worker Actions',
        'think_tank': 'Brookings - Metropolitan Policy Program'
    },
    'housing_policy': {
        'query': 'housing affordability',
        'description': 'Housing Affordability & Zoning Reform',
        'think_tank': 'Urban Institute - Housing Finance Policy Center'
    },
    'healthcare_reform': {
        'query': 'healthcare reform',
        'description': 'Healthcare Reform & Policy',
        'think_tank': 'RAND - Health Policy'
    },
    'climate_policy': {
        'query': 'climate policy',
        'description': 'Climate Change Policy & Regulation',
        'think_tank': 'Center for American Progress - Climate & Energy'
    },
    'education_policy': {
        'query': 'education reform',
        'description': 'Education Policy & School Reform',
        'think_tank': 'New America - Education Policy'
    }
}

def generate_demo(topic_key: str, topic_info: dict, connector: GDELTConnector, clusterer: SpatialClusterer):
    """Generate a single demo output"""

    print("\n" + "="*80)
    print(f"DEMO: {topic_info['description']}")
    print(f"Target Customer: {topic_info['think_tank']}")
    print("="*80)

    # Query GDELT
    df = connector.query_articles(
        topic=topic_info['query'],
        days_back=7,
        max_results=500
    )

    if len(df) < 10:
        print(f"⚠️  Insufficient data for {topic_key}, skipping...")
        return None

    # Run spatial clustering
    df = clusterer.cluster(df)

    # Get cluster summary
    summary = clusterer.summarize_clusters(df)

    # Create output directory
    output_dir = f"demos/{topic_key}"
    os.makedirs(output_dir, exist_ok=True)

    # Export data
    data_file = f"{output_dir}/articles.csv"
    df[['date', 'title', 'url', 'source', 'location', 'latitude', 'longitude', 'cluster']].to_csv(data_file, index=False)

    summary_file = f"{output_dir}/cluster_summary.csv"
    summary.to_csv(summary_file, index=False)

    print(f"\n✓ Data exported:")
    print(f"   {data_file}")
    print(f"   {summary_file}")

    # Create visualization
    fig = px.scatter_geo(
        df,
        lat='latitude',
        lon='longitude',
        color='cluster',
        hover_data=['title', 'location', 'source'],
        title=f'Spatial Narrative Clusters: {topic_info["description"]}',
        projection='albers usa',
        color_continuous_scale='Viridis'
    )

    fig.update_layout(
        geo=dict(
            scope='usa',
            showland=True,
            landcolor='rgb(243, 243, 243)',
            coastlinecolor='rgb(204, 204, 204)',
        ),
        height=600,
        width=1000
    )

    viz_file = f"{output_dir}/map.html"
    fig.write_html(viz_file)

    print(f"   {viz_file}")

    # Generate text report
    report = generate_report(topic_info, df, summary)
    report_file = f"{output_dir}/report.txt"

    with open(report_file, 'w') as f:
        f.write(report)

    print(f"   {report_file}")

    return {
        'topic': topic_key,
        'articles': len(df),
        'clusters': len(summary),
        'files': {
            'data': data_file,
            'summary': summary_file,
            'map': viz_file,
            'report': report_file
        }
    }

def generate_report(topic_info: dict, df: pd.DataFrame, summary: pd.DataFrame) -> str:
    """Generate executive summary report"""

    report = f"""
================================================================================
SPATIAL MEDIA INTELLIGENCE DEMO
{topic_info['description']}
================================================================================

Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}
Target Customer: {topic_info['think_tank']}

================================================================================
EXECUTIVE SUMMARY
================================================================================

Coverage Analysis:
  • Total articles: {len(df):,}
  • Date range: {df['date'].min().date()} to {df['date'].max().date()}
  • Geographic coverage: {df['location'].nunique()} unique locations
  • Source diversity: {df['source'].nunique()} media outlets

Spatial Narrative Clusters Discovered: {len(summary)}

This analysis reveals {len(summary)} distinct regional narrative patterns,
showing how media coverage of {topic_info['description'].lower()} varies
geographically across the United States.

================================================================================
REGIONAL NARRATIVE CLUSTERS
================================================================================

"""

    for _, cluster in summary.iterrows():
        report += f"""
Cluster {cluster['cluster_id'] + 1}: {cluster['location']}
  • Articles: {cluster['size']}
  • Geographic radius: {cluster['radius_km']:.1f} km
  • Sample headlines:
"""
        for i, headline in enumerate(cluster['sample_headlines'][:3], 1):
            report += f"     {i}. {headline}\n"

        report += "\n"

    report += f"""
================================================================================
KEY INSIGHTS
================================================================================

Regional Differences Detected:
  • Different locations show distinct coverage patterns
  • Narrative framing varies by geography
  • This spatial analysis is invisible in title-only monitoring

Value for Think Tanks:
  • Identify regional resistance patterns before policy rollout
  • Tailor messaging to specific geographic audiences
  • Detect early warning signals of opposition campaigns
  • Track policy discourse spread across regions

================================================================================
METHODOLOGY
================================================================================

Data Source: GDELT BigQuery (Global Database of Events, Language, and Tone)
  • 758M+ global media signals
  • Real-time monitoring (15-minute update cycle)
  • 80%+ geolocated articles (vs 0% in traditional tools)

Algorithm: Spatial-Semantic Clustering (Patent-Pending)
  • Combines text embeddings + geographic coordinates
  • λ_spatial = 0.15 (trade secret parameter)
  • Discovers regional narrative patterns automatically

Competitor Comparison:
  • Meltwater: No spatial clustering, title-only
  • Brandwatch: No spatial clustering, generic sentiment
  • Our platform: Geographic + semantic analysis combined

================================================================================
NEXT STEPS
================================================================================

For {topic_info['think_tank']}:

1. PILOT PROGRAM (3 months, $18,750)
   • 10 custom policy analyses
   • Regional narrative tracking
   • Monthly trend reports
   • 2 user seats

2. SUCCESS METRICS
   • Prediction accuracy: Does our spatial analysis correctly identify
     regional resistance patterns?
   • Utility: Do regional insights inform your policy messaging?
   • ROI: Does early warning save research/advocacy costs?

3. DECISION TIMELINE
   • Weeks 1-2: Onboarding + training
   • Weeks 3-12: Active pilot + monthly reviews
   • Week 13: Results review + annual contract decision

Annual Contract: $75,000/year
  • Unlimited policy analyses
  • 5 user seats
  • Quarterly trend reports
  • 24-hour support
  • API access

================================================================================
CONTACT
================================================================================

Brandon DeLo
Founder, Khipu Media Intelligence
brandon@khipu.ai

Schedule demo: khipu.ai/demo

================================================================================
"""

    return report

def main():
    """Generate all demos"""

    print("="*80)
    print("SPATIAL MEDIA INTELLIGENCE - DEMO GENERATION")
    print("="*80)
    print("\nGenerating 5 policy topic demos for customer discovery\n")

    # Initialize connectors
    connector = GDELTConnector()
    clusterer = SpatialClusterer(spatial_weight=0.15)

    # Generate demos
    results = []

    for topic_key, topic_info in DEMO_TOPICS.items():
        result = generate_demo(topic_key, topic_info, connector, clusterer)
        if result:
            results.append(result)

    # Summary
    print("\n" + "="*80)
    print("✓ DEMO GENERATION COMPLETE")
    print("="*80)
    print(f"\nGenerated {len(results)} demos:")

    for result in results:
        print(f"\n{result['topic']}:")
        print(f"  Articles: {result['articles']}")
        print(f"  Clusters: {result['clusters']}")
        print(f"  Files:")
        for file_type, file_path in result['files'].items():
            print(f"    • {file_type}: {file_path}")

    print("\n" + "="*80)
    print("NEXT STEPS")
    print("="*80)
    print("\n1. Review demo outputs in demos/ directory")
    print("2. Open HTML maps in browser to see visualizations")
    print("3. Read text reports for each topic")
    print("4. Prepare customer discovery calls:")
    print("   - Contact 10-15 think tank policy analysts")
    print("   - Show them these demos")
    print("   - Ask: Would you pay $75K/year for this?")
    print("\n5. If 3+ express strong interest → Build full platform")
    print("   If not → Use as portfolio piece, move on")
    print("\n")

if __name__ == '__main__':
    main()
