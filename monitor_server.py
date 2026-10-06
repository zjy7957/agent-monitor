# 依赖: flask psutil nvidia-ml-py
import time, random
from collections import deque
import psutil
from flask import Flask, jsonify, send_file

app = Flask(__name__)
history = deque(maxlen=120)

try:
    import pynvml; pynvml.nvmlInit(); GPU_OK = True
except Exception:
    GPU_OK = False

def gpu_stats():
    if not GPU_OK: return []
    out = []
    for i in range(pynvml.nvmlDeviceGetCount()):
        h = pynvml.nvmlDeviceGetHandleByIndex(i)
        m = pynvml.nvmlDeviceGetMemoryInfo(h)
        u = pynvml.nvmlDeviceGetUtilizationRates(h)
        out.append({"name": pynvml.nvmlDeviceGetName(h),
                    "used_mb": round(m.used/1024/1024),
                    "total_mb": round(m.total/1024/1024),
                    "gpu_util": u.gpu})
    return out

def agent_stats():   # 接真实框架时替换此函数
    return {"agents": 1+random.randint(0,2), "calls": random.randint(20,100),
            "tokens": random.randint(1500,7000), "latency": random.randint(120,500)}

@app.route("/api/stats")
def stats():
    g = gpu_stats(); g0 = g[0] if g else None; a = agent_stats()
    snap = {
        "ts": int(time.time()),
        "cpu": round(psutil.cpu_percent(interval=0.1),1), "cpu_count": psutil.cpu_count(),
        "mem_used": round(psutil.virtual_memory().used/1024/1024),
        "mem_total": round(psutil.virtual_memory().total/1024/1024),
        "mem_pct": psutil.virtual_memory().percent,
        "vram_pct": round(g0["used_mb"]/g0["total_mb"]*100) if g0 else 0,
        "vram_used": g0["used_mb"] if g0 else 0,
        "vram_total": g0["total_mb"] if g0 else 0,
        "gpu_util": g0["gpu_util"] if g0 else 0,
        "gpu_name": g0["name"] if g0 else "N/A",
        **a,
    }
    history.append(snap)
    return jsonify({"current": snap, "history": list(history)})

@app.route("/")
def home(): return send_file("index.html")

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)