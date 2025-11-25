"""
GDELT BigQuery Connector - Lean Validation Version
Simplified connector for demo generation
"""

from google.cloud import bigquery
import pandas as pd
from datetime import datetime, timedelta
import os

class GDELTConnector:
    """Query GDELT BigQuery for geolocated articles"""

    def __init__(self):
        self.client = bigquery.Client()
        print(f"✓ BigQuery client initialized (Project: {self.client.project})")

    def query_articles(
        self,
        topic: str,
        days_back: int = 7,
        max_results: int = 500
    ) -> pd.DataFrame:
        """
        Query GDELT for recent articles on a topic

        Args:
            topic: Search terms (e.g., "labor strikes")
            days_back: How many days of history
            max_results: Maximum articles to return

        Returns:
            DataFrame with geolocated articles
        """

        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back)

        # Build query - GDELT GKG has Locations as delimited string
        query = f"""
        SELECT
            DATE as date,
            SourceCommonName as source,
            DocumentIdentifier as url,
            V2Locations as locations_raw,
            Themes
        FROM `gdelt-bq.gdeltv2.gkg_partitioned`
        WHERE _PARTITIONTIME BETWEEN TIMESTAMP('{start_date.strftime('%Y-%m-%d')}')
                                  AND TIMESTAMP('{end_date.strftime('%Y-%m-%d')}')
          AND V2Locations IS NOT NULL
          AND V2Locations LIKE '%US#%'
          AND (
              LOWER(DocumentIdentifier) LIKE '%{topic.lower().replace(' ', '%')}%'
              OR LOWER(Themes) LIKE '%{topic.upper().replace(' ', '_')}%'
          )
        ORDER BY DATE DESC
        LIMIT {max_results * 2}
        """

        print(f"\n🔍 Querying GDELT...")
        print(f"   Topic: {topic}")
        print(f"   Date range: {start_date.date()} to {end_date.date()}")

        # Execute query
        query_job = self.client.query(query)
        df = query_job.to_dataframe()

        if len(df) == 0:
            print(f"⚠️  No articles found")
            return pd.DataFrame()

        # Parse dates
        df['date'] = pd.to_datetime(df['date'], format='%Y%m%d%H%M%S')

        # Extract titles from URLs
        df['title'] = df['url'].apply(self._extract_title)

        # Parse location data from V2Locations
        df = self._parse_locations(df)

        # Filter for valid US locations
        df = df[df['latitude'].notna() & df['longitude'].notna()].copy()
        df = df.head(max_results)

        if len(df) == 0:
            print(f"⚠️  No geolocated articles found")
            return pd.DataFrame()

        # Stats
        geo_pct = 100.0  # Already filtered for geolocated

        print(f"✓ Retrieved {len(df)} articles")
        print(f"  Geolocated: {geo_pct:.1f}%")
        print(f"  Locations: {df['location'].nunique()}")
        print(f"  Sources: {df['source'].nunique()}")

        return df

    def _parse_locations(self, df: pd.DataFrame) -> pd.DataFrame:
        """Parse V2Locations column to extract US location data"""
        locations = []
        latitudes = []
        longitudes = []

        for _, row in df.iterrows():
            loc_str = row['locations_raw']
            if not isinstance(loc_str, str):
                locations.append(None)
                latitudes.append(None)
                longitudes.append(None)
                continue

            # V2Locations format: type#name#countrycode#statecode##lat#lon#...
            # Split by semicolon to get individual locations
            location_records = loc_str.split(';')

            # Find first US location with valid coordinates
            found = False
            for loc_record in location_records:
                parts = loc_record.split('#')
                if len(parts) >= 7:
                    try:
                        country = parts[2] if len(parts) > 2 else ''
                        if country == 'US':
                            location_name = parts[1]
                            lat = float(parts[5])
                            lon = float(parts[6])

                            locations.append(location_name)
                            latitudes.append(lat)
                            longitudes.append(lon)
                            found = True
                            break
                    except (ValueError, IndexError):
                        continue

            if not found:
                locations.append(None)
                latitudes.append(None)
                longitudes.append(None)

        df['location'] = locations
        df['latitude'] = latitudes
        df['longitude'] = longitudes

        return df

    def _extract_title(self, url: str) -> str:
        """Extract title from URL"""
        if not isinstance(url, str):
            return "Untitled"

        parts = url.split('/')
        if len(parts) > 0:
            slug = parts[-1].split('?')[0]
            slug = slug.replace('.html', '').replace('.htm', '')
            slug = slug.replace('-', ' ').replace('_', ' ')
            return slug.title()[:100]
        return "Untitled"
