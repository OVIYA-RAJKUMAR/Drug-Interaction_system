from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict
import re
import json
from datetime import datetime

app = FastAPI(title="Drug Interaction Analysis API")

# Data Models
class DrugInput(BaseModel):
    name: str
    dosage: Optional[str] = None
    frequency: Optional[str] = None

class PatientProfile(BaseModel):
    age: int
    drugs: List[DrugInput]
    medical_conditions: Optional[List[str]] = []

class InteractionResult(BaseModel):
    severity: str
    description: str
    drugs_involved: List[str]

class DosageRecommendation(BaseModel):
    drug_name: str
    recommended_dosage: str
    age_group: str
    warnings: List[str]

class AlternativeDrug(BaseModel):
    name: str
    reason: str
    dosage: str

# Enhanced Drug Database
DRUG_INTERACTIONS = {
    ("warfarin", "aspirin"): {"severity": "HIGH", "description": "Increased bleeding risk"},
    ("paracetamol", "alcohol"): {"severity": "HIGH", "description": "Liver toxicity risk"},
    ("ibuprofen", "aspirin"): {"severity": "MEDIUM", "description": "Increased GI bleeding risk"},
    ("metformin", "alcohol"): {"severity": "MEDIUM", "description": "Risk of lactic acidosis"}
}

AGE_DOSAGE_RULES = {
    "paracetamol": {
        "0-12": "10-15mg/kg every 4-6 hours",
        "13-65": "500-1000mg every 4-6 hours",
        "65+": "500mg every 6-8 hours",
        "max_daily": 4000
    },
    "ibuprofen": {
        "0-12": "5-10mg/kg every 6-8 hours",
        "13-65": "200-400mg every 6-8 hours", 
        "65+": "200mg every 8 hours",
        "max_daily": 1200
    },
    "aspirin": {
        "0-12": "Not recommended",
        "13-65": "75-325mg daily",
        "65+": "75mg daily",
        "max_daily": 325
    }
}

DRUG_ALTERNATIVES = {
    "paracetamol": [{"name": "ibuprofen", "reason": "Anti-inflammatory effect"}],
    "ibuprofen": [{"name": "paracetamol", "reason": "Lower GI risk"}],
    "aspirin": [{"name": "paracetamol", "reason": "Safer for pain relief"}]
}

def get_age_group(age: int) -> str:
    if age <= 12: return "0-12"
    elif age <= 65: return "13-65"
    else: return "65+"

def extract_dosage_amount(dosage_str: str) -> float:
    if not dosage_str:
        return 0
    match = re.search(r'(\d+(?:\.\d+)?)', dosage_str)
    return float(match.group(1)) if match else 0

def check_overdosage(drug_name: str, dosage: str, frequency: str) -> dict:
    drug_name = drug_name.lower()
    if drug_name not in AGE_DOSAGE_RULES:
        return {"is_overdose": False, "warning": ""}
    
    dosage_amount = extract_dosage_amount(dosage)
    max_daily = AGE_DOSAGE_RULES[drug_name].get("max_daily", 0)
    
    if not dosage_amount or not max_daily:
        return {"is_overdose": False, "warning": ""}
    
    daily_doses = 1
    if frequency and "every" in frequency.lower():
        freq_match = re.search(r'every\s*(\d+)\s*hours?', frequency.lower())
        if freq_match:
            hours = int(freq_match.group(1))
            daily_doses = 24 // hours
    
    estimated_daily = dosage_amount * daily_doses
    
    if estimated_daily > max_daily:
        return {
            "is_overdose": True,
            "warning": f"OVERDOSE: {estimated_daily}mg/day exceeds {max_daily}mg/day",
            "estimated_daily": estimated_daily,
            "max_safe": max_daily
        }
    
    return {"is_overdose": False, "warning": ""}

@app.get("/")
async def root():
    return {"message": "Drug Interaction Analysis API"}

@app.post("/analyze-interactions")
async def analyze_interactions(patient: PatientProfile):
    interactions = []
    drug_names = [drug.name.lower() for drug in patient.drugs]
    
    for i, drug1 in enumerate(drug_names):
        for drug2 in drug_names[i+1:]:
            key = tuple(sorted([drug1, drug2]))
            if key in DRUG_INTERACTIONS:
                interaction = DRUG_INTERACTIONS[key]
                interactions.append({
                    "severity": interaction["severity"],
                    "description": interaction["description"],
                    "drugs_involved": [drug1, drug2]
                })
    
    return interactions

