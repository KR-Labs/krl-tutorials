# API Keys & Testing Guide for Multi-Domain Workflows

**Status:** ✅ All 3 integration workflows implemented and committed  
**Next Step:** Test with real connector data using API keys

---

## Overview

The three integration workflows demonstrate Sprint 7 enhancements with real-world use cases:

1. **Education Equity LSTM** (`education_equity_lstm.ipynb`)
   - Community tier connectors (FREE)
   - Ready to test with NCES + Census ACS Public

2. **Healthcare Causal GRU** (`healthcare_causal_gru.ipynb`)
   - Professional tier connectors ($149-599/mo)
   - Requires CDC, SAMHSA, Census ACS Detailed API keys

3. **Economic Forecasting Transformer** (`economic_forecasting_transformer.ipynb`)
   - Professional tier connectors ($149-599/mo)
   - Requires FRED, BLS, BEA API keys

---

## Required API Keys

### Community Tier (FREE)

**1. NCES (National Center for Education Statistics)**
- **Acquisition:** No API key required (public data)
- **Documentation:** https://nces.ed.gov/ccd/
- **Rate Limit:** Unlimited
- **Used in:** `education_equity_lstm.ipynb`

**2. Census ACS Public API**
- **Acquisition:** Request free key at https://api.census.gov/data/key_signup.html
- **Environment Variable:** `CENSUS_API_KEY`
- **Rate Limit:** 500 requests/day
- **Used in:** `education_equity_lstm.ipynb`, `healthcare_causal_gru.ipynb`

---

### Professional Tier ($149-599/mo)

**3. FRED (Federal Reserve Economic Data)**
- **Acquisition:** Request free key at https://fred.stlouisfed.org/docs/api/api_key.html
- **Environment Variable:** `FRED_API_KEY`
- **Rate Limit:** 100 requests/day (Community), 1000/day (Professional)
- **Used in:** `economic_forecasting_transformer.ipynb`
- **Series Required:**
  - `FEDFUNDS` - Federal Funds Rate
  - `A191RL1Q225SBEA` - Real GDP Growth Rate
  - `INDPRO` - Industrial Production Index
  - `CPIAUCSL` - Consumer Price Index

**4. BLS (Bureau of Labor Statistics)**
- **Acquisition:** Request key at https://www.bls.gov/developers/home.htm
- **Environment Variable:** `BLS_API_KEY`
- **Rate Limit:** 25 requests/day (unregistered), 500/day (registered)
- **Used in:** `economic_forecasting_transformer.ipynb`
- **Series Required:**
  - `LNS14000000` - Unemployment Rate
  - `CES0500000003` - Average Hourly Earnings

**5. BEA (Bureau of Economic Analysis)**
- **Acquisition:** Request key at https://apps.bea.gov/api/signup/
- **Environment Variable:** `BEA_API_KEY`
- **Rate Limit:** 1000 requests/day
- **Used in:** `economic_forecasting_transformer.ipynb`

