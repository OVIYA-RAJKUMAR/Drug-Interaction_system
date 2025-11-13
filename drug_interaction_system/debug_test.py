import re

def extract_dosage_amount(dosage_str: str) -> float:
    """Extract numeric dosage amount"""
    if not dosage_str:
        return 0
    match = re.search(r'(\d+(?:\.\d+)?)', dosage_str)
    return float(match.group(1)) if match else 0

def check_overdosage(drug_name: str, dosage: str, frequency: str) -> dict:
    """Check if dosage exceeds safe limits"""
    AGE_DOSAGE_RULES = {
        "paracetamol": {
            "max_daily": 4000
        },
        "ibuprofen": {
            "max_daily": 1200
        }
    }
    
    drug_name = drug_name.lower()
    print(f"Checking drug: {drug_name}")
    print(f"Dosage: {dosage}")
    print(f"Frequency: {frequency}")
    
    if drug_name not in AGE_DOSAGE_RULES:
        print(f"Drug {drug_name} not in rules")
        return {"is_overdose": False, "warning": ""}
    
    dosage_amount = extract_dosage_amount(dosage)
    print(f"Extracted dosage amount: {dosage_amount}")
    
    max_daily = AGE_DOSAGE_RULES[drug_name].get("max_daily", 0)
    print(f"Max daily: {max_daily}")
    
    if not dosage_amount or not max_daily:
        print("Missing dosage or max daily")
        return {"is_overdose": False, "warning": ""}
    
    # Estimate daily dose based on frequency
    daily_doses = 1
    if "every" in frequency.lower():
        freq_match = re.search(r'every\s*(\d+)\s*hours?', frequency.lower())
        if freq_match:
            hours = int(freq_match.group(1))
            daily_doses = 24 // hours
            print(f"Found frequency: every {hours} hours = {daily_doses} doses per day")
    
    estimated_daily = dosage_amount * daily_doses
    print(f"Estimated daily: {estimated_daily}mg")
    
    if estimated_daily > max_daily:
        print("OVERDOSE DETECTED!")
        return {
            "is_overdose": True,
            "warning": f"OVERDOSE WARNING: {estimated_daily}mg/day exceeds maximum safe dose of {max_daily}mg/day",
            "estimated_daily": estimated_daily,
            "max_safe": max_daily
        }
    
    print("No overdose")
    return {"is_overdose": False, "warning": ""}

# Test the function
print("=== TESTING OVERDOSE DETECTION ===")
result = check_overdosage("paracetamol", "1500mg", "every 4 hours")
print("Result:", result)
print()

print("=== TESTING NORMAL DOSE ===")
result2 = check_overdosage("paracetamol", "500mg", "every 6 hours")
print("Result:", result2)