@app.post("/dosage-recommendations")
async def get_dosage_recommendations(patient: PatientProfile):
    recommendations = []
    age_group = get_age_group(patient.age)
    
    for drug in patient.drugs:
        drug_name = drug.name.lower()
        if drug_name in AGE_DOSAGE_RULES:
            dosage = AGE_DOSAGE_RULES[drug_name][age_group]
            warnings = []
            
            # Check overdose
            overdose_check = check_overdosage(drug_name, drug.dosage or "", drug.frequency or "")
            if overdose_check["is_overdose"]:
                warnings.append(overdose_check["warning"])
                warnings.append("REDUCE DOSAGE IMMEDIATELY")
            
            if patient.age >= 65:
                warnings.append("Elderly patient - monitor for side effects")
            if patient.age <= 12:
                warnings.append("Pediatric dosing required")
                
            recommendations.append({
                "drug_name": drug_name,
                "recommended_dosage": dosage,
                "age_group": age_group,
                "warnings": warnings
            })
    
    return recommendations

@app.post("/alternative-medications")
async def get_alternatives(patient: PatientProfile):
    alternatives = []
    age_group = get_age_group(patient.age)
    
    for drug in patient.drugs:
        drug_name = drug.name.lower()
        
        # Check overdose
        overdose_check = check_overdosage(drug_name, drug.dosage or "", drug.frequency or "")
        
        if drug_name in DRUG_ALTERNATIVES:
            for alt in DRUG_ALTERNATIVES[drug_name]:
                reason = alt["reason"]
                if overdose_check["is_overdose"]:
                    reason = f"OVERDOSE DETECTED - {reason}"
                
                # Get safe dosage
                alt_name = alt["name"].lower()
                if alt_name in AGE_DOSAGE_RULES:
                    safe_dosage = AGE_DOSAGE_RULES[alt_name][age_group]
                else:
                    safe_dosage = "Consult physician"
                
                alternatives.append({
                    "name": alt["name"],
                    "reason": reason,
                    "dosage": safe_dosage
                })
    
    return alternatives

@app.post("/extract-drugs")
async def extract_drugs_from_text(text: Dict[str, str]):
    medical_text = text.get("text", "")
    drugs = []
    
    # Enhanced patterns
    patterns = [
        r'(\w+)\s+(\d+(?:\.\d+)?)\s*(mg|g)\s+(?:every|q)\s+(\d+)\s+hours?',
        r'(\w+)\s+(\d+(?:\.\d+)?)\s*(mg|g)\s+(?:daily|once daily|bid|tid)',
        r'take\s+(\w+)\s+(\d+(?:\.\d+)?)\s*(mg|g)',
        r'(\w+)\s+(\d+(?:\.\d+)?)\s*(mg|g)'
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, medical_text.lower())
        for match in matches:
            if len(match) >= 3:
                name, dose, unit = match[0], match[1], match[2]
                frequency = "as prescribed"
                if len(match) > 3:
                    frequency = f"every {match[3]} hours"
                
                drugs.append({
                    "name": name,
                    "dosage": f"{dose}{unit}",
                    "frequency": frequency
                })
    
    return drugs

@app.post("/comprehensive-analysis")
async def comprehensive_analysis(patient: PatientProfile):
    interactions = await analyze_interactions(patient)
    dosages = await get_dosage_recommendations(patient)
    alternatives = await get_alternatives(patient)
    
    # Check overdoses
    overdose_warnings = []
    for drug in patient.drugs:
        overdose_check = check_overdosage(drug.name.lower(), drug.dosage or "", drug.frequency or "")
        if overdose_check["is_overdose"]:
            overdose_warnings.append({
                "drug": drug.name,
                "warning": overdose_check["warning"],
                "estimated_daily": overdose_check.get("estimated_daily", 0),
                "max_safe": overdose_check.get("max_safe", 0)
            })
    
    return {
        "patient_age": patient.age,
        "analyzed_drugs": len(patient.drugs),
        "overdose_warnings": overdose_warnings,
        "interactions": interactions,
        "dosage_recommendations": dosages,
        "alternative_medications": alternatives,
        "analysis_timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)