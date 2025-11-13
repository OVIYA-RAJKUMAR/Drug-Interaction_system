@echo off
cd /d "c:\Users\OVIYA\OneDrive\ドキュメント\Desktop\data science project\drug_interaction_system"
echo Starting API...
start python api/main.py
timeout /t 3
echo Starting Frontend...
streamlit run frontend/app.py