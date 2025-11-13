# Overdosage Detection Test Guide

## How to Test Overdosage Detection

### Step 1: Start the System
```bash
python start.py
```

### Step 2: Go to Frontend
Open: http://localhost:8501

### Step 3: Test These Overdose Cases

#### Test Case 1: Paracetamol Overdose
- **Drug Name**: paracetamol
- **Dosage**: 1500mg (Normal: 500-1000mg)
- **Frequency**: every 4 hours
- **Patient Age**: 35
- **Expected**: Should show OVERDOSE WARNING (9000mg/day > 4000mg max)

#### Test Case 2: Ibuprofen Overdose  
- **Drug Name**: ibuprofen
- **Dosage**: 800mg (Normal: 200-400mg)
- **Frequency**: every 6 hours
- **Patient Age**: 25
- **Expected**: Should show OVERDOSE WARNING (3200mg/day > 1200mg max)

#### Test Case 3: Multiple Overdoses
Add both drugs above together
- **Expected**: Should show 2 overdose warnings + alternatives

### Step 4: Run Comprehensive Analysis
Click "Run Complete Analysis" button

### Expected Results:
1. ⚠️ OVERDOSE WARNINGS section should appear
2. Red error messages showing daily dose exceeds maximum
3. Alternative medications with "OVERDOSE DETECTED" reason
4. Overdose counter in metrics (top right)

### If Not Working:
1. Check API is running on localhost:8000
2. Check browser console for errors
3. Try the test script: `python test_overdose.py`

## Quick Test Commands

### Test via API directly:
```bash
curl -X POST "http://localhost:8000/comprehensive-analysis" \
-H "Content-Type: application/json" \
-d '{
  "age": 35,
  "drugs": [
    {
      "name": "paracetamol",
      "dosage": "1500mg",
      "frequency": "every 4 hours"
    }
  ]
}'
```

### Expected JSON Response:
```json
{
  "overdose_warnings": [
    {
      "drug": "paracetamol",
      "warning": "OVERDOSE WARNING: 9000mg/day exceeds maximum safe dose of 4000mg/day",
      "estimated_daily": 9000,
      "max_safe": 4000
    }
  ]
}
```