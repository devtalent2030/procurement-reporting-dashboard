#!/bin/bash

# ==============================================================================
# PROCUREMENT REPORTING PIPELINE AUTOMATION
# ==============================================================================
# Description: Orchestrates the end-to-end data refresh process.
#              1. Generates synthetic procurement data (Bronze Layer)
#              2. Audits data using ML for anomaly detection (Silver Layer)
# Usage:       ./run_pipeline.sh
# Author:      [Your Name]
# ==============================================================================

# 1. SETUP LOGGING
# Define text colors for better readability in the terminal
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}🚀 [START] Initiating Procurement Data Pipeline...${NC}"
echo "--------------------------------------------------------"

# 2. VIRTUAL ENVIRONMENT CHECK
# (Optional: Ensures we are running in the correct Python environment)
# if [[ -z "$VIRTUAL_ENV" ]]; then
#     echo -e "${YELLOW}⚠️  Warning: No virtual environment detected. Ensure dependencies are installed.${NC}"
# fi

# 3. STEP 1: DATA GENERATION
echo -e "${GREEN}📦 [Step 1/2] Generating Mock Data...${NC}"
python scripts/data_generator.py

# Check if the previous command failed (Exit Code != 0)
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ [ERROR] Data generation failed. Aborting pipeline.${NC}"
    exit 1
fi
echo "--------------------------------------------------------"

# 4. STEP 2: ANOMALY DETECTION
echo -e "${GREEN}🤖 [Step 2/2] Running AI Compliance Audit...${NC}"
python scripts/anomaly_detector.py

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ [ERROR] Anomaly detection model failed. Aborting pipeline.${NC}"
    exit 1
fi
echo "--------------------------------------------------------"

# 5. COMPLETION
echo -e "${GREEN}✅ [SUCCESS] Pipeline executed successfully.${NC}"
echo -e "📂 Output Location: ./data/processed/procurement_data_audited.csv"
echo -e "👉 Next Action: Open Power BI and click 'Refresh' to see updates."