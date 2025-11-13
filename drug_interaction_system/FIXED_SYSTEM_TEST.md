# FIXED SYSTEM - WORKING TEST CASES

## Step 1: Restart System
1. Close all terminals (Ctrl+C)
2. Open new terminal
3. Run: `python api/main.py`
4. Open another terminal  
5. Run: `streamlit run frontend/app.py`

## Step 2: Test Overdose Detection

### Go to: http://localhost:8501

**Patient Age:** 35

**Add Drug:**
- Name: `paracetamol`
- Dosage: `1500mg`
- Frequency: `every 4 hours`

**Click "Run Complete Analysis"**

### Expected Results:
- **Overdose Warnings:** 1
- **Warning:** "OVERDOSE: 9000mg/day exceeds 4000mg/day"
- **Alternatives:** Shows ibuprofen as alternative
- **Dosage Recommendations:** Shows "REDUCE DOSAGE IMMEDIATELY"

## Step 3: Test Text Extraction

**Go to "Text Extraction" tab**

**Enter text:**
```
Patient prescribed paracetamol 500mg every 6 hours and ibuprofen 200mg daily
```

**Click "Extract Drug Information"**

### Expected Results:
- Extracts: paracetamol 500mg every 6 hours
- Shows structured drug information

## Step 4: Test Normal Dose

**Patient Age:** 35

**Add Drug:**
- Name: `paracetamol`
- Dosage: `500mg`
- Frequency: `every 6 hours`

### Expected Results:
- **Overdose Warnings:** 0
- **Normal dosage recommendations**
- **No overdose alerts**

## Key Features Now Working:
✅ Overdose detection (1500mg every 4 hours = 9000mg/day > 4000mg limit)
✅ Alternative medications when overdose detected
✅ Dosage recommendations with warnings
✅ Text extraction from medical prescriptions
✅ Age-specific dosing
✅ Drug interaction detection

## If Still Not Working:
1. Restart computer
2. Check Windows Task Manager - kill all python.exe processes
3. Use different port (change 8000 to 8001 in both files)