# Drug Interaction Analysis System

A comprehensive system for analyzing drug interactions, providing age-specific dosage recommendations, and suggesting alternative medications.

## Features

1. **Drug Interaction Detection** - Identifies harmful interactions between multiple drugs
2. **Age-Specific Dosage Recommendations** - Provides safe dosages based on patient age
3. **Alternative Medication Suggestions** - Recommends safer alternatives when needed
4. **NLP-Based Drug Extraction** - Extracts drug information from medical text
5. **User-Friendly Interface** - Interactive Streamlit frontend with FastAPI backend

## Quick Start

### Installation
```bash
pip install -r requirements.txt
```

### Run the System
```bash
python run_system.py
```

This will start:
- FastAPI backend on http://localhost:8000
- Streamlit frontend on http://localhost:8501
- API documentation on http://localhost:8000/docs

### Manual Start (Alternative)
```bash
# Terminal 1 - Start API
python api/main.py

# Terminal 2 - Start Frontend
streamlit run frontend/app.py
```

## Usage

1. **Add Drugs**: Enter drug names, dosages, and frequencies
2. **Set Patient Age**: Specify patient age for appropriate recommendations
3. **Analyze Interactions**: Check for harmful drug combinations
4. **Get Dosage Recommendations**: Receive age-appropriate dosing
5. **Find Alternatives**: Discover safer medication options
6. **Extract from Text**: Use NLP to parse medical prescriptions

## API Endpoints

- `POST /analyze-interactions` - Detect drug interactions
- `POST /dosage-recommendations` - Get age-specific dosages
- `POST /alternative-medications` - Find alternative drugs
- `POST /extract-drugs` - Extract drugs from text
- `POST /comprehensive-analysis` - Complete analysis

## System Architecture

```
├── api/
│   └── main.py          # FastAPI backend
├── frontend/
│   └── app.py           # Streamlit interface
├── data/                # Drug databases (expandable)
├── models/              # NLP models (expandable)
├── requirements.txt     # Dependencies
└── run_system.py        # System launcher
```

## Extending the System

- **Add Drug Data**: Expand `DRUG_INTERACTIONS` and `AGE_DOSAGE_RULES` dictionaries
- **Improve NLP**: Integrate advanced models in the `extract_drug_info()` function
- **Add APIs**: Connect to external drug databases (FDA, DrugBank)
- **Enhanced UI**: Add more visualization and reporting features

## Safety Notice

This system is for educational and research purposes. Always consult healthcare professionals for medical decisions.