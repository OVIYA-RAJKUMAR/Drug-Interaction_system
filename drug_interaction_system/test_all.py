import requests
import json

API_URL = "http://localhost:8000"

def test_overdose():
    print("=== TESTING OVERDOSE DETECTION ===")
    data = {
        "age": 35,
        "drugs": [
            {"name": "paracetamol", "dosage": "1500mg", "frequency": "every 4 hours"}
        ]
    }
    
    response = requests.post(f"{API_URL}/comprehensive-analysis", json=data)
    result = response.json()
    
    print("Overdose Warnings:", len(result.get("overdose_warnings", [])))
    print("Alternatives:", len(result.get("alternative_medications", [])))
    print("Dosage Recs:", len(result.get("dosage_recommendations", [])))
    
    if result.get("overdose_warnings"):
        print("OVERDOSE DETECTED:", result["overdose_warnings"][0]["warning"])
    
    if result.get("alternative_medications"):
        print("ALTERNATIVE:", result["alternative_medications"][0]["name"])
    
    return result

def test_text_extraction():
    print("\n=== TESTING TEXT EXTRACTION ===")
    data = {"text": "Patient prescribed paracetamol 500mg every 6 hours and ibuprofen 200mg daily"}
    
    response = requests.post(f"{API_URL}/extract-drugs", json=data)
    result = response.json()
    
    print("Extracted drugs:", len(result))
    for drug in result:
        print(f"- {drug['name']}: {drug['dosage']} {drug['frequency']}")
    
    return result

def test_normal_dose():
    print("\n=== TESTING NORMAL DOSE ===")
    data = {
        "age": 35,
        "drugs": [
            {"name": "paracetamol", "dosage": "500mg", "frequency": "every 6 hours"}
        ]
    }
    
    response = requests.post(f"{API_URL}/comprehensive-analysis", json=data)
    result = response.json()
    
    print("Overdose Warnings:", len(result.get("overdose_warnings", [])))
    print("Should be 0 for normal dose")
    
    return result

if __name__ == "__main__":
    try:
        test_overdose()
        test_text_extraction()
        test_normal_dose()
        print("\n✅ ALL TESTS COMPLETED")
    except Exception as e:
        print(f"❌ ERROR: {e}")
        print("Make sure API is running: python api/main.py")