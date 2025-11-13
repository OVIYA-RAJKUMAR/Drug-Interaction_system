import subprocess
import time
import os
import signal

# Kill any existing Python processes on port 8000
try:
    subprocess.run(["taskkill", "/f", "/im", "python.exe"], capture_output=True)
    time.sleep(2)
except:
    pass

# Start new API
print("Starting API server...")
subprocess.run(["python", "api/main.py"])