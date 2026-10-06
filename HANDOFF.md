# 项目交接：Agent Monitor

## 这是什么
独立窗口监控面板：CPU/内存/显存/GPU 利用率 + Agent 调用统计 + 历史曲线。
技术栈：Flask 后端 + Electron 前端 + PyInstaller 打包。

## 当前状态（已完成）
- monitor_server.py：硬件+agent 指标 API（/api/stats）
- index.html：面板 + Chart.js 历史曲线
- main.js / package.json：Electron 独立窗口，portable 单 exe
- build.bat：本地一键打包
- .github/workflows/build.yml：CI 自动出 Windows exe

## 下一步待办（按优先级）
1. 接真实 Agent 指标：替换 monitor_server.py 的 agent_stats() 模拟函数（保持返回字段名不变）
2. 加事件日志 / 调用链面板（新端点 /api/events）
3. 加 GPU 温度、进程级 CPU/内存明细
4. 桌面图标 + 版本号 + 安装包（electron-builder nsis）

## 已知坑
- pynvml 需 --hidden-import 才能打进 exe
- 端口 5000 冲突时改 main.js 的 PORT 与后端一致
- 窗口空白多半是后端没起，先手动跑 build/monitor_server.exe 看报错

## 运行
本地：双击 build.bat → release\AgentMonitor.exe
CI：push 后 Actions → build-exe → Artifacts 下载 exe