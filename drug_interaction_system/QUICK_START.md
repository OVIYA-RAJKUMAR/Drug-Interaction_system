# Quick Start Guide - Drug Interaction System

## To Run After 20 Days:

### Method 1: Double-click the batch file
- Double-click `run_drug_system.bat`

### Method 2: Command line
```bash
cd "c:\Users\OVIYA\OneDrive\ドキュメント\Desktop\data science project\drug_interaction_system"
python start.py
```

### Method 3: Individual components
```bash
# Terminal 1 - API
python api/main.py

# Terminal 2 - Frontend  
streamlit run frontend/app.py
```

## Access URLs:
- **Frontend**: http://localhost:8501
- **API Docs**: http://localhost:8000/docs

## System Features:
1. Add drugs and patient age
2. Check drug interactions
3. Get dosage recommendations
4. Find alternative medications
5. Extract drugs from medical text

## Troubleshooting:
- If ports are busy, restart your computer
- Ensure Python and packages are still installed
- Re-run: `pip install fastapi uvicorn streamlit requests python-multipart`