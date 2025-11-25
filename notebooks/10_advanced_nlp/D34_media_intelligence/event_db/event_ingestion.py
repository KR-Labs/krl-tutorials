"""
GDELT Event Database Ingestion Pipeline

Downloads GDELT 2.0 Event Database CSV files and loads them into PostgreSQL.
Handles:
- CSV download with retry logic
- Parsing 58-column GDELT schema
- Batch insertion with error handling
- CAMEO code categorization
- Duplicate detection

Author: KRL Team
"""

import logging
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from urllib.parse import urljoin

import pandas as pd
import psycopg2
import requests
from psycopg2 import sql
from psycopg2.extras import execute_batch

from .config import (
    DATABASE_CONFIG, GDELT_CONFIG, INGESTION_CONFIG,
    get_database_url, DATA_DIR
)
from .cameo_mapping import CAMEOMapper

logger = logging.getLogger(__name__)


class GDELTEventIngestion:
    """GDELT Event Database CSV ingestion pipeline."""
    
    # GDELT Event DB column names (58 columns)
    GDELT_COLUMNS = [
        'GLOBALEVENTID', 'SQLDATE', 'MonthYear', 'Year', 'FractionDate',
        'Actor1Code', 'Actor1Name', 'Actor1CountryCode', 'Actor1KnownGroupCode',
        'Actor1EthnicCode', 'Actor1Religion1Code', 'Actor1Religion2Code',
        'Actor1Type1Code', 'Actor1Type2Code', 'Actor1Type3Code',
        'Actor2Code', 'Actor2Name', 'Actor2CountryCode', 'Actor2KnownGroupCode',
        'Actor2EthnicCode', 'Actor2Religion1Code', 'Actor2Religion2Code',
        'Actor2Type1Code', 'Actor2Type2Code', 'Actor2Type3Code',
        'IsRootEvent', 'EventCode', 'EventBaseCode', 'EventRootCode', 'QuadClass',
        'GoldsteinScale', 'NumMentions', 'NumSources', 'NumArticles', 'AvgTone',
        'Actor1Geo_Type', 'Actor1Geo_FullName', 'Actor1Geo_CountryCode',
        'Actor1Geo_ADM1Code', 'Actor1Geo_Lat', 'Actor1Geo_Long', 'Actor1Geo_FeatureID',
        'Actor2Geo_Type', 'Actor2Geo_FullName', 'Actor2Geo_CountryCode',
        'Actor2Geo_ADM1Code', 'Actor2Geo_Lat', 'Actor2Geo_Long', 'Actor2Geo_FeatureID',
        'ActionGeo_Type', 'ActionGeo_FullName', 'ActionGeo_CountryCode',
        'ActionGeo_ADM1Code', 'ActionGeo_Lat', 'ActionGeo_Long', 'ActionGeo_FeatureID',
        'DATEADDED', 'SOURCEURL'
    ]
    
    def __init__(self, db_config: Optional[Dict] = None):
        """Initialize ingestion pipeline.
        
        Args:
            db_config: PostgreSQL connection config (defaults to DATABASE_CONFIG)
        """
        self.db_config = db_config or DATABASE_CONFIG
        self.cameo_mapper = CAMEOMapper()
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'GDELT-Event-Ingestion/1.0'})
        
    def get_event_file_url(self, date: datetime) -> str:
        """Construct GDELT Event DB CSV URL for a given date.
        
        Args:
            date: Date to download events for
            
        Returns:
            Full URL to CSV.zip file
        """
        date_str = date.strftime('%Y%m%d')
        filename = f"{date_str}.export.CSV.zip"
        return urljoin(GDELT_CONFIG['base_url'], filename)
    
    def download_csv(self, url: str, retries: int = 3) -> Optional[pd.DataFrame]:
        """Download and parse GDELT CSV with retry logic.
        
        Args:
            url: Full URL to CSV.zip file
            retries: Number of retry attempts
            
        Returns:
            DataFrame with GDELT events, or None if download fails
        """
        for attempt in range(retries):
            try:
                logger.info(f"Downloading {url} (attempt {attempt+1}/{retries})")
                
                response = self.session.get(
                    url,
                    timeout=GDELT_CONFIG['timeout'],
                    stream=True
                )
                response.raise_for_status()
                
                # GDELT CSVs are tab-delimited, no headers
                df = pd.read_csv(
                    response.raw,
                    sep='\t',
                    header=None,
                    names=self.GDELT_COLUMNS,
                    compression='zip',
                    low_memory=False,
                    dtype={
                        'GLOBALEVENTID': 'Int64',
                        'SQLDATE': 'Int64',
                        'MonthYear': 'Int64',
                        'Year': 'Int64',
                        'QuadClass': 'Int64',
                        'NumMentions': 'Int64',
                        'NumSources': 'Int64',
                        'NumArticles': 'Int64'
                    }
                )
                
                logger.info(f"Downloaded {len(df):,} events from {url}")
                return df
                
            except requests.exceptions.RequestException as e:
                logger.warning(f"Download failed (attempt {attempt+1}): {e}")
                if attempt < retries - 1:
                    time.sleep(GDELT_CONFIG['retry_delay'])
                    
            except Exception as e:
                logger.error(f"Parsing failed: {e}")
                return None
                
        logger.error(f"Failed to download {url} after {retries} attempts")
        return None
    
    def preprocess_events(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and categorize events before insertion.
        
        Args:
            df: Raw GDELT DataFrame
            
        Returns:
            Processed DataFrame with socioeconomic categorization
        """
        # Convert SQLDATE to proper date format
        df['event_date'] = pd.to_datetime(df['SQLDATE'].astype(str), format='%Y%m%d')
        
        # Apply CAMEO categorization
        categorization = df['EventCode'].apply(
            lambda code: self.cameo_mapper.categorize_event(code)
        )
        df['socioeconomic_domain'] = categorization.apply(lambda x: x['domain'])
        df['socioeconomic_category'] = categorization.apply(lambda x: x['category'])
        df['category_confidence'] = categorization.apply(lambda x: x['confidence'])
        
        # Add ingestion metadata
        df['ingestion_timestamp'] = datetime.now()
        df['ingestion_batch_id'] = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        return df
    
    def insert_batch(self, conn, cursor, batch: pd.DataFrame) -> Tuple[int, int]:
        """Insert batch of events into PostgreSQL.
        
        Args:
            conn: psycopg2 connection
            cursor: psycopg2 cursor
            batch: DataFrame chunk to insert
            
        Returns:
            (inserted_count, error_count)
        """
        insert_query = sql.SQL("""
            INSERT INTO gdelt_events (
                event_id, event_date, month_year, year, fraction_date,
                actor1_code, actor1_name, actor1_country_code, actor1_known_group_code,
                actor1_ethnic_code, actor1_religion1_code, actor1_religion2_code,
                actor1_type1_code, actor1_type2_code, actor1_type3_code,
                actor2_code, actor2_name, actor2_country_code, actor2_known_group_code,
                actor2_ethnic_code, actor2_religion1_code, actor2_religion2_code,
                actor2_type1_code, actor2_type2_code, actor2_type3_code,
                is_root_event, event_code, event_base_code, event_root_code, quad_class,
                goldstein_scale, num_mentions, num_sources, num_articles, avg_tone,
                actor1_geo_type, actor1_geo_fullname, actor1_geo_country_code,
                actor1_geo_adm1_code, actor1_geo_lat, actor1_geo_long, actor1_geo_feature_id,
                actor2_geo_type, actor2_geo_fullname, actor2_geo_country_code,
                actor2_geo_adm1_code, actor2_geo_lat, actor2_geo_long, actor2_geo_feature_id,
                action_geo_type, action_geo_fullname, action_geo_country_code,
                action_geo_adm1_code, action_geo_lat, action_geo_long, action_geo_feature_id,
                date_added, source_url,
                socioeconomic_domain, socioeconomic_category, category_confidence,
                ingestion_timestamp, ingestion_batch_id
            ) VALUES (
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s,
                %s, %s,
                %s, %s, %s,
                %s, %s
            )
            ON CONFLICT (event_id) DO NOTHING
        """)
        
        # Prepare data tuples
        data = []
        for _, row in batch.iterrows():
            data.append((
                row['GLOBALEVENTID'], row['event_date'], row['MonthYear'], row['Year'], row['FractionDate'],
                row['Actor1Code'], row['Actor1Name'], row['Actor1CountryCode'], row['Actor1KnownGroupCode'],
                row['Actor1EthnicCode'], row['Actor1Religion1Code'], row['Actor1Religion2Code'],
                row['Actor1Type1Code'], row['Actor1Type2Code'], row['Actor1Type3Code'],
                row['Actor2Code'], row['Actor2Name'], row['Actor2CountryCode'], row['Actor2KnownGroupCode'],
                row['Actor2EthnicCode'], row['Actor2Religion1Code'], row['Actor2Religion2Code'],
                row['Actor2Type1Code'], row['Actor2Type2Code'], row['Actor2Type3Code'],
                row['IsRootEvent'], row['EventCode'], row['EventBaseCode'], row['EventRootCode'], row['QuadClass'],
                row['GoldsteinScale'], row['NumMentions'], row['NumSources'], row['NumArticles'], row['AvgTone'],
                row['Actor1Geo_Type'], row['Actor1Geo_FullName'], row['Actor1Geo_CountryCode'],
                row['Actor1Geo_ADM1Code'], row['Actor1Geo_Lat'], row['Actor1Geo_Long'], row['Actor1Geo_FeatureID'],
                row['Actor2Geo_Type'], row['Actor2Geo_FullName'], row['Actor2Geo_CountryCode'],
                row['Actor2Geo_ADM1Code'], row['Actor2Geo_Lat'], row['Actor2Geo_Long'], row['Actor2Geo_FeatureID'],
                row['ActionGeo_Type'], row['ActionGeo_FullName'], row['ActionGeo_CountryCode'],
                row['ActionGeo_ADM1Code'], row['ActionGeo_Lat'], row['ActionGeo_Long'], row['ActionGeo_FeatureID'],
                row['DATEADDED'], row['SOURCEURL'],
                row['socioeconomic_domain'], row['socioeconomic_category'], row['category_confidence'],
                row['ingestion_timestamp'], row['ingestion_batch_id']
            ))
        
        try:
            execute_batch(cursor, insert_query, data, page_size=INGESTION_CONFIG['batch_size'])
            conn.commit()
            return len(data), 0
        except Exception as e:
            conn.rollback()
            logger.error(f"Batch insertion failed: {e}")
            return 0, len(data)
    
    def ingest_date(self, date: datetime) -> Dict:
        """Download and ingest all events for a single date.
        
        Args:
            date: Date to ingest
            
        Returns:
            Statistics: {'date', 'downloaded', 'inserted', 'errors', 'duration_sec'}
        """
        start_time = time.time()
        url = self.get_event_file_url(date)
        
        # Download CSV
        df = self.download_csv(url)
        if df is None:
            return {
                'date': date.strftime('%Y-%m-%d'),
                'downloaded': 0,
                'inserted': 0,
                'errors': 0,
                'duration_sec': time.time() - start_time
            }
        
        # Preprocess
        df = self.preprocess_events(df)
        
        # Insert in batches
        conn = psycopg2.connect(**self.db_config)
        cursor = conn.cursor()
        
        total_inserted = 0
        total_errors = 0
        
        for i in range(0, len(df), INGESTION_CONFIG['chunk_size']):
            batch = df.iloc[i:i + INGESTION_CONFIG['chunk_size']]
            inserted, errors = self.insert_batch(conn, cursor, batch)
            total_inserted += inserted
            total_errors += errors
            
            logger.info(f"Batch {i//INGESTION_CONFIG['chunk_size']+1}: {inserted:,} inserted, {errors:,} errors")
        
        cursor.close()
        conn.close()
        
        duration = time.time() - start_time
        logger.info(f"Ingestion complete: {total_inserted:,} events in {duration:.1f}s")
        
        return {
            'date': date.strftime('%Y-%m-%d'),
            'downloaded': len(df),
            'inserted': total_inserted,
            'errors': total_errors,
            'duration_sec': duration
        }
    
    def ingest_date_range(self, start_date: datetime, end_date: datetime) -> List[Dict]:
        """Ingest events for a date range.
        
        Args:
            start_date: First date to ingest (inclusive)
            end_date: Last date to ingest (inclusive)
            
        Returns:
            List of statistics dicts for each date
        """
        results = []
        current_date = start_date
        
        while current_date <= end_date:
            logger.info(f"Ingesting {current_date.strftime('%Y-%m-%d')}")
            result = self.ingest_date(current_date)
            results.append(result)
            current_date += timedelta(days=1)
        
        # Summary
        total_downloaded = sum(r['downloaded'] for r in results)
        total_inserted = sum(r['inserted'] for r in results)
        total_errors = sum(r['errors'] for r in results)
        total_duration = sum(r['duration_sec'] for r in results)
        
        logger.info(f"""
        Ingestion Summary:
        - Dates: {len(results)}
        - Downloaded: {total_downloaded:,}
        - Inserted: {total_inserted:,}
        - Errors: {total_errors:,}
        - Duration: {total_duration:.1f}s
        """)
        
        return results


def main():
    """Example usage: ingest last 7 days of events."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    ingestion = GDELTEventIngestion()
    
    # Ingest last 7 days
    end_date = datetime.now() - timedelta(days=1)  # Yesterday (GDELT has 15min lag)
    start_date = end_date - timedelta(days=6)
    
    results = ingestion.ingest_date_range(start_date, end_date)
    
    print("\n=== Ingestion Complete ===")
    for result in results:
        print(f"{result['date']}: {result['inserted']:,} events in {result['duration_sec']:.1f}s")


if __name__ == '__main__':
    main()
