# EXACT TEST STEPS

## 1. Open Frontend
Go to: http://localhost:8501

## 2. Enter Patient Info
- **Patient Age:** 35

## 3. Add Drug (Left side)
- **Drug Name:** paracetamol
- **Dosage:** 1500mg  
- **Frequency:** every 4 hours
- **Click "Add Drug"**

## 4. Run Analysis
- **Click "Run Complete Analysis"** (bottom of page)

## 5. Expected Results
You should see:

**Metrics (top):**
- Patient Age: 35
- Drugs Analyzed: 1  
- Interactions Found: 0
- **Overdoses: 1** (with CRITICAL delta)

**OVERDOSE WARNINGS section:**
- **PARACETAMOL**
- **Warning:** OVERDOSE: 9000.0mg/day exceeds 4000mg/day
- **Daily Dose:** 9000.0mg (Max Safe: 4000mg)

**Alternative Medications section:**
- **Ibuprofen:** OVERDOSE DETECTED - Anti-inflammatory effect
- **Dosage:** 200-400mg every 6-8 hours

**Dosage Recommendations section:**
- **Paracetamol:** 500-1000mg every 4-6 hours
- **Warnings:** OVERDOSE: 9000.0mg/day exceeds 4000mg/day
- **REDUCE DOSAGE IMMEDIATELY**

## If Not Working:
1. Refresh the browser page
2. Check if API is running on localhost:8000
3. Try the test again with exact values above