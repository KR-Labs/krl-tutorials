# Event Database Module - Implementation Plan

**Path:** Focused validation (40-60 hours over 2-3 weeks)  
**Goal:** Validate demand for actor network and CAMEO event analysis  
**Budget:** $50-100/month infrastructure  
**Risk:** Low - manageable scope, clear deliverables

---

## 🎯 Success Criteria

**Technical:**
- [ ] Ingest 500K+ GDELT events (1+ week of data)
- [ ] Parse all 58 GDELT Event DB columns correctly
- [ ] Map CAMEO codes to socioeconomic domains (>90% accuracy)
- [ ] Generate actor network graphs (<15 seconds)
- [ ] Create geospatial event heatmaps
- [ ] Query API responding in <5 seconds

**Business:**
- [ ] Demo to 3+ potential users/clients
- [ ] Gather feedback on value proposition
- [ ] Validate 2-3 specific use cases
- [ ] Identify revenue/engagement model

---

## 📅 Week 1: Foundation + Data Ingestion

### **Day 1-2: Environment Setup** (8 hours)

**Objectives:**
- Set up PostgreSQL database with proper schema
- Configure development environment
- Test GDELT Event DB access
- Create logging and monitoring

**Tasks:**

1. **Install PostgreSQL**
   ```bash
   # macOS
   brew install postgresql@15
   brew services start postgresql@15
   
   # Create database
   createdb gdelt_events
   ```

2. **Install Python dependencies**
   ```bash
   pip install psycopg2-binary sqlalchemy pandas requests gzip
   ```

3. **Create database schema** (see `schema_events.sql` below)

4. **Test GDELT Event DB access**
   ```python
   # Test CSV download
   import requests
   from datetime import datetime, timedelta
   
   yesterday = datetime.now() - timedelta(days=1)
   date_str = yesterday.strftime('%Y%m%d')
   url = f"http://data.gdeltproject.org/gdeltv2/{date_str}.export.CSV.zip"
   
   response = requests.get(url, timeout=30)
   print(f"Status: {response.status_code}, Size: {len(response.content)} bytes")
   ```

**Deliverables:**
- [ ] PostgreSQL database running
- [ ] Schema created and validated
- [ ] GDELT CSV access confirmed
- [ ] Dev environment configured

---

### **Day 3-5: Event Ingestion Pipeline** (12 hours)

**Objectives:**
- Build automated CSV download and parsing
- Implement 58-column event parser
- Add incremental loading with deduplication
- Create CAMEO categorization

**Tasks:**

1. **Build CSV downloader** (see `event_ingestion.py` below)
   - Download daily/hourly GDELT batches
   - Handle .zip compression
   - Retry logic with exponential backoff
   - Progress tracking

2. **Create event parser**
   - Parse 58 tab-separated columns
   - Handle missing/malformed data
   - Type conversion and validation
   - Error logging

3. **Implement database insertion**
   - Batch inserts (1000 rows at a time)
   - Conflict handling (ON CONFLICT DO NOTHING)
   - Transaction management
   - Performance optimization

4. **Add CAMEO mapping** (see `cameo_mapping.py` below)
   - Map event codes to socioeconomic domains
   - Add keyword matching for refinement
   - Store categorization in database

**Deliverables:**
- [ ] Automated daily ingestion working
- [ ] 100K+ events ingested successfully
- [ ] CAMEO categorization functional
- [ ] Error handling robust

---

### **Day 6-7: Validation & Scaling** (8 hours)

**Objectives:**
- Ingest full week of data (500K+ events)
- Validate data quality
- Optimize query performance
- Document ingestion process

**Tasks:**

1. **Scale ingestion**
   - Ingest 7 days of historical data
   - Monitor memory usage and performance
   - Add database indexes
   - Optimize batch sizes

2. **Data quality validation**
   - Check for duplicate events
   - Validate CAMEO code distribution
   - Verify geographic coordinates
   - Test socioeconomic categorization

3. **Performance testing**
   - Benchmark insert speed
   - Test query response times
   - Add connection pooling if needed
   - Monitor database size

4. **Documentation**
   - Document ingestion process
   - Create troubleshooting guide
   - Add data quality metrics
   - Write operator instructions

**Deliverables:**
- [ ] 500K+ events in database
- [ ] Data quality report generated
- [ ] Query performance benchmarks
- [ ] Documentation complete

