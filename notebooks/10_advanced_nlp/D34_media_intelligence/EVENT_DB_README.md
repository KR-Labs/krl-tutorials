# Event Database Analytics - Lightweight MVP

## 🎯 Overview

This directory contains **in-memory prototypes** of Event Database analytics that work with GDELT data **without requiring PostgreSQL or infrastructure setup**.

Perfect for:
- 🚀 **Rapid prototyping** - Test analytics before infrastructure investment
- 💼 **Portfolio demos** - Show capabilities without deployment
- 🧪 **MVP validation** - Prove demand before 40-60 hour database build
- 📊 **Research projects** - Analyze 100-1000 events in Jupyter notebooks

---

## 📁 File Structure

```
event_db/                    # Full database implementation (40-60 hours)
├── schema_events.sql        # PostgreSQL schema (58 columns)
├── event_ingestion.py       # CSV download pipeline
├── cameo_mapping.py         # CAMEO categorization (DB version)
├── actor_networks.py        # Network analysis (DB version)
├── geo_analysis.py          # Geospatial clustering (DB version)
├── api.py                   # FastAPI REST endpoints
└── config.py                # Database configuration

event_db_lite.py             # 🌟 LIGHTWEIGHT IN-MEMORY VERSION
                             # Works with DataFrames, no database required!

D34_media_intelligence_advanced.ipynb  # Notebook with integrated analytics
```

---

## 🚀 Quick Start (In-Memory MVP)

### Option 1: Use the Notebook (Recommended)

1. Open `D34_media_intelligence_advanced.ipynb`
2. Run cells sequentially through Part 3
3. Get results in seconds without infrastructure

**What you'll see:**
- ✅ CAMEO event categorization (6 socioeconomic domains)
- ✅ Actor network analysis (who did what to whom)
- ✅ Geospatial clustering (hotspot detection)
- ✅ Interactive visualizations (network graphs, maps)

### Option 2: Use event_db_lite.py Directly

```python
from event_db_lite import CAMEOMapperLite, ActorNetworkAnalyzerLite, GeoEventAnalyzerLite
import pandas as pd

# 1. Load GDELT event data (from CSV or connector)
events_df = pd.read_csv('gdelt_events.csv')

# 2. Categorize by socioeconomic domain
mapper = CAMEOMapperLite()
events_df = mapper.categorize_dataframe(events_df)

# 3. Build actor network
network = ActorNetworkAnalyzerLite()
interactions = network.build_interactions_df(events_df)
G = network.build_graph(interactions)
top_actors = network.get_top_actors(G, n=10)

# 4. Cluster geographically
geo = GeoEventAnalyzerLite()
events_df = geo.cluster_events(events_df)
hotspots = geo.get_hotspots(events_df)
```

---

## 📊 What Each Module Does

### `event_db_lite.py` (Lightweight, No Database)

**CAMEOMapperLite**
- Maps CAMEO event codes → socioeconomic domains
- 75+ predefined mappings (labor, health, inequality, education, governance, climate)
- Works directly on DataFrames

**ActorNetworkAnalyzerLite**
- Builds actor interaction networks from events
- Calculates centrality metrics (degree, betweenness, eigenvector)
- Detects communities (greedy modularity)
- No database queries - pure DataFrame operations

**GeoEventAnalyzerLite**
- Clusters events geographically (DBSCAN)
- Identifies hotspots (top N clusters by event count)
- Color-codes by conflict/cooperation (Goldstein scale)
- No PostGIS required - uses sklearn + numpy

---

## 🆚 Lite vs. Full Comparison

| Feature | event_db_lite.py (MVP) | event_db/ (Full) |
|---------|------------------------|------------------|
| **Setup Time** | 0 minutes | 2-4 hours |
| **Dependencies** | pandas, networkx, sklearn | + PostgreSQL, psycopg2, folium, fastapi |
| **Data Source** | In-memory DataFrames | PostgreSQL database |
| **Scale** | 100-1,000 events | 500K+ events/day |
| **Query Speed** | Instant (in-memory) | <5s (with indexes) |
| **Infrastructure** | None | PostgreSQL + Redis + API server |
| **Persistence** | None (re-run each time) | Permanent storage |
| **Real-time** | Manual fetch | Automated daily ingestion |
| **Historical** | Recent data only | 1979-present (BigQuery) |
| **Cost** | $0 | $23-82/month (production) |
| **Use Case** | Demos, prototypes, research | Production monitoring, dashboards |

---

## 🎯 When to Use Each

### Use `event_db_lite.py` if:
- ✅ Prototyping analytics approach
- ✅ Demoing capabilities to stakeholders
- ✅ Analyzing 100-1000 events (sufficient sample)
- ✅ Portfolio/consulting project
- ✅ One-time research analysis
- ✅ No infrastructure budget

### Use `event_db/` (full implementation) if:
- ✅ Monitoring 500K+ events daily
- ✅ Real-time alerting required
- ✅ Historical analysis (multi-year)
- ✅ Multiple users/dashboards
- ✅ API access for external tools
- ✅ Production SaaS product

---

## 📈 Development Roadmap

### Phase 1: MVP Prototype (✅ Complete - This!)
- In-memory analytics with real GDELT data
- CAMEO categorization, actor networks, geospatial clustering
- Interactive visualizations in Jupyter
- **Time:** 0 hours setup, works immediately
- **Cost:** $0

