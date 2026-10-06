# 设计决策（为什么这么选）

1. 前端单文件 index.html，不拆 React/Vue
   → 零构建、双击即跑、便于打包进单 exe。新 agent 不要拆成框架。

2. 后端 Flask + 前端 fetch 轮询（2s），不用 WebSocket
   → 简单够用、无额外依赖。要实时推送再作为独立待办引入。

3. 硬件用 psutil，显存用 pynvml（NVIDIA）
   → 跨平台轻量。AMD/Intel 核显显存读不到，前端显示 N/A 是预期行为，不是 bug。

4. 打包：PyInstaller 单 exe 后端 + Electron portable 前端
   → 目标机不装 Python，双击弹独立窗口。红线：pyinstaller 必须带 --hidden-import pynvml。

5. Agent 指标当前是模拟数据 agent_stats()
   → 有意为之的"先跑通样子"。接手第一件事替换它，但保持返回字段名不变。