**Week 1 Checkpoint:**
- ✅ Database operational with 500K+ events
- ✅ Automated daily ingestion
- ✅ CAMEO categorization working
- ✅ Foundation ready for analytics

---

## 📅 Week 2: Actor Networks + Geospatial

### **Day 8-10: Actor Network Analysis** (12 hours)

**Objectives:**
- Build actor network construction
- Implement community detection
- Create network visualizations
- Add influence metrics

**Tasks:**

1. **Network construction** (see `actor_networks.py` below)
   - Query events by date range and filters
   - Build NetworkX graph (nodes = actors, edges = interactions)
   - Weight edges by interaction frequency
   - Add edge attributes (event types, sentiment, Goldstein)

2. **Community detection**
   - Apply Louvain algorithm for communities
   - Calculate modularity scores
   - Identify coalition structures
   - Label communities

3. **Influence metrics**
   - Betweenness centrality (broker actors)
   - Eigenvector centrality (influential actors)
   - PageRank (importance ranking)
   - Degree distribution

4. **Visualization**
   - Create interactive network graphs (Plotly)
   - Color-code by community
   - Size nodes by influence
   - Filter by event type

**Deliverables:**
- [ ] Actor network module functional
- [ ] Community detection working
- [ ] Influence scores calculated
- [ ] Interactive visualizations

---

### **Day 11-12: Geospatial Analysis** (8 hours)

**Objectives:**
- Build geographic event clustering
- Create interactive heatmaps
- Add country-level aggregation
- Implement cross-border analysis

**Tasks:**

1. **Geographic clustering** (see `geo_analysis.py` below)
   - Use DBSCAN for spatial clustering
   - Identify event hotspots
   - Calculate cluster statistics
   - Track hotspot evolution over time

2. **Interactive heatmaps**
   - Create Folium maps with event markers
   - Add choropleth layers (country-level)
   - Color-code by event type/sentiment
   - Add popup details for events

3. **Country aggregation**
   - Group events by country
   - Calculate event type distribution
   - Compute sentiment averages
   - Track temporal trends

4. **Cross-border analysis**
   - Identify border region events
   - Analyze bilateral interactions
   - Track conflict/cooperation patterns
   - Visualize trade routes, migration, conflict zones

**Deliverables:**
- [ ] Geographic clustering operational
- [ ] Interactive Folium maps
- [ ] Country-level dashboards
- [ ] Border analysis tools

---

### **Day 13-14: API + Demo Dashboard** (8 hours)

**Objectives:**
- Expose REST API endpoints
- Build Streamlit demo dashboard
- User testing and refinement
- Prepare client demo

**Tasks:**

1. **REST API** (see `api.py` below)
   - FastAPI application
   - Event search endpoint
   - Actor network endpoint
   - Geographic heatmap endpoint
   - API documentation (Swagger)

2. **Streamlit Dashboard**
   - Date range selector
   - Event type filter
   - Actor selection
   - Network visualization panel
   - Geographic map panel
   - Summary statistics

3. **User Testing**
   - Test with sample socioeconomic queries
   - Validate response times
   - Check visualization clarity
   - Gather feedback from 2-3 users

4. **Client Demo Preparation**
   - Prepare 5-10 compelling examples
   - Create demo script
   - Document key insights
   - Practice presentation

**Deliverables:**
- [ ] REST API operational (5+ endpoints)
- [ ] Streamlit dashboard live
- [ ] User testing complete
- [ ] Client demo ready

**Week 2 Checkpoint:**
- ✅ Actor network analysis functional
- ✅ Geospatial clustering working
- ✅ Interactive dashboard deployed
- ✅ Ready for client validation

---

## 🗂️ Code Structure

```
D34_media_intelligence/
├── event_db/
│   ├── __init__.py
│   ├── config.py              # Database config, API keys
│   ├── schema_events.sql      # PostgreSQL schema
│   ├── event_ingestion.py     # CSV download + parsing
│   ├── cameo_mapping.py       # CAMEO to domain mapping
│   ├── actor_networks.py      # Network analysis
│   ├── geo_analysis.py        # Geospatial clustering
│   ├── api.py                 # FastAPI endpoints
│   └── utils.py               # Helper functions
├── dashboards/
│   ├── streamlit_app.py       # Main dashboard
│   └── components/            # Reusable components
├── tests/
│   ├── test_ingestion.py
│   ├── test_networks.py
│   └── test_api.py
├── notebooks/
│   ├── event_db_exploration.ipynb
│   └── network_analysis_examples.ipynb
├── data/
│   └── cameo_codes.json       # CAMEO code reference
├── logs/
│   └── ingestion.log
└── README_EVENT_DB.md
```