**6. CDC (Centers for Disease Control)**
- **Acquisition:** CDC Wonder (https://wonder.cdc.gov/) - No API key for public data
- **API Documentation:** https://wonder.cdc.gov/wonder/help/API.html
- **Environment Variable:** `CDC_API_KEY` (if using restricted datasets)
- **Used in:** `healthcare_causal_gru.ipynb`
- **Datasets Required:**
  - Chronic Disease Indicators (diabetes, heart disease, obesity prevalence)

**7. SAMHSA (Substance Abuse and Mental Health Services)**
- **Acquisition:** Contact SAMHSA for data access at https://www.samhsa.gov/data/
- **Environment Variable:** `SAMHSA_API_KEY`
- **Rate Limit:** Varies by dataset
- **Used in:** `healthcare_causal_gru.ipynb`
- **Datasets Required:**
  - National Survey on Drug Use and Health (NSDUH) state-level data

**8. Census ACS Detailed**
- **Acquisition:** Same as Census ACS Public (free key)
- **Environment Variable:** `CENSUS_API_KEY`
- **Documentation:** https://www.census.gov/data/developers/data-sets/acs-5year.html
- **Used in:** `healthcare_causal_gru.ipynb`
- **Variables Required:**
  - `B17001_002E` - Population below poverty level
  - `B01003_001E` - Total population
  - `B15003_022E` - Bachelor's degree or higher
  - `B27001_005E` - Uninsured population

---

## Setup Instructions

### 1. Environment Variables

Create a `.env` file in the project root:

```bash
# Community Tier (FREE)
CENSUS_API_KEY=your_census_api_key_here

# Professional Tier
FRED_API_KEY=your_fred_api_key_here
BLS_API_KEY=your_bls_api_key_here
BEA_API_KEY=your_bea_api_key_here
CDC_API_KEY=your_cdc_api_key_here  # If using restricted datasets
SAMHSA_API_KEY=your_samhsa_api_key_here
```

### 2. Load Environment Variables in Notebooks

Add this cell at the top of each notebook:

```python
import os
from dotenv import load_dotenv

# Load API keys from .env file
load_dotenv()

# Verify keys are loaded
required_keys = ['CENSUS_API_KEY']  # Adjust per notebook
for key in required_keys:
    if not os.getenv(key):
        print(f"⚠️ WARNING: {key} not found in environment!")
    else:
        print(f"✅ {key} loaded")
```

### 3. Configure Connectors

Update connector initialization with API keys:

```python
# Example: Census ACS Public connector
from krl_data_connectors.community import CensusACSPublicConnector

census = CensusACSPublicConnector(api_key=os.getenv('CENSUS_API_KEY'))
```

---

## Testing Checklist

### Education Equity LSTM (Community Tier)

- [ ] **Census API key obtained** (free)
- [ ] **NCES data accessible** (no key required)
- [ ] **Run notebook cell-by-cell**
  - [ ] Data ingestion cells (NCES, Census)
  - [ ] Equity factor engineering cell
  - [ ] LSTM training cell (50 epochs, ~5-10 minutes)
  - [ ] Evaluation cell (accuracy + fairness metrics)
  - [ ] Visualization cells (6 plots)
- [ ] **Verify outputs:**
  - [ ] Schools dataset has >1000 records
  - [ ] Demographics dataset has 58 counties (CA)
  - [ ] Equity factors shape: (n_schools, 3)
  - [ ] Training loss decreases over epochs
  - [ ] R² score > 0.5
  - [ ] Fairness score (demographic parity) < 0.1
  - [ ] Comparison shows equity LSTM has lower fairness score than standard LSTM

### Healthcare Causal GRU (Professional Tier)

- [ ] **CDC API key obtained**
- [ ] **SAMHSA API key obtained**
- [ ] **Census API key obtained** (same as above)
- [ ] **Run notebook cell-by-cell**
  - [ ] Causal DAG construction cell (9 variables, 12 edges)
  - [ ] Causal mask computation cell (44% sparsity)
  - [ ] Data ingestion cells (CDC, SAMHSA, Census)
  - [ ] GRU training cell (50 epochs, ~5-10 minutes)
  - [ ] Causal consistency check cell
  - [ ] Policy simulation cell (poverty reduction)
- [ ] **Verify outputs:**
  - [ ] DAG visualization shows 3 levels (social → behavioral → outcomes)
  - [ ] Causal mask has 36 blocked connections (44% sparsity)
  - [ ] State-level data has 50 states × 3 years = 150 samples
  - [ ] Training loss decreases over epochs
  - [ ] Causal consistency test: pred_change < 0.01 (PASS)
  - [ ] Policy simulation: 10% poverty reduction → diabetes reduction
  - [ ] Comparison shows causal GRU maintains accuracy with enforced causality

### Economic Forecasting Transformer (Professional Tier)

- [ ] **FRED API key obtained**
- [ ] **BLS API key obtained**
- [ ] **BEA API key obtained**
- [ ] **Run notebook cell-by-cell**
  - [ ] Economic DAG construction cell (6 variables, 10 edges)
  - [ ] Causal PE computation cell (ancestor/descendant/hub penalty)
  - [ ] Data ingestion cells (FRED, BLS, BEA)
  - [ ] Transformer training cell (50 epochs, ~10-15 minutes)
  - [ ] Forecast evaluation cell (1-month ahead inflation)
  - [ ] Policy simulation cell (interest rate increase)
- [ ] **Verify outputs:**
  - [ ] DAG visualization shows 4 levels (monetary → growth → labor → prices)
  - [ ] Causal PE: federal_funds_rate has highest descendant depth (1.0), hub penalty (0.67)
  - [ ] Time series data: 168 months (2010-2023), 6 features
  - [ ] Training loss decreases over epochs
  - [ ] RMSE < 1.0 (inflation forecasting accuracy)
  - [ ] Policy simulation: 1% rate increase → inflation reduction (expected)
  - [ ] Comparison shows causal Transformer improves interpretability

---

## Expected Runtime

| Notebook | Training Time (CPU) | Training Time (GPU) | Total Notebook Runtime |
|----------|---------------------|---------------------|------------------------|
| Education Equity LSTM | 5-10 min | 2-3 min | 15-20 min |
| Healthcare Causal GRU | 5-10 min | 2-3 min | 15-20 min |
| Economic Forecasting Transformer | 10-15 min | 3-5 min | 20-25 min |

**Hardware Recommendations:**
- **Minimum:** 8GB RAM, 4-core CPU
- **Recommended:** 16GB RAM, 8-core CPU, NVIDIA GPU (optional but speeds up training)

---

## Troubleshooting

### Common Issues

**1. API Rate Limiting**
```
Error: HTTPError 429 - Too Many Requests
```
**Solution:** Wait 24 hours for rate limit reset, or upgrade to Professional tier

**2. Missing Data**
```
Error: Series 'FEDFUNDS' not found
```
**Solution:** Check FRED series ID spelling, verify API key has access to series

**3. CUDA Out of Memory**
```
RuntimeError: CUDA out of memory
```
**Solution:** Reduce batch size (32 → 16 → 8) or use CPU (`device = torch.device('cpu')`)

**4. Causal Mask Shape Mismatch**
```
RuntimeError: Expected tensor shape (9, 9), got (6, 6)
```
**Solution:** Verify DAG variables match feature matrix columns exactly

**5. Synthetic Data Only**
```
Note: This demo uses synthetic data since Community tier only provides school directory
```
**Solution:** Upgrade to Professional tier for real longitudinal data (NCES CCD)

---

## Success Criteria

### Minimum Requirements (All Notebooks)
- ✅ All cells execute without errors
- ✅ Training loss decreases over epochs
- ✅ R² score > 0.3 (explains >30% variance)
- ✅ Visualizations render correctly

### Professional Quality (Production-Ready)
- ✅ R² score > 0.7 (explains >70% variance)
- ✅ Fairness metrics show demographic parity (education)
- ✅ Causal consistency verified (healthcare)
- ✅ Policy simulations produce expected directional effects
- ✅ Comparison shows Sprint 7 enhancements improve metrics

---

## Next Steps After Testing

1. **Document Results:**
   - Create `TESTING_RESULTS.md` with screenshots, metrics, and observations
   - Note any API issues, rate limits, or data quality problems

2. **Hyperparameter Tuning:**
   - Education: Experiment with `lambda_eq` (0.5, 0.7, 0.9)
   - Healthcare: Try different causal DAG structures
   - Economic: Test different sequence lengths (12, 24, 36 months)

3. **Production Deployment:**
   - Package notebooks as Python scripts
   - Set up automated data fetching pipelines
   - Deploy to cloud (AWS SageMaker, Azure ML, GCP Vertex AI)

4. **Customer Demos:**
   - Prepare presentation with key visualizations
   - Highlight fairness improvements (education)
   - Show causal consistency (healthcare)
   - Demonstrate policy simulation (economic)

5. **Professional Tier Marketing:**
   - Create comparison table: Community vs Professional tier
   - Document exclusive features (47 additional connectors)
   - Calculate ROI for Professional subscription

---

## API Key Security

**🔒 IMPORTANT: Never commit API keys to Git!**

Add to `.gitignore`:
```
.env
*.env
*_api_key.txt
secrets/
```

**Best Practices:**
- Store keys in environment variables or secret management service (AWS Secrets Manager, Azure Key Vault)
- Rotate keys every 90 days
- Use separate keys for dev/staging/production
- Monitor API usage to detect unauthorized access

---

## Support

**Issues with Connectors:**
- File GitHub issue: https://github.com/KR-Labs/krl-data-connectors/issues
- Email: support@kr-labs.com

**Issues with Models:**
- File GitHub issue: https://github.com/KR-Labs/krl-model-zoo/issues

**Professional Tier Upgrade:**
- Contact sales: sales@kr-labs.com
- Pricing: $149-599/mo (47 additional connectors, priority support)

---

## Conclusion

✅ **Integration Phase Complete:** All 3 multi-domain workflows implemented  
🔬 **Ready for Testing:** API keys required for real data validation  
🚀 **Next Milestone:** March 1, 2026 launch with Professional tier customers

**Patent-Safe Innovation Demonstrated:**
- Education: Equity-weighted LSTM attention (domain-specific fairness)
- Healthcare: Causal recurrence gates (domain-specific causality)
- Economic: Causal positional encoding (domain-specific graph-aware attention)

**Business Value Created:**
- Community tier: Free proof-of-concept (education workflow)
- Professional tier: $149-599/mo value demonstration (healthcare, economic workflows)
- Enterprise tier: Custom DAG integration, dedicated support ($999-5,000/mo)
