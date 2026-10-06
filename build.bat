@echo off
pip install flask psutil nvidia-ml-py pyinstaller
pyinstaller --onefile --noconsole --hidden-import pynvml --distpath build --name monitor_server monitor_server.py
npm install
npm run build
echo 产物: release\AgentMonitor.exe