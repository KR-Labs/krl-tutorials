# Technical Specifications: Media Intelligence Platform Extensions

**Project:** Socioeconomic Media Intelligence Platform  
**Current State:** Production Doc API Client (v2.0)  
**Target State:** Multi-Source Intelligence Platform with Event & Content Analytics  
**Timeline:** 4-6 weeks (80-120 hours)  
**Author:** KR-Labs

---

## 📋 Table of Contents

1. [Module 1: Event Database Analytics](#module-1-event-database-analytics)
2. [Module 2: Deep Content NLP](#module-2-deep-content-nlp)
3. [Integration Architecture](#integration-architecture)
4. [Infrastructure Requirements](#infrastructure-requirements)
5. [Development Roadmap](#development-roadmap)

---

## Module 1: Event Database Analytics

**Purpose:** Structured event tracking with actor networks and CAMEO coding  
**Effort:** 40-60 hours  
**Dependencies:** GDELT Event Database (CSV exports or BigQuery)  
**Primary Value:** "Who did what to whom, where, and when?"

### 1.1 Core Capabilities

#### **A. Event Ingestion Pipeline**

**Objective:** Automated daily download and parsing of GDELT Event Database

**Technical Implementation:**

```python
class GDELTEventIngestion:
    """
    Automated ingestion pipeline for GDELT Event Database.
    
    Features:
    - Daily/hourly batch downloads from GDELT CSV exports
    - Incremental loading with deduplication
    - CAMEO event type parsing and categorization
    - Actor code extraction and normalization
    - Geographic coordinate extraction
    - Goldstein scale scoring
    """
    
    def __init__(self, storage_backend='postgresql'):
        self.storage = storage_backend
        self.base_url = "http://data.gdeltproject.org/gdeltv2/"
    
    def fetch_event_batch(self, date: str, hour: Optional[str] = None):
        """
        Download GDELT event batch for specific date/hour.
        
        GDELT publishes events every 15 minutes in format:
        YYYYMMDDHHMMSS.export.CSV.zip
        
        Args:
            date: YYYYMMDD format
            hour: Optional HH format for hourly granularity
        """
        pass
    
    def parse_event_record(self, raw_row: List[str]) -> Dict:
        """
        Parse 58-column GDELT event record into structured format.
        
        Key fields:
        - GLOBALEVENTID: Unique event identifier
        - SQLDATE: Event date
        - Actor1Code, Actor2Code: Primary actors (e.g., 'USA', 'CHN')
        - EventCode: CAMEO event type (e.g., '14' for protest)
        - GoldsteinScale: Conflict(-10) to cooperation(+10)
        - NumMentions: Source article count
        - AvgTone: Sentiment (-100 to +100)
        - ActionGeo_Lat/Long: Event location
        - SOURCEURL: Primary source article
        """
        pass
    
    def filter_socioeconomic_events(self, events: pd.DataFrame) -> pd.DataFrame:
        """
        Filter for socioeconomic event types:
        - Protests (CAMEO 14*)
        - Labor actions (CAMEO 14*, 19*)
        - Policy announcements (CAMEO 01*, 03*)
        - Economic activity (CAMEO 06*, 07*)
        - Social unrest (CAMEO 14*, 18*, 19*)
        """
        pass
```

**Data Schema:**

```sql
CREATE TABLE gdelt_events (
    event_id BIGINT PRIMARY KEY,
    event_date DATE NOT NULL,
    event_timestamp TIMESTAMP,
    
    -- Actors
    actor1_code VARCHAR(50),
    actor1_name VARCHAR(255),
    actor1_country CHAR(3),
    actor2_code VARCHAR(50),
    actor2_name VARCHAR(255),
    actor2_country CHAR(3),
    
    -- Event Classification
    event_code VARCHAR(10),
    event_base_code VARCHAR(10),
    event_root_code VARCHAR(10),
    quad_class INT,  -- 1=Verbal Cooperation, 2=Material Cooperation, 3=Verbal Conflict, 4=Material Conflict
    
    -- Event Attributes
    goldstein_scale DECIMAL(5,2),  -- Conflict/cooperation intensity
    num_mentions INT,              -- Number of source articles
    num_sources INT,
    num_articles INT,
    avg_tone DECIMAL(6,2),         -- Sentiment score
    
    -- Geography
    action_geo_type INT,
    action_geo_country CHAR(3),
    action_geo_lat DECIMAL(9,6),
    action_geo_long DECIMAL(9,6),
    
    -- Source
    source_url TEXT,
    date_added TIMESTAMP,
    
    -- Domain Classification (added by us)
    socioeconomic_category VARCHAR(50),  -- 'labor', 'health', 'education', etc.
    socioeconomic_subcategory VARCHAR(50),
    
    -- Indexes
    INDEX idx_date (event_date),
    INDEX idx_actors (actor1_code, actor2_code),
    INDEX idx_event_code (event_code),
    INDEX idx_location (action_geo_country, action_geo_lat, action_geo_long),
    INDEX idx_category (socioeconomic_category)
);
```

#### **B. CAMEO Event Categorization**

**Objective:** Map CAMEO codes to socioeconomic domains

```python
SOCIOECONOMIC_EVENT_MAPPING = {
    "labor_action": {
        "cameo_codes": ["14", "141", "142", "143", "144", "145"],
        "description": "Protests, demonstrations, strikes",
        "keywords": ["strike", "protest", "demonstration", "picket", "walkout"]
    },
    "policy_announcement": {
        "cameo_codes": ["01", "010", "011", "012", "013"],
        "description": "Government policy statements",
        "keywords": ["policy", "legislation", "regulation", "law", "bill"]
    },
    "economic_cooperation": {
        "cameo_codes": ["06", "061", "062", "063"],
        "description": "Economic aid, trade agreements",
        "keywords": ["trade", "investment", "aid", "loan", "grant"]
    },
    "social_conflict": {
        "cameo_codes": ["18", "181", "182", "183", "19", "190"],
        "description": "Violence, fighting, assault",
        "keywords": ["violence", "clash", "fight", "attack", "riot"]
    },
    "diplomatic_cooperation": {
        "cameo_codes": ["03", "04", "05"],
        "description": "Intent to cooperate, consultation",
        "keywords": ["cooperation", "agreement", "partnership", "alliance"]
    }
}

def categorize_event(event_code: str, actor_info: Dict, article_text: str) -> str:
    """
    Classify event into socioeconomic domain using:
    1. CAMEO code lookup
    2. Actor type analysis (government, labor, NGO, etc.)
    3. Keyword matching in source article
    """
    pass
```

#### **C. Actor Network Analysis**

**Objective:** Map relationships between actors over time

```python
class ActorNetworkAnalyzer:
    """
    Build and analyze actor interaction networks.
    
    Use Cases:
    - Identify key players in policy domains
    - Track coalition formation
    - Detect conflict escalation patterns
    - Monitor diplomatic relationships
    """
    
    def build_network(
        self,
        start_date: str,
        end_date: str,
        actor_filter: Optional[List[str]] = None,
        event_types: Optional[List[str]] = None,
        min_interactions: int = 5
    ) -> nx.Graph:
        """
        Construct network graph where:
        - Nodes = Actors (countries, orgs, groups)
        - Edges = Interactions (weighted by frequency)
        - Edge attributes = event types, sentiment, Goldstein scores
        
        Returns NetworkX graph for visualization and analysis
        """
        pass
    
    def identify_communities(self, network: nx.Graph) -> Dict:
        """Detect actor coalitions using community detection"""
        pass
    
    def calculate_influence_scores(self, network: nx.Graph) -> pd.DataFrame:
        """Calculate centrality metrics (betweenness, eigenvector, PageRank)"""
        pass
    
    def track_relationship_evolution(
        self,
        actor1: str,
        actor2: str,
        start_date: str,
        end_date: str
    ) -> pd.DataFrame:
        """
        Track how two actors' relationship evolves over time.
        
        Returns time series of:
        - Interaction frequency
        - Average Goldstein score (conflict/cooperation)
        - Event type distribution
        - Sentiment trends
        """
        pass
```

#### **D. Geospatial Event Analysis**

**Objective:** Map events to geographic regions for spatial analysis

```python
class GeoEventAnalyzer:
    """
    Geographic analysis of socioeconomic events.
    
    Capabilities:
    - Heatmap generation for event types
    - Cross-border event propagation tracking
    - Regional clustering and hotspot detection
    - Country-level event aggregation
    """
    
    def create_event_heatmap(
        self,
        event_type: str,
        date_range: Tuple[str, str],
        resolution: str = 'country'  # 'country', 'region', 'city'
    ) -> gpd.GeoDataFrame:
        """Generate choropleth data for mapping"""
        pass
    
    def detect_event_clusters(
        self,
        events: pd.DataFrame,
        radius_km: float = 100
    ) -> List[Dict]:
        """
        Use DBSCAN to identify geographic event clusters.
        
        Useful for:
        - Identifying protest hotspots
        - Tracking social unrest spread
        - Detecting policy implementation patterns
        """
        pass
    
    def analyze_cross_border_events(
        self,
        country1: str,
        country2: str,
        date_range: Tuple[str, str]
    ) -> Dict:
        """
        Analyze events involving multiple countries.
        
        Returns:
        - Border region event counts
        - Bilateral interaction patterns
        - Cross-border cooperation vs. conflict ratios
        """
        pass
```

### 1.2 API Endpoints

Expose event data via REST API:

```python
# FastAPI endpoint examples

@app.get("/api/v1/events/search")
async def search_events(
    actor: Optional[str] = None,
    event_type: Optional[str] = None,
    country: Optional[str] = None,
    start_date: str = Query(...),
    end_date: str = Query(...),
    limit: int = 100
):
    """
    Search events with flexible filters.
    
    Example:
    GET /api/v1/events/search?actor=USA&event_type=14&start_date=2025-01-01&end_date=2025-01-31
    """
    pass

@app.get("/api/v1/events/actor-network")
async def get_actor_network(
    actors: List[str] = Query(...),
    start_date: str = Query(...),
    end_date: str = Query(...),
    min_interactions: int = 5
):
    """
    Generate actor network graph data.
    
    Returns JSON with nodes, edges, and network metrics.
    """
    pass

@app.get("/api/v1/events/timeseries")
async def get_event_timeseries(
    event_type: str = Query(...),
    country: Optional[str] = None,
    start_date: str = Query(...),
    end_date: str = Query(...),
    granularity: str = 'daily'  # 'daily', 'weekly', 'monthly'
):
    """
    Get time series of event counts and sentiment.
    
    Returns DataFrame-compatible JSON for plotting.
    """
    pass

@app.get("/api/v1/events/heatmap")
async def get_event_heatmap(
    event_type: str = Query(...),
    date: str = Query(...),
    resolution: str = 'country'
):
    """
    Get geographic heatmap data for specific date.
    
    Returns GeoJSON for mapping libraries.
    """
    pass
```

### 1.3 Deliverables

**Week 1-2 (20-30 hours):**
- ✅ Event ingestion pipeline (CSV download + parsing)
- ✅ Database schema and ORM models
- ✅ CAMEO to socioeconomic domain mapping
- ✅ Basic event search API

**Week 2-3 (20-30 hours):**
- ✅ Actor network analysis module
- ✅ Geospatial event clustering
- ✅ Time series aggregation
- ✅ Dashboard visualizations (Plotly/Folium)

**Validation Metrics:**
- Successfully ingest 50,000+ events per day
- <5 second response time for event searches
- <15 second response time for network graph generation
- >95% CAMEO code parsing accuracy

---

## Module 2: Deep Content NLP

**Purpose:** Full-text article analysis with transformer-based NLP  
**Effort:** 40-80 hours  
**Dependencies:** crawl4ai, Hugging Face Transformers, OpenAI API (optional)  
**Primary Value:** "What is actually being said in these articles?"

### 2.1 Core Capabilities

#### **A. Production Web Scraping Pipeline**

**Objective:** Reliable, scalable article content extraction

```python
class ProductionArticleScraper:
    """
    Production-grade web scraping for news articles.
    
    Features:
    - Async crawling with crawl4ai
    - Retry logic with exponential backoff
    - Anti-bot detection handling
    - Content extraction and validation
    - Deduplication (exact + fuzzy)
    """
    
    def __init__(
        self,
        max_concurrent: int = 10,
        timeout: int = 30,
        user_agent_rotation: bool = True,
        proxy_pool: Optional[List[str]] = None
    ):
        self.max_concurrent = max_concurrent
        self.timeout = timeout
        self.user_agents = self._load_user_agents() if user_agent_rotation else None
        self.proxy_pool = proxy_pool
    
    async def scrape_article(self, url: str, max_retries: int = 3) -> Dict:
        """
        Extract article content from URL.
        
        Returns:
        {
            'url': str,
            'title': str,
            'content': str,  # Main article text
            'author': str,
            'publish_date': datetime,
            'lang': str,
            'word_count': int,
            'extraction_quality': float,  # 0-1 confidence score
            'scrape_timestamp': datetime
        }
        """
        pass
    
    async def batch_scrape(
        self,
        urls: List[str],
        priority_queue: bool = True
    ) -> List[Dict]:
        """
        Scrape multiple URLs with concurrent workers.
        
        Implements:
        - Priority queue (scrape high-value sources first)
        - Rate limiting per domain
        - Failed URL retry queue
        - Progress tracking
        """
        pass
    
    def validate_content(self, article: Dict) -> bool:
        """
        Validate extracted content quality.
        
        Checks:
        - Minimum word count (>100 words)
        - Content-to-boilerplate ratio
        - Language detection matches expected
        - No common error patterns (404 text, paywalls, etc.)
        """
        pass
```

**Content Storage:**

```sql
CREATE TABLE article_content (
    article_id SERIAL PRIMARY KEY,
    url TEXT UNIQUE NOT NULL,
    url_hash VARCHAR(64) UNIQUE,  -- SHA256 for deduplication
    
    -- Metadata
    title TEXT,
    author TEXT,
    publish_date TIMESTAMP,
    source_domain VARCHAR(255),
    language CHAR(2),
    
    -- Content
    full_text TEXT,
    word_count INT,
    char_count INT,
    
    -- Scraping Metadata
    scrape_timestamp TIMESTAMP,
    scrape_duration_ms INT,
    extraction_quality DECIMAL(3,2),
    scraper_version VARCHAR(20),
    
    -- Status
    status VARCHAR(20),  -- 'success', 'failed', 'paywall', 'timeout'
    error_message TEXT,
    
    -- Deduplication
    content_hash VARCHAR(64),  -- For fuzzy matching
    is_duplicate BOOLEAN DEFAULT FALSE,
    duplicate_of INT REFERENCES article_content(article_id),
    
    -- Indexes
    INDEX idx_url_hash (url_hash),
    INDEX idx_publish_date (publish_date),
    INDEX idx_domain (source_domain),
    INDEX idx_status (status),
    FULLTEXT INDEX ft_content (full_text)
);
```

#### **B. Advanced NLP Processing**

**Objective:** Extract structured insights from article text

```python
class DeepContentAnalyzer:
    """
    Transformer-based NLP for article analysis.
    
    Capabilities:
    - Extractive & abstractive summarization
    - Named entity recognition (persons, orgs, locations)
    - Stance detection (support/oppose on issues)
    - Claim extraction and fact-checking hooks
    - Topic modeling with coherence
    - Semantic similarity and clustering
    """
    
    def __init__(
        self,
        summarization_model: str = "facebook/bart-large-cnn",
        ner_model: str = "dslim/bert-base-NER",
        stance_model: str = "cardiffnlp/twitter-roberta-base-stance",
        use_gpu: bool = True
    ):
        self.summarizer = pipeline("summarization", model=summarization_model)
        self.ner = pipeline("ner", model=ner_model)
        self.stance_detector = pipeline("text-classification", model=stance_model)
    
    def generate_summary(
        self,
        text: str,
        max_length: int = 150,
        min_length: int = 50,
        style: str = 'abstractive'
    ) -> Dict:
        """
        Generate article summary.
        
        Returns:
        {
            'summary': str,
            'compression_ratio': float,
            'key_sentences': List[str],  # Extractive highlights
            'quality_score': float
        }
        """
        pass
    
    def extract_entities(self, text: str) -> Dict:
        """
        Extract and classify named entities.
        
        Returns:
        {
            'persons': List[str],
            'organizations': List[str],
            'locations': List[str],
            'dates': List[str],
            'money': List[str],
            'policy_mentions': List[str]  # Custom domain-specific
        }
        """
        pass
    
    def detect_stance(
        self,
        text: str,
        target_topic: str,
        target_entity: Optional[str] = None
    ) -> Dict:
        """
        Determine article stance on topic/entity.
        
        Example:
        detect_stance(
            text="Article content...",
            target_topic="universal healthcare",
            target_entity="Biden administration"
        )
        
        Returns:
        {
            'stance': str,  # 'support', 'oppose', 'neutral'
            'confidence': float,
            'evidence_sentences': List[str],
            'sentiment_score': float
        }
        """
        pass
    
    def extract_claims(self, text: str) -> List[Dict]:
        """
        Identify factual claims for potential fact-checking.
        
        Returns list of:
        {
            'claim_text': str,
            'claim_type': str,  # 'statistical', 'causal', 'policy', etc.
            'entity_mentions': List[str],
            'confidence': float,
            'fact_checkable': bool
        }
        """
        pass
    
    def analyze_framing(
        self,
        text: str,
        domain: str = 'socioeconomic'
    ) -> Dict:
        """
        Analyze how issue is framed.
        
        Detects:
        - Moral frames (care/harm, fairness, authority, etc.)
        - Economic frames (cost, efficiency, growth, etc.)
        - Political frames (conflict, attribution, mobilization, etc.)
        
        Returns frame distribution and evidence.
        """
        pass
```

#### **C. Content Enrichment Pipeline**

**Objective:** Combine scraped content with NLP insights

```python
class ContentEnrichmentPipeline:
    """
    End-to-end pipeline: URL → Scrape → NLP → Storage
    """
    
    def __init__(self, scraper, analyzer, storage):
        self.scraper = scraper
        self.analyzer = analyzer
        self.storage = storage
    
    async def enrich_article_batch(
        self,
        urls: List[str],
        enable_stance: bool = True,
        enable_claims: bool = False,  # Slower, optional
        target_topics: Optional[List[str]] = None
    ) -> List[Dict]:
        """
        Full enrichment pipeline:
        1. Scrape URLs
        2. Validate content
        3. Run NLP (summary, entities, stance)
        4. Store structured output
        
        Returns enriched article records.
        """
        pass
    
    def create_knowledge_graph(
        self,
        articles: List[Dict],
        min_entity_mentions: int = 3
    ) -> nx.Graph:
        """
        Build knowledge graph from article entities.
        
        Nodes: Persons, Organizations, Locations, Topics
        Edges: Co-mentions, relationships, interactions
        
        Use for:
        - Entity-centric search
        - Relationship discovery
        - Influence mapping
        """
        pass
```

**NLP Results Storage:**

```sql
CREATE TABLE article_nlp_analysis (
    analysis_id SERIAL PRIMARY KEY,
    article_id INT REFERENCES article_content(article_id),
    
    -- Summary
    summary_text TEXT,
    summary_compression DECIMAL(4,2),
    key_sentences JSONB,
    
    -- Entities
    persons JSONB,  -- ['name1', 'name2', ...]
    organizations JSONB,
    locations JSONB,
    dates JSONB,
    
    -- Stance & Framing
    primary_topic VARCHAR(255),
    stance VARCHAR(20),  -- 'support', 'oppose', 'neutral'
    stance_confidence DECIMAL(4,2),
    framing_analysis JSONB,  -- {frame_type: score}
    
    -- Claims
    extracted_claims JSONB,
    
    -- Semantic Features
    embedding VECTOR(768),  -- For semantic search (pgvector)
    
    -- Processing Metadata
    nlp_model_version VARCHAR(50),
    processing_timestamp TIMESTAMP,
    processing_duration_ms INT,
    
    -- Indexes
    INDEX idx_article (article_id),
    INDEX idx_topic (primary_topic),
    INDEX idx_stance (stance)
);

-- Enable pgvector for semantic search
CREATE INDEX article_embedding_idx ON article_nlp_analysis 
USING ivfflat (embedding vector_cosine_ops);
```

### 2.2 Integration with Existing Systems

**Link scraped content to GDELT metadata:**

```python
def link_gdelt_to_content(gdelt_article: Dict, scraped_content: Dict):
    """
    Connect GDELT Doc API metadata with scraped full-text.
    
    Enables:
    - Title-only baseline vs. full-text comparison
    - Sentiment validation (title vs. content)
    - Entity extraction from both sources
    - Cross-validation of claims
    """
    pass

def cross_validate_sentiment(
    gdelt_sentiment: float,
    content_sentiment: float,
    title: str,
    full_text: str
) -> Dict:
    """
    Compare title-level vs. content-level sentiment.
    
    Detects:
    - Clickbait (sentiment mismatch)
    - Nuanced reporting (title simplified, content balanced)
    - Consistent framing
    """
    pass
```

### 2.3 Deliverables

**Week 1-2 (20-40 hours):**
- ✅ Production scraping pipeline with crawl4ai
- ✅ Content extraction and validation
- ✅ Database schema for full-text storage
- ✅ Basic NLP: summarization + entity extraction

**Week 3-4 (20-40 hours):**
- ✅ Advanced NLP: stance detection + claim extraction
- ✅ Semantic search with vector embeddings
- ✅ Knowledge graph construction
- ✅ Integration with Doc API and Event DB

**Validation Metrics:**
- >90% successful content extraction rate
- <10 seconds per article for full NLP pipeline
- >85% entity extraction accuracy (human validation sample)
- >80% stance detection accuracy (validated subset)

---

## Integration Architecture

### 3.1 Data Flow

```
┌─────────────────────────────────────────────────────────────┐
│                      DATA SOURCES                            │
├────────────┬──────────────────┬───────────────────────┬──────┤
│ GDELT      │ GDELT Event DB   │ Web Scraping          │ User │
│ Doc API    │ (CSV/BigQuery)   │ (crawl4ai)            │ Input│
└──────┬─────┴────────┬─────────┴──────────┬────────────┴──────┘
       │              │                    │
       │              │                    │
       ▼              ▼                    ▼
┌─────────────────────────────────────────────────────────────┐
│                   INGESTION LAYER                           │
├─────────────┬──────────────────┬──────────────────────────┬─┤
│ Doc API     │ Event Ingestion  │ Content Scraper          │ │
│ Connector   │ Pipeline         │ + Validator              │ │
│ (existing)  │ (new)            │ (new)                    │ │
└──────┬──────┴────────┬─────────┴──────────┬───────────────┴─┘
       │               │                    │
       │               │                    │
       ▼               ▼                    ▼
┌─────────────────────────────────────────────────────────────┐
│                     DATA STORAGE                            │
├─────────────┬──────────────────┬───────────────────────────┤
│ PostgreSQL  │ PostgreSQL       │ PostgreSQL + Vector DB    │
│ (metadata)  │ (events)         │ (full-text + embeddings)  │
└──────┬──────┴────────┬─────────┴──────────┬────────────────┘
       │               │                    │
       │               │                    │
       ▼               ▼                    ▼
┌─────────────────────────────────────────────────────────────┐
│                   ANALYTICS LAYER                           │
├─────────────┬──────────────────┬───────────────────────────┤
│ Title       │ Actor Networks   │ Deep NLP                  │
│ Analytics   │ CAMEO Coding     │ (Summary, Entities,       │
│ (existing)  │ Geo Clustering   │  Stance, Claims)          │
│             │ (new)            │ (new)                     │
└──────┬──────┴────────┬─────────┴──────────┬────────────────┘
       │               │                    │
       └───────────────┴────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                      API LAYER                              │
├─────────────┬──────────────────┬───────────────────────────┤
│ REST API    │ GraphQL API      │ WebSocket (real-time)     │
│ (FastAPI)   │ (optional)       │ (optional)                │
└──────┬──────┴────────┬─────────┴──────────┬────────────────┘
       │               │                    │
       └───────────────┴────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                  PRESENTATION LAYER                         │
├─────────────┬──────────────────┬───────────────────────────┤
│ Jupyter     │ Streamlit        │ React Dashboard           │
│ Notebooks   │ Dashboard        │ (production)              │
│ (current)   │ (MVP)            │ (future)                  │
└─────────────┴──────────────────┴───────────────────────────┘
```

### 3.2 Unified Query Interface

```python
class UnifiedMediaIntelligence:
    """
    Single interface for all data sources.
    
    Combines:
    - Doc API (title-level, real-time)
    - Event DB (structured events, actors, CAMEO)
    - Content NLP (full-text, deep semantics)
    """
    
    def __init__(self):
        self.doc_api = GDELTConnector()
        self.event_db = GDELTEventIngestion()
        self.content_nlp = DeepContentAnalyzer()
    
    def comprehensive_search(
        self,
        query: str,
        start_date: str,
        end_date: str,
        include_events: bool = True,
        include_full_text: bool = True,
        stance_filter: Optional[str] = None
    ) -> Dict:
        """
        Search across all data sources.
        
        Returns:
        {
            'articles': [...],  # Doc API metadata
            'events': [...],    # Related GDELT events
            'content': [...],   # Full-text with NLP
            'summary': {...},   # Cross-source insights
            'actors': [...],    # Key actors mentioned
            'topics': [...],    # Topic distribution
            'sentiment': {...}, # Sentiment trends
            'geographic': {...} # Geographic patterns
        }
        """
        pass
    
    def entity_timeline(
        self,
        entity: str,
        entity_type: str,  # 'person', 'organization', 'topic'
        start_date: str,
        end_date: str
    ) -> pd.DataFrame:
        """
        Track entity across all data sources over time.
        
        Returns timeline with:
        - Mention frequency
        - Sentiment trends
        - Associated events
        - Stance patterns
        - Network connections
        """
        pass
    
    def compare_sources(
        self,
        topic: str,
        sources: List[str],
        date_range: Tuple[str, str]
    ) -> Dict:
        """
        Compare how different sources cover same topic.
        
        Analyzes:
        - Coverage volume
        - Framing differences
        - Stance distribution
        - Entity emphasis
        - Sentiment divergence
        """
        pass
```

---

## Infrastructure Requirements

### 4.1 Development Environment

**Python Dependencies:**
```txt
# Core
python>=3.10
pandas>=2.0
numpy>=1.24
sqlalchemy>=2.0
psycopg2-binary>=2.9

# Web Scraping
crawl4ai>=0.2
playwright>=1.40
beautifulsoup4>=4.12
newspaper3k>=0.2.8

# NLP
transformers>=4.35
torch>=2.1
spacy>=3.7
nltk>=3.8
sentence-transformers>=2.2
bertopic>=0.16

# Network Analysis
networkx>=3.2
python-louvain>=0.16

# Geospatial
geopandas>=0.14
folium>=0.15
shapely>=2.0

# API & Dashboard
fastapi>=0.104
uvicorn>=0.24
streamlit>=1.28
plotly>=5.17

# Database
pgvector>=0.2  # For semantic search
asyncpg>=0.29  # Async PostgreSQL

# Infrastructure
redis>=5.0
celery>=5.3  # Task queue
```

### 4.2 Infrastructure Stack

**Database:**
- PostgreSQL 15+ with pgvector extension
- 100GB+ storage for events + content
- Connection pooling (pgbouncer)

**Caching:**
- Redis 7+ for session caching
- Memcached for API response caching

**Task Queue:**
- Celery with Redis backend
- Separate queues for scraping vs. NLP

**Compute:**
- 8+ CPU cores for parallel processing
- 16GB+ RAM for NLP models
- Optional GPU for faster inference (T4/V100)

**Estimated Costs (AWS/GCP):**
- Database: $50-100/month (db.t3.large)
- Compute: $100-200/month (c5.2xlarge or GPU instance)
- Storage: $10-30/month
- Data transfer: $20-50/month
- **Total: $200-400/month**

---

## Development Roadmap

### Week 1: Foundation + Event DB Ingestion

**Days 1-2: Setup**
- [ ] Set up development environment
- [ ] Initialize database schema (events + content)
- [ ] Configure GDELT Event DB access
- [ ] Set up logging and monitoring

**Days 3-5: Event Ingestion**
- [ ] Build CSV download pipeline
- [ ] Implement event parser (58 columns)
- [ ] Create CAMEO to socioeconomic mapping
- [ ] Write database insertion logic
- [ ] Add incremental loading + deduplication

**Days 6-7: Validation**
- [ ] Ingest 1 week of events (~500K records)
- [ ] Validate CAMEO categorization
- [ ] Test query performance
- [ ] Document data quality metrics

**Deliverables:**
- Automated daily event ingestion
- Database with 500K+ events
- CAMEO categorization working
- Query API (basic endpoints)

---

### Week 2: Actor Networks + Geospatial

**Days 8-10: Network Analysis**
- [ ] Build actor network construction
- [ ] Implement community detection
- [ ] Calculate influence metrics
- [ ] Create network visualization (NetworkX + Plotly)

**Days 11-12: Geospatial**
- [ ] Build geographic clustering (DBSCAN)
- [ ] Create event heatmaps (Folium)
- [ ] Implement country-level aggregation
- [ ] Add cross-border event analysis

**Days 13-14: API + Dashboard**
- [ ] Expose network API endpoints
- [ ] Expose geospatial API endpoints
- [ ] Build Streamlit dashboard prototype
- [ ] User testing and refinement

**Deliverables:**
- Actor network module working
- Geospatial event clustering
- Interactive Streamlit dashboard
- 5+ API endpoints for queries

---

### Week 3: Content Scraping + Basic NLP

**Days 15-17: Scraping Pipeline**
- [ ] Set up crawl4ai with Playwright
- [ ] Implement async batch scraping
- [ ] Add retry logic and error handling
- [ ] Create content validation logic
- [ ] Build deduplication (exact + fuzzy)

**Days 18-20: Basic NLP**
- [ ] Implement summarization (BART)
- [ ] Add entity extraction (spaCy/BERT)
- [ ] Create sentiment analysis (full-text)
- [ ] Build comparison (title vs. content sentiment)

**Days 21: Integration**
- [ ] Link scraped content to GDELT metadata
- [ ] Store NLP results in database
- [ ] Test end-to-end pipeline
- [ ] Performance optimization

**Deliverables:**
- Production scraping pipeline
- 1000+ scraped articles
- Basic NLP (summary, entities, sentiment)
- Database integration complete

---

### Week 4: Advanced NLP + Knowledge Graph

**Days 22-24: Advanced NLP**
- [ ] Implement stance detection
- [ ] Add claim extraction
- [ ] Build framing analysis
- [ ] Create semantic embeddings (sentence-transformers)

**Days 25-26: Knowledge Graph**
- [ ] Build entity co-occurrence graph
- [ ] Implement relationship extraction
- [ ] Add graph visualization
- [ ] Create entity-centric search

**Days 27-28: Final Integration**
- [ ] Unified query interface
- [ ] Comprehensive dashboard
- [ ] Performance testing at scale
- [ ] Documentation and examples

**Deliverables:**
- Full NLP pipeline operational
- Knowledge graph built and queryable
- Complete integrated system
- Polished demo and documentation

---

## Success Metrics

### Technical Metrics

**Data Quality:**
- [ ] >95% event parsing accuracy
- [ ] >90% content extraction success rate
- [ ] >85% entity extraction accuracy (sample validation)
- [ ] <5% duplicate rate after deduplication

**Performance:**
- [ ] <5s response time for event queries
- [ ] <15s for network graph generation
- [ ] <10s per article for full NLP pipeline
- [ ] >100 concurrent API requests supported

**Scale:**
- [ ] 50K+ events ingested per day
- [ ] 500+ articles scraped per day
- [ ] 1M+ events in database
- [ ] 10K+ full-text articles stored

### Business Metrics

**Portfolio Value:**
- [ ] Professional demo ready for client presentations
- [ ] Documentation suitable for hiring managers
- [ ] Clear differentiation vs. existing tools
- [ ] Demonstrable socioeconomic domain expertise

**Extensibility:**
- [ ] Modular architecture for easy additions
- [ ] Clear API contracts for integration
- [ ] Comprehensive tests (>80% coverage)
- [ ] Production-ready code quality

---

## Risk Mitigation

### Technical Risks

**Risk:** Scraping failures due to anti-bot measures  
**Mitigation:** Implement robust retry logic, proxy rotation, rate limiting per domain

**Risk:** NLP model inference too slow  
**Mitigation:** Use model quantization, batch processing, optional GPU acceleration

**Risk:** Database performance degrades at scale  
**Mitigation:** Proper indexing, query optimization, connection pooling, read replicas

**Risk:** Data quality issues (malformed events, extraction errors)  
**Mitigation:** Comprehensive validation, quality score tracking, manual review samples

### Business Risks

**Risk:** Insufficient differentiation from existing tools  
**Mitigation:** Focus on socioeconomic domain expertise, custom analytics, transparency

**Risk:** Unclear market demand  
**Mitigation:** Build MVP first, validate with potential users, pivot if needed

**Risk:** Ongoing infrastructure costs  
**Mitigation:** Start with minimal infrastructure, scale based on actual usage

---

## Next Steps

**Immediate Actions:**

1. **Approve technical specifications** - Review and confirm approach
2. **Set up development environment** - Clone repos, install dependencies
3. **Initialize database schema** - Create tables, indexes, relationships
4. **Begin Week 1 implementation** - Event DB ingestion pipeline

**Questions to Resolve:**

- [ ] BigQuery access vs. CSV-only? (Cost vs. capabilities)
- [ ] GPU access for NLP? (Speed vs. cost)
- [ ] Hosting preference? (AWS vs. GCP vs. local)
- [ ] OpenAI API budget? (For optional advanced NLP)

**Ready to start building?** Confirm approach and we'll begin Week 1 implementation.

---

**Document Version:** 1.0  
**Last Updated:** November 2025  
**Author:** KR-Labs  
**Status:** Awaiting Approval
