"""
FINN Launcher: Starts the FastAPI server and opens the mobile web interface.
Run with: python run.py
"""
import socket
import uvicorn
import webbrowser
import threading
import time

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

def open_browser():
    time.sleep(1.5)
    url = "http://localhost:8000"
    try:
        webbrowser.open(url)
    except Exception:
        pass

if __name__ == "__main__":
    local_ip = get_local_ip()
    print("=" * 65)
    print("  FINN: Financial Investment Agent (ENAM Holdings Challenge)")
    print("  Mobile-First AI Intelligence Layer for Public Markets")
    print("=" * 65)
    print(f"\n  [Local PC]    : http://localhost:8000")
    print(f"  [On Your Phone]: http://{local_ip}:8000 (Connect phone to same Wi-Fi)\n")
    print("=" * 65)
    threading.Thread(target=open_browser, daemon=True).start()
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)