### Phase 2: User Validation (Next Step)
- Demo to 3+ potential users
- Gather feedback on features
- Confirm demand before infrastructure build
- **Time:** 1 week
- **Decision:** GO/NO-GO on full platform

### Phase 3: Database Implementation (If Validated)
- PostgreSQL setup + schema (4 hours)
- Daily ingestion pipeline (8 hours)
- API endpoints (8 hours)
- Streamlit dashboard (8 hours)
- **Time:** 40-60 hours
- **Cost:** $0 dev, $23-82/month production

### Phase 4: Deep NLP Extension (Optional)
- Full-text scraping (crawl4ai)
- Transformer NLP (stance detection, framing)
- GKG integration (entities, themes)
- **Time:** 40-80 hours additional

---

## 🧪 Example Workflow

### 1. Fetch GDELT Events
```python
from krl_data_connectors.professional.media.gdelt_enhanced import GDELTConnectorEnhanced

connector = GDELTConnectorEnhanced(use_bigquery=False)
events = connector.get_events(date='20250115', actor='USA', max_results=250)
events_df = pd.DataFrame(events)
```

### 2. Apply CAMEO Categorization
```python
from event_db_lite import CAMEOMapperLite

mapper = CAMEOMapperLite()
events_df = mapper.categorize_dataframe(events_df)

# See domain distribution
print(events_df['socioeconomic_domain'].value_counts())
```

### 3. Build Actor Network
```python
from event_db_lite import ActorNetworkAnalyzerLite

network = ActorNetworkAnalyzerLite()
interactions = network.build_interactions_df(events_df)
G = network.build_graph(interactions, directed=False)

# Get top actors
top_actors = network.get_top_actors(G, metric='degree', n=10)
for actor, score in top_actors:
    print(f"{actor}: {score:.4f}")

# Detect communities
communities = network.detect_communities(G)
print(f"Detected {len(set(communities.values()))} communities")
```

### 4. Geospatial Analysis
```python
from event_db_lite import GeoEventAnalyzerLite

geo = GeoEventAnalyzerLite()
events_df = geo.cluster_events(events_df, eps_km=50, min_samples=10)
hotspots = geo.get_hotspots(events_df, top_n=5)

print(hotspots[['cluster_id', 'event_count', 'center_lat', 'center_lon', 'avg_goldstein']])
```

---

## 💡 Key Insights Demonstrated

### CAMEO Categorization
- **300+ event codes** → **6 socioeconomic domains**
- Confidence scores for mapping quality
- Domain-specific network analysis

### Actor Networks
- "Who did what to whom?" intelligence
- Community detection (collaboration clusters)
- Centrality metrics (key actors identification)

### Geospatial Clustering
- DBSCAN algorithm for hotspot detection
- Goldstein scale (conflict/cooperation coloring)
- Geographic concentration patterns

---

## 🚧 Known Limitations (By Design)

### Data Constraints
- ⚠️ **100-1,000 events max** - In-memory limits
- ⚠️ **Recent data only** - CSV has 1-7 day lag
- ⚠️ **No persistence** - Re-run for updates
- ⚠️ **No real-time** - Manual fetch required

### Analytics Constraints
- ⚠️ **No temporal evolution** - Single snapshot only
- ⚠️ **No multi-week networks** - Limited time range
- ⚠️ **Simplified clustering** - No advanced algorithms
- ⚠️ **No caching** - Recompute on every run

### Infrastructure Constraints
- ⚠️ **No API** - Notebook-based only
- ⚠️ **No dashboard** - Manual visualization
- ⚠️ **No multi-user** - Single analyst
- ⚠️ **No automation** - Manual execution

**These are intentional trade-offs for rapid prototyping.**  
Full implementation removes all these constraints.

---

## 📚 Dependencies

### Minimal (event_db_lite.py)
```bash
pip install pandas numpy networkx scikit-learn
```

### Full Stack (event_db/ implementation)
```bash
pip install -r requirements.txt

# Includes:
# - psycopg2-binary (PostgreSQL)
# - sqlalchemy (ORM)
# - python-louvain (community detection)
# - folium (interactive maps)
# - fastapi, uvicorn (REST API)
# - streamlit (dashboard)
# - plotly (visualizations)
```

---

## 🎓 Learning Resources

### GDELT Documentation
- **Event Database:** https://blog.gdeltproject.org/gdelt-2-0-our-global-world-in-realtime/
- **CAMEO Taxonomy:** https://www.gdeltproject.org/data/documentation/CAMEO.Manual.1.1b3.pdf
- **BigQuery:** https://blog.gdeltproject.org/gdelt-2-0-now-in-google-bigquery/

### Methodology Papers
- **Actor Network Analysis:** Social network analysis methods
- **DBSCAN Clustering:** Density-based spatial clustering
- **Goldstein Scale:** Conflict/cooperation measurement

---

## 🤝 Contributing

This is a prototype demonstrating analytics patterns. For production use:

1. Review `TECHNICAL_SPECS.md` for full implementation details
2. See `EVENT_DB_IMPLEMENTATION.md` for 2-3 week build plan
3. Use `QUICKSTART.md` for database setup instructions

---

## 📄 License

Apache 2.0 (see repository LICENSE file)

---

## 🎯 Bottom Line

**event_db_lite.py = 5-minute MVP**  
**event_db/ = 40-60 hour production system**

Start with lite. Build full only when validated.

**Philosophy:** Prove demand before infrastructure investment.
