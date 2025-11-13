import requests

# Test overdose detection directly
data = {
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
    response = requests.post("http://localhost:8000/comprehensive-analysis", json=data)
    result = response.json()
    
    print("Response:", result)
    print("Overdose warnings:", result.get("overdose_warnings", []))
    
except Exception as e:
    print("Error:", e)