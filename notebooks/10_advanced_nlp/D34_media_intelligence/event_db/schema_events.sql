-- GDELT Event Database Schema
-- PostgreSQL 15+
-- 
-- This schema stores GDELT 2.0 Event Database records with 58 columns
-- plus additional fields for socioeconomic categorization.

CREATE TABLE IF NOT EXISTS gdelt_events (
    -- Primary Key
    event_id BIGINT PRIMARY KEY,
    
    -- Temporal Information
    event_date DATE NOT NULL,
    month_year INTEGER,
    year INTEGER,
    fraction_date DECIMAL(10, 5),
    
    -- Actor 1 (Primary Actor)
    actor1_code VARCHAR(50),
    actor1_name TEXT,
    actor1_country_code CHAR(3),
    actor1_known_group_code VARCHAR(50),
    actor1_ethnic_code VARCHAR(50),
    actor1_religion1_code VARCHAR(50),
    actor1_religion2_code VARCHAR(50),
    actor1_type1_code VARCHAR(50),
    actor1_type2_code VARCHAR(50),
    actor1_type3_code VARCHAR(50),
    
    -- Actor 2 (Secondary Actor)
    actor2_code VARCHAR(50),
    actor2_name TEXT,
    actor2_country_code CHAR(3),
    actor2_known_group_code VARCHAR(50),
    actor2_ethnic_code VARCHAR(50),
    actor2_religion1_code VARCHAR(50),
    actor2_religion2_code VARCHAR(50),
    actor2_type1_code VARCHAR(50),
    actor2_type2_code VARCHAR(50),
    actor2_type3_code VARCHAR(50),
    
    -- Event Classification
    is_root_event BOOLEAN,
    event_code VARCHAR(10) NOT NULL,
    event_base_code VARCHAR(10),
    event_root_code VARCHAR(10),
    quad_class INTEGER,  -- 1=Verbal Coop, 2=Material Coop, 3=Verbal Conflict, 4=Material Conflict
    
    -- Event Attributes
    goldstein_scale DECIMAL(5, 2),  -- -10 (conflict) to +10 (cooperation)
    num_mentions INTEGER,           -- Number of source articles
    num_sources INTEGER,            -- Number of source documents
    num_articles INTEGER,           -- Number of articles
    avg_tone DECIMAL(6, 2),        -- Sentiment (-100 to +100)
    
    -- Actor 1 Geography
    actor1_geo_type INTEGER,
    actor1_geo_fullname TEXT,
    actor1_geo_country_code CHAR(3),
    actor1_geo_adm1_code VARCHAR(10),
    actor1_geo_lat DECIMAL(9, 6),
    actor1_geo_long DECIMAL(9, 6),
    actor1_geo_feature_id VARCHAR(20),
    
    -- Actor 2 Geography
    actor2_geo_type INTEGER,
    actor2_geo_fullname TEXT,
    actor2_geo_country_code CHAR(3),
    actor2_geo_adm1_code VARCHAR(10),
    actor2_geo_lat DECIMAL(9, 6),
    actor2_geo_long DECIMAL(9, 6),
    actor2_geo_feature_id VARCHAR(20),
    
    -- Action Geography (where event occurred)
    action_geo_type INTEGER,
    action_geo_fullname TEXT,
    action_geo_country_code CHAR(3),
    action_geo_adm1_code VARCHAR(10),
    action_geo_lat DECIMAL(9, 6),
    action_geo_long DECIMAL(9, 6),
    action_geo_feature_id VARCHAR(20),
    
    -- Source Information
    date_added TIMESTAMP,
    source_url TEXT,
    
    -- Socioeconomic Categorization (added by us)
    socioeconomic_domain VARCHAR(50),     -- 'labor', 'health', 'education', etc.
    socioeconomic_category VARCHAR(50),   -- 'labor_action', 'policy_announcement', etc.
    category_confidence DECIMAL(3, 2),    -- 0.00 to 1.00
    
    -- Metadata
    ingestion_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ingestion_batch_id VARCHAR(50),
    
    -- Indexes for common queries
    CONSTRAINT unique_event UNIQUE (event_id)
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_event_date ON gdelt_events(event_date);
CREATE INDEX IF NOT EXISTS idx_event_code ON gdelt_events(event_code);
CREATE INDEX IF NOT EXISTS idx_actor1_code ON gdelt_events(actor1_code);
CREATE INDEX IF NOT EXISTS idx_actor2_code ON gdelt_events(actor2_code);
CREATE INDEX IF NOT EXISTS idx_actor1_country ON gdelt_events(actor1_country_code);
CREATE INDEX IF NOT EXISTS idx_actor2_country ON gdelt_events(actor2_country_code);
CREATE INDEX IF NOT EXISTS idx_action_country ON gdelt_events(action_geo_country_code);
CREATE INDEX IF NOT EXISTS idx_quad_class ON gdelt_events(quad_class);
CREATE INDEX IF NOT EXISTS idx_socioeconomic_domain ON gdelt_events(socioeconomic_domain);
CREATE INDEX IF NOT EXISTS idx_socioeconomic_category ON gdelt_events(socioeconomic_category);

-- Composite indexes for common queries
CREATE INDEX IF NOT EXISTS idx_date_domain ON gdelt_events(event_date, socioeconomic_domain);
CREATE INDEX IF NOT EXISTS idx_date_actors ON gdelt_events(event_date, actor1_code, actor2_code);
CREATE INDEX IF NOT EXISTS idx_country_date ON gdelt_events(action_geo_country_code, event_date);

-- Geospatial index (for proximity queries)
CREATE INDEX IF NOT EXISTS idx_action_geo_lat_long ON gdelt_events(action_geo_lat, action_geo_long);

-- Summary statistics table (for dashboard performance)
CREATE TABLE IF NOT EXISTS event_statistics (
    stat_id SERIAL PRIMARY KEY,
    stat_date DATE NOT NULL,
    socioeconomic_domain VARCHAR(50),
    event_count INTEGER,
    avg_goldstein DECIMAL(5, 2),
    avg_tone DECIMAL(6, 2),
    top_countries JSONB,
    top_actors JSONB,
    computed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_stat UNIQUE (stat_date, socioeconomic_domain)
);

CREATE INDEX IF NOT EXISTS idx_stat_date ON event_statistics(stat_date);
CREATE INDEX IF NOT EXISTS idx_stat_domain ON event_statistics(socioeconomic_domain);

-- Actor relationships table (for network analysis caching)
CREATE TABLE IF NOT EXISTS actor_relationships (
    relationship_id SERIAL PRIMARY KEY,
    actor1 VARCHAR(50) NOT NULL,
    actor2 VARCHAR(50) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    interaction_count INTEGER,
    avg_goldstein DECIMAL(5, 2),
    avg_tone DECIMAL(6, 2),
    event_types JSONB,  -- Distribution of event codes
    computed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_relationship UNIQUE (actor1, actor2, start_date, end_date)
);

CREATE INDEX IF NOT EXISTS idx_actor_rel_actors ON actor_relationships(actor1, actor2);
CREATE INDEX IF NOT EXISTS idx_actor_rel_dates ON actor_relationships(start_date, end_date);

-- Comments for documentation
COMMENT ON TABLE gdelt_events IS 'GDELT 2.0 Event Database records with socioeconomic categorization';
COMMENT ON COLUMN gdelt_events.event_id IS 'Unique identifier for the event (GLOBALEVENTID)';
COMMENT ON COLUMN gdelt_events.goldstein_scale IS 'Conflict/cooperation intensity: -10 (extreme conflict) to +10 (extreme cooperation)';
COMMENT ON COLUMN gdelt_events.quad_class IS 'Event quadrant: 1=Verbal Cooperation, 2=Material Cooperation, 3=Verbal Conflict, 4=Material Conflict';
COMMENT ON COLUMN gdelt_events.socioeconomic_domain IS 'High-level domain: labor_and_employment, health_and_social_policy, etc.';
COMMENT ON COLUMN gdelt_events.socioeconomic_category IS 'Specific category: labor_action, policy_announcement, etc.';
