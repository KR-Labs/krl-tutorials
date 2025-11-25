#!/bin/bash
# BigQuery Setup for Lean Validation
# Run this script to set up Google Cloud BigQuery access

set -e  # Exit on error

echo "=========================================="
echo "BigQuery Setup for Media Intelligence"
echo "=========================================="
echo ""

# Step 1: Authenticate
echo "Step 1: Authenticating with Google Cloud..."
gcloud auth login

# Step 2: Create project
echo ""
echo "Step 2: Creating Google Cloud project..."
PROJECT_ID="khipu-media-intel-$(date +%s)"
gcloud projects create $PROJECT_ID --name="Khipu Media Intelligence"

# Set as active project
gcloud config set project $PROJECT_ID

echo "✓ Project created: $PROJECT_ID"
echo ""

# Step 3: Enable billing
echo "Step 3: Enable billing"
echo "⚠️  IMPORTANT: You need to link a billing account manually"
echo "    Go to: https://console.cloud.google.com/billing"
echo "    Link your billing account (you should have GCP credits)"
echo ""
read -p "Press ENTER once you've linked billing account..."

# Step 4: Enable APIs
echo ""
echo "Step 4: Enabling BigQuery API..."
gcloud services enable bigquery.googleapis.com
gcloud services enable cloudresourcemanager.googleapis.com

echo "✓ APIs enabled"
echo ""

# Step 5: Create service account
echo "Step 5: Creating service account..."
gcloud iam service-accounts create gdelt-reader \
    --display-name="GDELT BigQuery Reader" \
    --description="Service account for reading GDELT data"

# Grant permissions
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:gdelt-reader@${PROJECT_ID}.iam.gserviceaccount.com" \
    --role="roles/bigquery.user"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:gdelt-reader@${PROJECT_ID}.iam.gserviceaccount.com" \
    --role="roles/bigquery.dataViewer"

echo "✓ Service account created with permissions"
echo ""

# Step 6: Generate credentials
echo "Step 6: Generating credentials..."
mkdir -p ~/khipu-credentials

gcloud iam service-accounts keys create ~/khipu-credentials/gdelt-bigquery.json \
    --iam-account=gdelt-reader@${PROJECT_ID}.iam.gserviceaccount.com

echo "✓ Credentials saved to: ~/khipu-credentials/gdelt-bigquery.json"
echo ""

# Step 7: Set environment variable
echo "Step 7: Setting environment variable..."
export GOOGLE_APPLICATION_CREDENTIALS="$HOME/khipu-credentials/gdelt-bigquery.json"

# Add to shell config
SHELL_CONFIG=""
if [ -f ~/.zshrc ]; then
    SHELL_CONFIG=~/.zshrc
elif [ -f ~/.bashrc ]; then
    SHELL_CONFIG=~/.bashrc
fi

if [ -n "$SHELL_CONFIG" ]; then
    echo "" >> $SHELL_CONFIG
    echo "# Google Cloud credentials for GDELT" >> $SHELL_CONFIG
    echo "export GOOGLE_APPLICATION_CREDENTIALS=\"\$HOME/khipu-credentials/gdelt-bigquery.json\"" >> $SHELL_CONFIG
    echo "✓ Added to $SHELL_CONFIG"
    echo ""
    echo "⚠️  Run: source $SHELL_CONFIG"
fi

# Step 8: Install Python dependencies
echo ""
echo "Step 8: Installing Python dependencies..."
pip install google-cloud-bigquery pandas db-dtypes sentence-transformers scikit-learn --quiet

echo "✓ Python dependencies installed"
echo ""

# Summary
echo "=========================================="
echo "✓ SETUP COMPLETE"
echo "=========================================="
echo ""
echo "Project ID: $PROJECT_ID"
echo "Credentials: ~/khipu-credentials/gdelt-bigquery.json"
echo ""
echo "Next steps:"
echo "1. source $SHELL_CONFIG  # Reload shell config"
echo "2. cd lean_validation"
echo "3. python test_bigquery.py  # Test connection"
echo ""