---

## 🛠️ Starter Code

I'll create the following files to get you started immediately:

1. **schema_events.sql** - PostgreSQL database schema
2. **event_ingestion.py** - CSV download and parsing
3. **cameo_mapping.py** - CAMEO to socioeconomic domain mapping
4. **actor_networks.py** - Network analysis module
5. **geo_analysis.py** - Geospatial clustering
6. **api.py** - FastAPI REST endpoints
7. **streamlit_app.py** - Interactive dashboard
8. **config.py** - Configuration management

Each file will include:
- Complete implementation (not stubs)
- Robust error handling
- Professional logging
- Inline documentation
- Type hints

---

## 💰 Infrastructure Budget

### **Week 1-2 (Development)**
- **Local PostgreSQL:** $0 (localhost)
- **GDELT data:** $0 (free CSV exports)
- **Python packages:** $0 (open source)
- **Total:** $0/month

### **Week 3+ (Production/Demo)**
- **Heroku PostgreSQL:** $9-50/month (Hobby-Basic tier, 10M rows)
- **Heroku dyno (web):** $7-25/month (Hobby tier)
- **Heroku dyno (worker):** $7/month (for daily ingestion)
- **Total:** $23-82/month

**Recommended Start:** Local development (Week 1-2), then Heroku Hobby tier ($23/month) for demos.

---

## ✅ Validation Checklist

### **Technical Validation**
- [ ] 500K+ events ingested without errors
- [ ] Query response times <5 seconds
- [ ] Network graphs generate in <15 seconds
- [ ] CAMEO categorization >90% accuracy (manual sample)
- [ ] API endpoints all functional
- [ ] Dashboard loads in <3 seconds

### **Business Validation**
- [ ] Demo to 3+ potential users
- [ ] 2-3 specific use cases validated
- [ ] Feedback indicates value proposition
- [ ] Pricing/engagement model identified
- [ ] Decision: Build full platform OR pivot OR stop

---

## 🚦 Go/No-Go Decision Points

**After Week 1:**
- ✅ **GO:** If ingestion works smoothly, data quality is good
- ⚠️ **PIVOT:** If GDELT data quality is poor, consider alternative sources
- ❌ **STOP:** If technical complexity exceeds value

**After Week 2:**
- ✅ **GO:** If demos receive positive feedback, clear use cases emerge
- ⚠️ **PIVOT:** If different analytics needed (not networks), adjust scope
- ❌ **STOP:** If no clear demand or differentiation

**After User Testing:**
- ✅ **BUILD FULL PLATFORM:** If validated demand + willing to pay/engage
- ⚠️ **ITERATE:** If feedback suggests different features
- ❌ **PORTFOLIO ONLY:** If no market fit, keep as demo

---

## 📊 Success Metrics

**Week 1 Targets:**
- 500K+ events in database
- <2 minutes to ingest 1 day of data
- >95% successful parse rate
- 0 critical bugs

**Week 2 Targets:**
- Generate network graph for 1000 events in <15 sec
- Create heatmap for 10K events in <10 sec
- API responds to 10 concurrent requests
- Dashboard loads in <3 seconds

**Business Targets:**
- 3+ user demos completed
- 2+ positive feedback sessions
- 1+ potential client/partner identified
- Clear next steps defined

---

## 🚀 Let's Start Building

**Next Immediate Actions:**

1. **Review this plan** - Confirm scope and timeline
2. **Set up environment** - PostgreSQL + Python deps
3. **Run Day 1 setup** - Database schema + test GDELT access
4. **Begin Day 3 implementation** - Event ingestion pipeline

I'll now create all the starter code files. Ready?

---

**Timeline:** 2-3 weeks (40-60 hours)  
**Risk:** Low - focused scope, manageable commitment  
**Upside:** Validates demand, builds on existing work, portfolio++  

Let's build! 🔨
