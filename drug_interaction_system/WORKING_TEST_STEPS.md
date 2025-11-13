# WORKING OVERDOSE TEST - Step by Step

## Step 1: Stop any running servers
Press Ctrl+C in any terminal running the API

## Step 2: Start fresh API server
```bash
cd "c:\Users\OVIYA\OneDrive\ドキュメント\Desktop\data science project\drug_interaction_system"
python api/main.py
```

## Step 3: Test via API (in new terminal)
```bash
python simple_test.py
```

## Step 4: Test via Frontend
1. Open new terminal
2. Run: `streamlit run frontend/app.py`
3. Go to: http://localhost:8501

## Step 5: Enter OVERDOSE TEST DATA

### In the Streamlit interface:

**Patient Age:** 35

**Add Drug 1:**
- Drug Name: `paracetamol`
- Dosage: `1500mg`
- Frequency: `every 4 hours`
- Click "Add Drug"

**Add Drug 2:**
- Drug Name: `ibuprofen`  
- Dosage: `800mg`
- Frequency: `every 6 hours`
- Click "Add Drug"

## Step 6: Run Analysis
Click "Run Complete Analysis" button

## Expected Results:
```
⚠️ OVERDOSE WARNINGS (2)

🚨 PARACETAMOL
Warning: OVERDOSE WARNING: 9000.0mg/day exceeds maximum safe dose of 4000mg/day
Daily Dose: 9000mg (Max Safe: 4000mg)

🚨 IBUPROFEN  
Warning: OVERDOSE WARNING: 4800.0mg/day exceeds maximum safe dose of 1200mg/day
Daily Dose: 4800mg (Max Safe: 1200mg)

Alternative Medications:
🚨 IBUPROFEN (SAFER ALTERNATIVE)
Reason: OVERDOSE DETECTED - Lower GI risk
Safe Dosage: 200-400mg every 6-8 hours

🚨 DICLOFENAC (SAFER ALTERNATIVE)  
Reason: OVERDOSE DETECTED - Anti-inflammatory effect
Safe Dosage: 200-400mg every 6-8 hours
```

## If Still Not Working:
1. Check API logs for errors
2. Restart computer to clear ports
3. Try different port: Change 8000 to 8001 in both files
4. Check Windows Firewall settings

## Quick Verification:
The debug test shows overdose detection works:
- 1500mg every 4 hours = 9000mg/day (exceeds 4000mg limit) ✅
- Function correctly identifies overdose ✅