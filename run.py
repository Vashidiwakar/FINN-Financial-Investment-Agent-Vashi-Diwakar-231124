"""
FINN Launcher: Starts the FastAPI server and opens the mobile web interface.
Run with: python run.py
"""
import uvicorn
import webbrowser
import threading
import time

def open_browser():
    time.sleep(1.5)
    url = "http://localhost:8000"
    print(f"\n[FINN Agent] Opening mobile prototype in browser: {url}\n")
    try:
        webbrowser.open(url)
    except Exception:
        pass

if __name__ == "__main__":
    print("=" * 60)
    print("  FINN: Financial Investment Agent (ENAM Holdings Challenge)")
    print("  Mobile-First AI Intelligence Layer for Public Markets")
    print("=" * 60)
    threading.Thread(target=open_browser, daemon=True).start()
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
