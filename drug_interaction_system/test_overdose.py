import requests
import json

# Test overdosage detection
def test_overdose():
    url = "http://localhost:8000/comprehensive-analysis"
    
    # Test case with overdosage
    test_data = {
        "age": 35,
        "drugs": [
            {
                "name": "paracetamol",
                "dosage": "1500mg",  # OVERDOSE: Normal is 500-1000mg
                "frequency": "every 4 hours"  # This gives 9000mg/day (max is 4000mg)
            },
            {
                "name": "ibuprofen", 
                "dosage": "800mg",   # OVERDOSE: Normal is 200-400mg
                "frequency": "every 6 hours"  # This gives 3200mg/day (max is 1200mg)
            }
        ],
        "medical_conditions": []
    }
    
    try:
        response = requests.post(url, json=test_data)
        result = response.json()
        
        print("=== OVERDOSE TEST RESULTS ===")
        print(f"Patient Age: {result['patient_age']}")
        print(f"Drugs Analyzed: {result['analyzed_drugs']}")
        
        if result.get('overdose_warnings'):
            print(f"\n🚨 OVERDOSE WARNINGS FOUND: {len(result['overdose_warnings'])}")
            for warning in result['overdose_warnings']:
                print(f"- Drug: {warning['drug']}")
                print(f"- Warning: {warning['warning']}")
                print(f"- Daily Dose: {warning['estimated_daily']}mg")
                print(f"- Max Safe: {warning['max_safe']}mg")
                print()
        else:
            print("\n❌ NO OVERDOSE WARNINGS DETECTED (This is a problem!)")
        
        if result.get('alternative_medications'):
            print("🔄 ALTERNATIVES SUGGESTED:")
            for alt in result['alternative_medications']:
                print(f"- {alt['name']}: {alt['reason']}")
                print(f"  Safe dosage: {alt['dosage']}")
        
        return result
        
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    print("Testing overdosage detection...")
    print("Make sure the API is running on localhost:8000")
    print()
    test_overdose()