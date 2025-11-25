# Lean Validation - Spatial Media Intelligence

## Overview

This is your **lean validation toolkit** to test market demand before building the full platform.

**Goal:** Create 5 compelling demos showing spatial narrative clustering, then validate think tank interest

**Investment:** $0 (use existing GCP credits)
**Timeline:** 1-2 weeks (10-15 hours)
**Risk:** Very low

---

## What You'll Create

5 demo outputs for different policy topics:

1. **Labor Strikes** → Brookings Metropolitan Policy Program
2. **Housing Policy** → Urban Institute Housing Finance Policy Center
3. **Healthcare Reform** → RAND Health Policy
4. **Climate Policy** → Center for American Progress Climate & Energy
5. **Education Policy** → New America Education Policy

Each demo includes:
- ✅ Articles with geographic coordinates (80%+ coverage)
- ✅ Spatial narrative clusters (5-10 regional patterns)
- ✅ Interactive map visualization
- ✅ Executive summary report
- ✅ Data exports (CSV)

---

## Setup (2-3 hours)

### Step 1: Run BigQuery Setup

```bash
cd lean_validation
chmod +x setup_bigquery.sh
./setup_bigquery.sh
```

This will:
1. Create Google Cloud project
2. Enable BigQuery API
3. Create service account with permissions
4. Generate credentials
5. Install Python dependencies

**Important:** You'll need to link a billing account manually. Go to:
https://console.cloud.google.com/billing

(You should have GCP credits available)

### Step 2: Reload Shell Config

```bash
source ~/.zshrc  # or source ~/.bashrc
```

This loads the GOOGLE_APPLICATION_CREDENTIALS environment variable.

### Step 3: Test Connection

```bash
python test_connection.py
```

**Expected output:**
```
✓ BigQuery client initialized (Project: khipu-media-intel-XXXXXXXX)
✓ Retrieved 47 articles
  Geolocated: 85.1%
  Locations: 23
  Sources: 31
✓ CONNECTION TEST PASSED
```

If you see this, you're ready to generate demos!

---

## Generate Demos (1-2 hours)

### Run Demo Generation Script

```bash
python generate_demos.py
```

This will:
1. Query GDELT BigQuery for 5 policy topics
2. Run spatial clustering on each
3. Create visualizations and reports
4. Export everything to `demos/` directory

**Expected runtime:** 10-15 minutes for all 5 demos

**Output structure:**
```
demos/
├── labor_strikes/
│   ├── articles.csv           # Raw data
│   ├── cluster_summary.csv    # Cluster metadata
│   ├── map.html              # Interactive visualization
│   └── report.txt            # Executive summary
├── housing_policy/
│   └── ...
├── healthcare_reform/
│   └── ...
├── climate_policy/
│   └── ...
└── education_policy/
    └── ...
```

---

## Review Demos

### 1. Open Interactive Maps

```bash
# On Mac:
open demos/labor_strikes/map.html
open demos/housing_policy/map.html
# ... etc

# Or just double-click the HTML files
```

You should see:
- 🗺️ US map with article locations
- 🎨 Color-coded clusters (5-10 regional patterns)
- 📍 Hover to see article details

### 2. Read Executive Reports

```bash
cat demos/labor_strikes/report.txt
```

Each report includes:
- Coverage statistics
- Cluster summaries with sample headlines
- Key insights (regional differences)
- Value proposition for think tanks
- Pilot program details

### 3. Examine Data

```bash
head demos/labor_strikes/articles.csv
head demos/labor_strikes/cluster_summary.csv
```

---

## Customer Discovery (1-2 weeks)

Now you have 5 professional demos. Time to validate demand.

### Target Contacts (10-15 people)

#### Brookings Institution
- Metropolitan Policy Program (labor/housing)
- Economic Studies (policy analysis)

#### Urban Institute
- Housing Finance Policy Center
- Income & Benefits Policy Center

#### RAND Corporation
- Health Policy
- Infrastructure, Transportation & Environment

#### Center for American Progress
- Economic Policy Team
- Climate & Energy

#### New America
- Education Policy
- Political Reform Program

### Outreach Strategy

**Email Template:**

```
Subject: Early warning system for policy resistance - 2 weeks before opposition emerges

Hi [Name],

I noticed [Think Tank] recently published [specific report] on [policy topic].

I've built an AI system that predicts regional resistance to policy proposals
2 weeks before opposition campaigns emerge - using spatial analysis of 758M
media signals.

Example: Our analysis of [relevant topic] showed:
• [X] distinct regional narrative patterns
• [Location 1]: [narrative description]
• [Location 2]: [different narrative]

This reveals geographic differences invisible to traditional media monitoring.

Would you be open to a 15-minute demo showing how this works for your research areas?

Best,
Brandon

P.S. - I've attached a sample analysis of [topic relevant to their work]
```

**Attachment:** Send them the HTML map + text report for the most relevant demo

### Discovery Call Script (15-20 minutes)

**Minute 1-3: Context**
- "Thanks for your time. I'll show you something in 15 minutes that could
  save your organization $50K-100K per policy study."
- "May I ask: How do you currently track media coverage of your policy
  recommendations?"

**Minute 4-10: Demo**
- Share screen → Open HTML map
- Walk through: "This is 7 days of coverage on [topic]..."
- Point out: "Notice the regional clusters - [Location A] frames this as
  [narrative], while [Location B] frames it as [different narrative]"
- Ask: "Is this difference meaningful for your policy work?"

