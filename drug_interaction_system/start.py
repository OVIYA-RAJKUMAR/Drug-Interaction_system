import subprocess
import time
import sys
import os

def main():
    print("Starting Drug Interaction Analysis System...")
    
    # Start API
    print("Starting API server...")
    api_process = subprocess.Popen([
        sys.executable, "api/main.py"
    ], cwd=os.getcwd())
    
    # Wait for API to start
    time.sleep(3)
    
    # Start Streamlit
    print("Starting Streamlit frontend...")
    print("API: http://localhost:8000")
    print("Frontend: http://localhost:8501")
    
    subprocess.run([
        sys.executable, "-m", "streamlit", "run", "frontend/app.py"
    ], cwd=os.getcwd())

if __name__ == "__main__":
    main()