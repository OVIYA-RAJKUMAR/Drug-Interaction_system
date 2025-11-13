import subprocess
import time
import webbrowser
from threading import Thread

def start_api():
    """Start the FastAPI backend"""
    subprocess.run(["python", "api/main.py"], cwd=".")

def start_frontend():
    """Start the Streamlit frontend"""
    time.sleep(3)  # Wait for API to start
    subprocess.run(["streamlit", "run", "frontend/app.py"], cwd=".")

def main():
    print("🚀 Starting Drug Interaction Analysis System...")
    
    # Start API in background thread
    api_thread = Thread(target=start_api, daemon=True)
    api_thread.start()
    
    print("✅ API starting on http://localhost:8000")
    print("✅ Frontend will start on http://localhost:8501")
    print("\n📖 API Documentation: http://localhost:8000/docs")
    
    # Start frontend (blocking)
    start_frontend()

if __name__ == "__main__":
    main()