**Minute 11-15: Validation Questions**
- "How much do you spend annually on policy studies?" (Get to ROI)
- "Have any of your recommendations faced unexpected regional resistance?"
  (Pain point validation)
- "If you could predict that 2 weeks in advance, what's that worth?" (Value)
- "Would your organization pay $75K/year for this capability?" (Price test)

**Minute 16-20: Next Steps**
- If interested: "Let me send you a pilot proposal - 3 months, $18.75K,
  10 custom analyses"
- If not interested: "What would make this more valuable to you?" (Learn)

### Success Metrics

**Strong Interest Signals:**
- "This is exactly what we need"
- "Can we start a pilot?"
- "Let me introduce you to [decision maker]"
- "What's your availability for next steps?"

**Lukewarm Signals:**
- "Interesting, send me more info"
- "I'll think about it"
- "We'd need to see a longer trial"

**Decision Criteria:**

**✅ PROCEED with full 8-week build if:**
- 3+ contacts express strong interest
- At least 1 requests pilot proposal
- Pricing ($75K/year) doesn't immediately disqualify you

**⚠️ PIVOT if:**
- Lukewarm responses across the board
- No one willing to pay >$20K/year
- Feature requests would require 6+ months to build

**❌ STOP if:**
- No interest after 10-15 calls
- They already have solutions they like
- Market says "nice to have, not must-have"

---

## Cost Analysis

### Actual Costs (Lean Validation)

- Google Cloud (BigQuery): **$0** (use credits)
- Python dependencies: **$0** (open source)
- Your time: 10-15 hours over 1-2 weeks

**Total investment:** $0

### If You Proceed to Full Build

- Weeks 1-4 (MVP build): $258 (BigQuery + Jina Reader)
- Weeks 5-8 (Customer pilots): $0 (deferred revenue)
- Month 9+ (Patent filing): $20,000 (if traction)

**Total Year 1:** $22,258 investment

**Expected Year 1 revenue:** $18.75K - $112.5K (1-2 customers)

---

## Files in This Directory

| File | Purpose |
|------|---------|
| `setup_bigquery.sh` | Automated Google Cloud setup |
| `gdelt_connector.py` | BigQuery connector (simplified) |
| `spatial_clustering.py` | Patent-pending algorithm |
| `generate_demos.py` | Creates 5 demo outputs |
| `test_connection.py` | Verify BigQuery access |
| `README.md` | This file |

---

## Troubleshooting

### Problem: "Could not determine credentials"

**Solution:**
```bash
echo $GOOGLE_APPLICATION_CREDENTIALS
# Should show: /Users/bcdelo/khipu-credentials/gdelt-bigquery.json

# If not:
export GOOGLE_APPLICATION_CREDENTIALS="$HOME/khipu-credentials/gdelt-bigquery.json"
source ~/.zshrc
```

### Problem: "No articles found"

**Solutions:**
- Try broader search terms (change in `generate_demos.py`)
- Extend time range (`days_back=14` instead of `7`)
- Different topic (some have more coverage than others)

### Problem: "Permission denied on bigquery.jobs.create"

**Solution:**
```bash
# Re-run permission grants
PROJECT_ID=$(gcloud config get-value project)

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:gdelt-reader@${PROJECT_ID}.iam.gserviceaccount.com" \
    --role="roles/bigquery.user"
```

### Problem: "Embedding model download fails"

**Solution:**
```bash
# Sentence transformers needs to download model on first run
# Make sure you have internet connection
# If firewall issues, download manually:

python3 -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
```

---

## Next Steps After Validation

### If Strong Interest (3+ contacts)

**Week 1-2:**
- Draft 2 pilot proposals ($18.75K each)
- Send to most interested contacts
- Negotiate terms

**Week 3-4:**
- Sign first pilot
- Begin 8-week full build (see main development plan)

**Month 3-6:**
- Execute pilots
- Collect testimonials
- Refine product based on feedback

**Month 7-9:**
- Convert pilots to annual contracts
- File provisional patent
- Scale to 3-5 customers

### If Lukewarm Interest

**Option 1:** Adjust positioning
- Lower price point ($20K-30K/year)
- Different customer segment (consulting firms?)
- Feature pivot (what did they actually want?)

**Option 2:** Portfolio piece
- Keep demos in portfolio
- Showcase technical skills:
  - BigQuery integration
  - Patent-pending algorithm (λ_spatial=0.15)
  - Professional visualizations
- Move on to next project

### If No Interest

**Accept reality:**
- Market validation failed
- Don't build the full platform
- Learned valuable lessons:
  - How to do customer discovery
  - BigQuery + spatial clustering
  - Professional demo creation

**Portfolio value:**
- Still demonstrates strong technical skills
- Shows ability to:
  - Integrate complex APIs
  - Implement novel algorithms
  - Create production-quality outputs
  - Validate ideas before building

---

## Key Takeaways

**This lean validation approach:**

✅ **Minimizes risk**
- $0 investment
- 1-2 weeks time
- Learn before you build

✅ **Maximizes learning**
- Real customer feedback
- Market validation
- Pricing insights

✅ **Provides options**
- Strong interest → Build full platform
- Lukewarm → Pivot or adjust
- No interest → Portfolio piece, move on

**The full 8-week build makes sense ONLY if this validation succeeds.**

Don't fall in love with the solution. Fall in love with the problem. If think tanks don't have this problem (or won't pay $75K to solve it), that's valuable data.

---

**Questions or issues?**

Check the main development plan for detailed technical specs, or reach out if you hit blockers during setup.

Good luck! 🚀
