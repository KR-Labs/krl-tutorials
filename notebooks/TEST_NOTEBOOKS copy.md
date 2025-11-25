# Testing Integration Phase 2 Notebooks

## Required API Keys

Before running the notebooks, you need to obtain API keys from these sources:

### Healthcare Causal Analysis Notebook (`healthcare_causal_gru.ipynb`)
1. **Census API Key**: https://api.census.gov/data/key_signup.html
   - Free, instant approval
   - Required for: Census ACS Detailed demographic data

2. **CDC Data**: https://wonder.cdc.gov/
   - Note: CDC Wonder API may not require authentication
   - Alternative: Use CDC API Gateway (https://data.cdc.gov/)

### Economic Forecasting Notebook (`economic_forecasting_transformer.ipynb`)
1. **FRED API Key**: https://fred.stlouisfed.org/docs/api/api_key.html
   - Free, instant approval
   - Required for: Federal Reserve economic data

2. **BLS API Key**: https://www.bls.gov/developers/home.htm
   - Free, registration required
   - Required for: Bureau of Labor Statistics employment data

3. **BEA API Key**: https://apps.bea.gov/api/signup/
   - Free, instant approval
   - Required for: Bureau of Economic Analysis GDP data

## Setup Instructions

### 1. Create .env file
```bash
cd /Users/bcdelo/Documents/GitHub/KRL/krl-tutorials
cp .env.example .env
```

### 2. Add your API keys to .env
```bash
# Edit .env with your actual keys
FRED_API_KEY=your_actual_fred_key
BLS_API_KEY=your_actual_bls_key
BEA_API_KEY=your_actual_bea_key
CENSUS_API_KEY=your_actual_census_key
CDC_API_KEY=your_actual_cdc_key  # if required
```

### 3. Load environment variables
In the notebook, add this cell at the beginning:
```python
import os
from dotenv import load_dotenv

# Load API keys from .env
load_dotenv()

# Configure connectors with API keys
os.environ['FRED_API_KEY'] = os.getenv('FRED_API_KEY')
os.environ['BLS_API_KEY'] = os.getenv('BLS_API_KEY')
os.environ['BEA_API_KEY'] = os.getenv('BEA_API_KEY')
os.environ['CENSUS_API_KEY'] = os.getenv('CENSUS_API_KEY')
os.environ['CDC_API_KEY'] = os.getenv('CDC_API_KEY')
```

## Testing Without API Keys (Mock Mode)

If you don't have API keys yet, you can test the notebooks with synthetic data:

### Option 1: Use Mock Data
```python
# Add to beginning of notebook
USE_MOCK_DATA = True

if USE_MOCK_DATA:
    # Generate synthetic data
    import numpy as np
    import pandas as pd
    
    # Create mock health data
    health_data = pd.DataFrame({
        'county_fips': np.repeat(np.arange(1000, 1100), 9),
        'year': np.tile(np.arange(2015, 2024), 100),
        'MORT_ALL_CAUSE': np.random.uniform(600, 1000, 900),
        'MORT_HEART_DISEASE': np.random.uniform(150, 300, 900),
        'MORT_CANCER': np.random.uniform(120, 250, 900),
        'PREV_DIABETES': np.random.uniform(8, 15, 900),
        'PREV_HYPERTENSION': np.random.uniform(25, 40, 900),
        'HEALTHCARE_ACCESS': np.random.uniform(70, 95, 900)
    })
    
    # Create mock demographic data
    demographic_data = pd.DataFrame({
        'county_fips': np.repeat(np.arange(1000, 1100), 9),
        'year': np.tile(np.arange(2015, 2024), 100),
        'MEDIAN_INCOME': np.random.uniform(40000, 80000, 900),
        'POVERTY_RATE': np.random.uniform(10, 25, 900),
        'EDUCATION_BACHELORS_PCT': np.random.uniform(15, 45, 900),
        'HOUSING_CROWDING': np.random.uniform(2, 8, 900),
        'UNEMPLOYMENT_RATE': np.random.uniform(3, 10, 900),
        'FOOD_STAMP_PCT': np.random.uniform(8, 20, 900),
        'INSURANCE_COVERAGE': np.random.uniform(80, 95, 900)
    })
```

### Option 2: Use krl-data-connectors Mock Mode
```python
# Set test mode in connectors
import os
os.environ['KRL_TEST_MODE'] = 'true'
os.environ['KRL_USE_MOCKS'] = 'true'

# Connectors will return synthetic data
from krl_data_connectors.professional.cdc_full import CDCFullConnector
cdc = CDCFullConnector()  # Will use mock data
```

## Expected Results

### Healthcare Notebook
- **Training time**: ~5-10 minutes on CPU
- **Expected metrics**: 
  - MAE: 50-150 (mortality rate scale)
  - RMSE: 80-200
  - R²: 0.60-0.85

### Economic Notebook
- **Training time**: ~10-15 minutes on CPU
- **Expected metrics**:
  - MAE: 0.3-0.6 (normalized scale)
  - RMSE: 0.4-0.8
  - Causal consistency: Errors increase along chain

## Troubleshooting

### Rate Limiting Issues
If you encounter rate limit errors:
1. Add delays between API calls
2. Cache responses locally
3. Use smaller date ranges for testing

### Missing Dependencies
```bash
pip install python-dotenv
pip install torch torchvision
pip install scikit-learn pandas numpy matplotlib seaborn
```

### Connector Import Errors
Ensure krl-data-connectors and krl-model-zoo are installed:
```bash
cd /Users/bcdelo/Documents/GitHub/KRL/Private\ IP/krl-data-connectors
pip install -e .

cd /Users/bcdelo/Documents/GitHub/KRL/Private\ IP/krl-model-zoo
pip install -e .
```

## License Validation

These notebooks use **Professional and Enterprise tier** connectors. Ensure:
1. Valid license file exists: `~/.krl/license.key`
2. License includes Professional/Enterprise tier access
3. License not expired

For testing purposes, the connectors should gracefully degrade to Community tier or mock data if licenses aren't available.

## Next Steps

After successful testing:
1. Document any rate limiting issues encountered
2. Note actual runtime performance
3. Validate visualizations render correctly
4. Check that causal DAG constraints work as expected
5. Commit working notebooks to krl-tutorials repository
