import requests
import json

def test_overdose():
    url = "http://localhost:8000/comprehensive-analysis"
    
    # Test case with overdosage
    test_data = {
        "age": 35,
        "drugs": [
            {
                "name": "paracetamol",
                "dosage": "1500mg",
                "frequency": "every 4 hours"
            }
        ]
    }
    
    try:
        response = requests.post(url, json=test_data)
        result = response.json()
        
        print("OVERDOSE TEST RESULTS")
        print("Patient Age:", result['patient_age'])
        print("Drugs Analyzed:", result['analyzed_drugs'])
        
        if result.get('overdose_warnings'):
            print("OVERDOSE WARNINGS FOUND:", len(result['overdose_warnings']))
            for warning in result['overdose_warnings']:
                print("Drug:", warning['drug'])
                print("Warning:", warning['warning'])
                print("Daily Dose:", warning['estimated_daily'], "mg")
                print("Max Safe:", warning['max_safe'], "mg")
                print()
        else:
            print("NO OVERDOSE WARNINGS - Check the code!")
        
        if result.get('alternative_medications'):
            print("ALTERNATIVES:")
            for alt in result['alternative_medications']:
                print("-", alt['name'], ":", alt['reason'])
        
        return True
        
    except Exception as e:
        print("Error:", str(e))
        return False

if __name__ == "__main__":
    test_overdose()