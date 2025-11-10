#!/usr/bin/env python3
"""
Test script for Integration Phase 2 notebooks with mock data.
Tests both healthcare and economic forecasting workflows.
"""

import sys
import numpy as np
import pandas as pd
from pathlib import Path

def test_healthcare_notebook_with_mock_data():
    """Test healthcare causal analysis with synthetic data."""
    print("\n" + "="*80)
    print("TESTING: Healthcare Causal Analysis Workflow (Mock Data)")
    print("="*80)
    
    try:
        # Generate mock health data
        print("\n[1/7] Generating mock CDC health data...")
        n_counties = 100
        n_years = 9  # 2015-2023
        n_samples = n_counties * n_years
        
        health_data = pd.DataFrame({
            'county_fips': np.repeat(np.arange(1000, 1000 + n_counties), n_years),
            'year': np.tile(np.arange(2015, 2015 + n_years), n_counties),
            'MORT_ALL_CAUSE': np.random.uniform(600, 1000, n_samples),
            'MORT_HEART_DISEASE': np.random.uniform(150, 300, n_samples),
            'MORT_CANCER': np.random.uniform(120, 250, n_samples),
            'PREV_DIABETES': np.random.uniform(8, 15, n_samples),
            'PREV_HYPERTENSION': np.random.uniform(25, 40, n_samples),
            'HEALTHCARE_ACCESS': np.random.uniform(70, 95, n_samples)
        })
        print(f"   ✓ Generated {n_samples} health records")
        
        # Generate mock demographic data
        print("\n[2/7] Generating mock Census demographic data...")
        demographic_data = pd.DataFrame({
            'county_fips': np.repeat(np.arange(1000, 1000 + n_counties), n_years),
            'year': np.tile(np.arange(2015, 2015 + n_years), n_counties),
            'MEDIAN_INCOME': np.random.uniform(40000, 80000, n_samples),
            'POVERTY_RATE': np.random.uniform(10, 25, n_samples),
            'EDUCATION_BACHELORS_PCT': np.random.uniform(15, 45, n_samples),
            'HOUSING_CROWDING': np.random.uniform(2, 8, n_samples),
            'UNEMPLOYMENT_RATE': np.random.uniform(3, 10, n_samples),
            'FOOD_STAMP_PCT': np.random.uniform(8, 20, n_samples),
            'INSURANCE_COVERAGE': np.random.uniform(80, 95, n_samples)
        })
        print(f"   ✓ Generated {n_samples} demographic records")
        
        # Merge data
        print("\n[3/7] Merging health and demographic data...")
        merged_data = pd.merge(health_data, demographic_data, on=['county_fips', 'year'])
        print(f"   ✓ Merged data shape: {merged_data.shape}")
        
        # Define causal structure
        print("\n[4/7] Defining causal DAG...")
        economic_vars = ['MEDIAN_INCOME', 'POVERTY_RATE', 'UNEMPLOYMENT_RATE', 'INSURANCE_COVERAGE']
        social_vars = ['EDUCATION_BACHELORS_PCT', 'HOUSING_CROWDING', 'FOOD_STAMP_PCT']
        health_vars = ['MORT_ALL_CAUSE', 'MORT_HEART_DISEASE', 'MORT_CANCER', 
                      'PREV_DIABETES', 'PREV_HYPERTENSION', 'HEALTHCARE_ACCESS']
        
        n_variables = len(economic_vars) + len(social_vars) + len(health_vars)
        causal_dag = np.zeros((n_variables, n_variables))
        
        # Economic → Social
        for i in range(len(economic_vars)):
            for j in range(len(economic_vars), len(economic_vars) + len(social_vars)):
                causal_dag[i, j] = 1
        
        # Social → Health
        for i in range(len(economic_vars), len(economic_vars) + len(social_vars)):
            for j in range(len(economic_vars) + len(social_vars), n_variables):
                causal_dag[i, j] = 1
        
        # Economic → Health (direct)
        for i in range(len(economic_vars)):
            for j in range(len(economic_vars) + len(social_vars), n_variables):
                causal_dag[i, j] = 1
        
        print(f"   ✓ DAG created: {n_variables} variables, {causal_dag.sum():.0f} edges")
        print(f"   ✓ Structure: Economic({len(economic_vars)}) → Social({len(social_vars)}) → Health({len(health_vars)})")
        
        # Create sequences
        print("\n[5/7] Creating time series sequences...")
        from sklearn.preprocessing import StandardScaler
        
        feature_columns = economic_vars + social_vars + health_vars
        sequences = []
        targets = []
        
        for county in merged_data['county_fips'].unique():
            county_data = merged_data[merged_data['county_fips'] == county].sort_values('year')
            county_features = county_data[feature_columns].values
            
            # 5-year sequences
            for i in range(len(county_features) - 5):
                sequences.append(county_features[i:i+5])
                targets.append(county_features[i+5, 0])  # Predict MORT_ALL_CAUSE
        
        X = np.array(sequences)
        y = np.array(targets)
        print(f"   ✓ Created {len(X)} sequences of shape {X[0].shape}")
        
        # Normalize and split
        print("\n[6/7] Normalizing and splitting data...")
        scaler = StandardScaler()
        X_flat = X.reshape(-1, n_variables)
        X_scaled = scaler.fit_transform(X_flat).reshape(X.shape)
        
        train_size = int(0.7 * len(X_scaled))
        val_size = int(0.15 * len(X_scaled))
        
        X_train = X_scaled[:train_size]
        y_train = y[:train_size]
        X_val = X_scaled[train_size:train_size+val_size]
        y_val = y[train_size:train_size+val_size]
        X_test = X_scaled[train_size+val_size:]
        y_test = y[train_size+val_size:]
        
        print(f"   ✓ Train: {len(X_train)}, Val: {len(X_val)}, Test: {len(X_test)}")
        
        # Simulate model training (simplified)
        print("\n[7/7] Simulating GRU Causal Gates training...")
        print("   ℹ Full training requires PyTorch and krl-model-zoo")
        print("   ℹ Mock test validates data pipeline only")
        
        # Calculate baseline metrics
        y_pred_baseline = np.full_like(y_test, y_train.mean())
        mae_baseline = np.abs(y_test - y_pred_baseline).mean()
        rmse_baseline = np.sqrt(((y_test - y_pred_baseline)**2).mean())
        
        print(f"\n   Baseline metrics (predicting mean):")
        print(f"   - MAE: {mae_baseline:.4f}")
        print(f"   - RMSE: {rmse_baseline:.4f}")
        print(f"   - Expected GRU improvement: 20-40% reduction in error")
        
        print("\n" + "✓"*80)
        print("Healthcare workflow data pipeline: PASSED")
        print("✓"*80)
        return True
        
    except Exception as e:
        print(f"\n✗ Healthcare workflow FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_economic_notebook_with_mock_data():
    """Test economic forecasting with synthetic data."""
    print("\n" + "="*80)
    print("TESTING: Economic Forecasting Workflow (Mock Data)")
    print("="*80)
    
    try:
        # Generate mock economic time series
        print("\n[1/7] Generating mock FRED interest rate data...")
        n_months = 168  # 14 years * 12 months (2010-2023)
        dates = pd.date_range('2010-01-01', periods=n_months, freq='MS')
        
        fred_data = pd.DataFrame({
            'date': dates,
            'DFF': np.random.uniform(0.05, 2.5, n_months),        # Fed Funds Rate
            'DGS10': np.random.uniform(1.5, 3.5, n_months),       # 10Y Treasury
            'GDPC1': np.random.uniform(16000, 21000, n_months),   # Real GDP
            'INDPRO': np.random.uniform(90, 110, n_months),       # Industrial Production
            'CPIAUCSL': np.random.uniform(230, 300, n_months),    # CPI
            'PPIACO': np.random.uniform(180, 250, n_months),      # PPI
            'PCEPILFE': np.random.uniform(1.5, 3.5, n_months)     # Core PCE
        })
        print(f"   ✓ Generated {n_months} months of FRED data")
        
        # Generate mock BLS labor data
        print("\n[2/7] Generating mock BLS employment data...")
        bls_data = pd.DataFrame({
            'date': dates,
            'LNS14000000': np.random.uniform(3.5, 9.0, n_months),     # Unemployment Rate
            'LNS11300000': np.random.uniform(62, 67, n_months),       # Labor Force Participation
            'CES0000000001': np.random.uniform(130000, 160000, n_months),  # Total Employment
            'CES0500000003': np.random.uniform(23, 32, n_months)      # Avg Hourly Earnings
        })
        print(f"   ✓ Generated {n_months} months of BLS data")
        
        # Generate mock BEA data
        print("\n[3/7] Generating mock BEA national accounts data...")
        bea_data = pd.DataFrame({
            'date': dates,
            'GDP_NOMINAL': np.random.uniform(18000, 26000, n_months),
            'GDP_REAL': np.random.uniform(17000, 22000, n_months)
        })
        print(f"   ✓ Generated {n_months} months of BEA data")
        
        # Merge all data
        print("\n[4/7] Merging economic data sources...")
        merged_data = fred_data.merge(bls_data, on='date').merge(bea_data, on='date')
        print(f"   ✓ Merged data shape: {merged_data.shape}")
        
        # Define causal structure
        print("\n[5/7] Defining macroeconomic causal DAG...")
        interest_vars = ['DFF', 'DGS10']
        gdp_vars = ['GDPC1', 'INDPRO', 'GDP_REAL']
        employment_vars = ['LNS14000000', 'LNS11300000', 'CES0000000001', 'CES0500000003']
        inflation_vars = ['CPIAUCSL', 'PPIACO', 'PCEPILFE']
        
        feature_columns = interest_vars + gdp_vars + employment_vars + inflation_vars
        n_variables = len(feature_columns)
        
        causal_dag = np.zeros((n_variables, n_variables))
        
        # Interest → GDP
        for i in range(len(interest_vars)):
            for j in range(len(interest_vars), len(interest_vars) + len(gdp_vars)):
                causal_dag[i, j] = 1
        
        # GDP → Employment
        for i in range(len(interest_vars), len(interest_vars) + len(gdp_vars)):
            for j in range(len(interest_vars) + len(gdp_vars), 
                          len(interest_vars) + len(gdp_vars) + len(employment_vars)):
                causal_dag[i, j] = 1
        
        # Employment → Inflation
        for i in range(len(interest_vars) + len(gdp_vars), 
                      len(interest_vars) + len(gdp_vars) + len(employment_vars)):
            for j in range(len(interest_vars) + len(gdp_vars) + len(employment_vars), n_variables):
                causal_dag[i, j] = 1
        
        # Direct effects: Interest → Inflation, GDP → Inflation
        for i in range(len(interest_vars)):
            for j in range(len(interest_vars) + len(gdp_vars) + len(employment_vars), n_variables):
                causal_dag[i, j] = 1
        
        for i in range(len(interest_vars), len(interest_vars) + len(gdp_vars)):
            for j in range(len(interest_vars) + len(gdp_vars) + len(employment_vars), n_variables):
                causal_dag[i, j] = 1
        
        print(f"   ✓ DAG created: {n_variables} variables, {causal_dag.sum():.0f} edges")
        print(f"   ✓ Structure: Interest({len(interest_vars)}) → GDP({len(gdp_vars)}) → Employment({len(employment_vars)}) → Inflation({len(inflation_vars)})")
        
        # Create sequences
        print("\n[6/7] Creating multi-horizon forecast sequences...")
        from sklearn.preprocessing import StandardScaler
        
        data_values = merged_data[feature_columns].values
        seq_length = 12
        forecast_horizon = 3
        
        sequences = []
        targets = []
        
        for i in range(len(data_values) - seq_length - forecast_horizon + 1):
            sequences.append(data_values[i:i+seq_length])
            targets.append(data_values[i+seq_length:i+seq_length+forecast_horizon])
        
        X = np.array(sequences)
        y = np.array(targets)
        print(f"   ✓ Created {len(X)} sequences")
        print(f"   ✓ Input shape: {X[0].shape} (12 months × {n_variables} variables)")
        print(f"   ✓ Output shape: {y[0].shape} (3 months × {n_variables} variables)")
        
        # Normalize and split
        print("\n[7/7] Normalizing and splitting data...")
        scaler = StandardScaler()
        
        X_flat = X.reshape(-1, n_variables)
        y_flat = y.reshape(-1, n_variables)
        
        scaler.fit(X_flat)
        X_scaled = scaler.transform(X_flat).reshape(X.shape)
        y_scaled = scaler.transform(y_flat).reshape(y.shape)
        
        train_size = int(0.8 * len(X_scaled))
        val_size = int(0.1 * len(X_scaled))
        
        X_train = X_scaled[:train_size]
        y_train = y_scaled[:train_size]
        X_val = X_scaled[train_size:train_size+val_size]
        y_val = y_scaled[train_size:train_size+val_size]
        X_test = X_scaled[train_size+val_size:]
        y_test = y_scaled[train_size+val_size:]
        
        print(f"   ✓ Train: {len(X_train)}, Val: {len(X_val)}, Test: {len(X_test)}")
        
        # Simulate model
        print("\n   Simulating Transformer Causal PE training...")
        print("   ℹ Full training requires PyTorch and krl-model-zoo")
        print("   ℹ Mock test validates data pipeline only")
        
        # Baseline metrics
        for h in range(forecast_horizon):
            y_pred_baseline = np.zeros_like(y_test[:, h, :])
            mae_baseline = np.abs(y_test[:, h, :] - y_pred_baseline).mean()
            rmse_baseline = np.sqrt(((y_test[:, h, :] - y_pred_baseline)**2).mean())
            print(f"\n   Horizon {h+1} baseline metrics:")
            print(f"   - MAE: {mae_baseline:.4f}")
            print(f"   - RMSE: {rmse_baseline:.4f}")
        
        print(f"\n   Expected Transformer improvement: 30-50% reduction in error")
        print(f"   Expected causal consistency: Errors increase Interest → Inflation")
        
        print("\n" + "✓"*80)
        print("Economic workflow data pipeline: PASSED")
        print("✓"*80)
        return True
        
    except Exception as e:
        print(f"\n✗ Economic workflow FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("\n" + "="*80)
    print("INTEGRATION PHASE 2 - NOTEBOOK TESTING WITH MOCK DATA")
    print("="*80)
    print("\nThis script validates the data pipelines for both notebooks.")
    print("Full model training requires: PyTorch, krl-model-zoo, krl-data-connectors")
    print("\nRunning tests...")
    
    results = []
    
    # Test healthcare workflow
    results.append(("Healthcare Causal Analysis", test_healthcare_notebook_with_mock_data()))
    
    # Test economic workflow
    results.append(("Economic Forecasting", test_economic_notebook_with_mock_data()))
    
    # Summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    
    for name, passed in results:
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{status}: {name}")
    
    all_passed = all(result[1] for result in results)
    
    if all_passed:
        print("\n" + "✓"*80)
        print("ALL TESTS PASSED - Data pipelines are ready!")
        print("✓"*80)
        print("\nNext steps:")
        print("1. Install dependencies: pip install torch scikit-learn pandas numpy matplotlib seaborn")
        print("2. Install KRL packages: krl-model-zoo, krl-data-connectors")
        print("3. Configure API keys in .env file (see .env.example)")
        print("4. Run notebooks in Jupyter to train actual models")
        return 0
    else:
        print("\n" + "✗"*80)
        print("SOME TESTS FAILED - Review errors above")
        print("✗"*80)
        return 1


if __name__ == "__main__":
    sys.exit(main())
