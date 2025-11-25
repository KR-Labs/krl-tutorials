# Quick Start - Generate Demos in 30 Minutes

**Goal:** Get from zero to 5 professional demos in ~30 minutes

**What you need:**
- Google Cloud account (with credits)
- Terminal access
- 30 minutes

---

## Step-by-Step (Copy/Paste Commands)

### 1. Navigate to Directory (30 seconds)

```bash
cd "/Users/bcdelo/Documents/GitHub/KRL/krl-tutorials/notebooks/10_advanced_nlp/D34_media_intelligence/lean_validation"
```

### 2. Run BigQuery Setup (5-7 minutes)

```bash
chmod +x setup_bigquery.sh
./setup_bigquery.sh
```

**What happens:**
- Creates Google Cloud project
- Enables BigQuery API
- Creates service account
- Downloads credentials
- Installs Python packages

**Manual step:** When prompted, go to https://console.cloud.google.com/billing and link your billing account

**Then press ENTER to continue**

### 3. Reload Shell (10 seconds)

```bash
source ~/.zshrc  # or source ~/.bashrc
```

This loads your credentials into the environment.

### 4. Test Connection (1 minute)

```bash
python test_connection.py
```

**Expected output:**
```
✓ BigQuery client initialized (Project: khipu-media-intel-XXXXXXXX)
✓ Retrieved 47 articles
✓ CONNECTION TEST PASSED

You're ready to generate demos!
```

**If you see errors**, check [README.md#troubleshooting](README.md#troubleshooting)

### 5. Generate Demos (10-15 minutes)

```bash
python generate_demos.py
```

**What happens:**
- Queries GDELT for 5 policy topics
- Runs spatial clustering on each
- Creates visualizations + reports
- Exports to `demos/` directory

**Expected output:**
```
✓ DEMO GENERATION COMPLETE

Generated 5 demos:

labor_strikes:
  Articles: 287
  Clusters: 8
  Files:
    • data: demos/labor_strikes/articles.csv
    • summary: demos/labor_strikes/cluster_summary.csv
    • map: demos/labor_strikes/map.html
    • report: demos/labor_strikes/report.txt

[... 4 more demos ...]
```

### 6. Review Demos (5 minutes)

```bash
# Open interactive maps
open demos/labor_strikes/map.html
open demos/housing_policy/map.html
open demos/healthcare_reform/map.html
open demos/climate_policy/map.html
open demos/education_policy/map.html

# Read executive reports
cat demos/labor_strikes/report.txt
```

**Look for:**
- 🗺️ US map with colored clusters (5-10 regional patterns)
- 📊 Cluster summaries showing different regional narratives
- 📄 Professional executive summary reports

### 7. Prepare for Customer Discovery (5-10 minutes)

**Pick your favorite demo** (probably labor_strikes or housing_policy)

**Review the key insights:**
```bash
cat demos/labor_strikes/report.txt | grep -A 10 "KEY INSIGHTS"
```

**Practice your pitch:**
- "This shows 8 distinct regional narrative patterns for labor strikes..."
- "Notice how [Location A] frames this as [X] while [Location B] frames it as [Y]..."
- "Traditional tools show volume, we show geographic narrative differences..."

---

## You Now Have

✅ **5 professional demos** showing spatial narrative clustering
✅ **Interactive visualizations** (HTML maps)
✅ **Executive reports** (text summaries)
✅ **Data exports** (CSV files)
✅ **A clear value proposition** (regional insights = better policy strategy)

---

## Next: Customer Discovery

### Who to Contact

**Target:** Policy analysts at think tanks

**Organizations:**
- Brookings Institution (Metropolitan Policy Program)
- Urban Institute (Housing Finance Policy Center)
- RAND Corporation (Health Policy)
- Center for American Progress (Economic Policy)
- New America (Education Policy)

### How to Contact

**LinkedIn:**
1. Search: "[Organization] policy analyst"
2. Filter: 2nd/3rd degree connections
3. Send connection request with note:

```
Hi [Name] - I noticed your work on [policy topic] at [Think Tank].

I've built an AI system that reveals regional narrative differences in
policy coverage (invisible to traditional monitoring tools).

Would you be open to a quick demo? I think it could be relevant to your work.
```

**Email:**
1. Find contact info on organization website
2. Send brief email (see README.md for template)
3. Attach HTML map for their area of interest

### The Ask

**Discovery call:** 15-20 minutes

**Goal:** Validate two things
1. **Problem:** Do they track regional media coverage? Is it painful?
2. **Willingness to pay:** Would they pay $75K/year for this solution?

### Decision Criteria

**After 10-15 calls, evaluate:**

**✅ Build full platform if:**
- 3+ express strong interest ("This is exactly what we need")
- 1+ requests pilot proposal
- Pricing doesn't immediately disqualify you

**⚠️ Pivot if:**
- Interest but pricing too high → Lower to $20K-30K, try again
- Wrong customer segment → Try consulting firms or government agencies
- Feature gaps → Adjust product, re-pitch

**❌ Stop if:**
- No interest across 10-15 calls
- They have solutions they're happy with
- "Nice to have" not "must have"

---

## What This Costs You

**Time:**
- Setup: 30 minutes
- Customer discovery: 1-2 weeks (10-15 calls × 20 min each = 5 hours)

**Money:**
- BigQuery: $0 (use GCP credits)
- Everything else: $0 (open source)

**Total: $0 and ~6 hours**

**What you get:**
- Real market validation
- Professional demos (portfolio)
- Decision data (build or pivot)

---

## If Validation Succeeds

**Then and only then**, proceed with the full 8-week build:
- Investment: $22K (dev + patent)
- Expected revenue: $112.5K Year 1
- ROI: 403%

**But validate first.** Don't fall in love with the solution before you know there's a problem worth solving.

---

## Troubleshooting

**Setup fails?**
- Check README.md#troubleshooting
- Verify GCP billing is linked
- Re-run `./setup_bigquery.sh`

**No demo outputs?**
- Some topics have less coverage (try different search terms)
- Extend time range (edit `generate_demos.py`, set `days_back=14`)
- Check BigQuery quota (shouldn't hit limits on free tier)

**Questions?**
- See detailed README.md
- Check main development plan for full specs

---

**Ready? Let's go!** 🚀

```bash
cd lean_validation
./setup_bigquery.sh
```
