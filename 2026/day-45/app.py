from flask import Flask, jsonify
import psutil
import platform
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({
        "message": "System Stats API is running",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

@app.route("/health")
def health():
    return jsonify({"status": "healthy"}), 200

@app.route("/stats")
def stats():
    return jsonify({
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory": {
            "total_mb": round(psutil.virtual_memory().total / 1024 / 1024, 2),
            "used_mb": round(psutil.virtual_memory().used / 1024 / 1024, 2),
            "percent": psutil.virtual_memory().percent
        },
        "disk": {
            "total_gb": round(psutil.disk_usage('/').total / 1024 / 1024 / 1024, 2),
            "used_gb": round(psutil.disk_usage('/').used / 1024 / 1024 / 1024, 2),
            "percent": psutil.disk_usage('/').percent
        },
        "platform": platform.system(),
        "python_version": platform.python_version()
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


