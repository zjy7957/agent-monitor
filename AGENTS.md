# AGENTS.md — Agent Monitor

## 约定
- 后端 Flask，端口 5000，改端口要同步 main.js 的 PORT
- 前端是单文件 index.html，不要拆框架，保持零构建
- 打包命令固定：pyinstaller --onefile --noconsole --hidden-import pynvml
- 新增指标：在 monitor_server.py 的 snap 字典加字段，前端对应加卡片

## 不要做
- 不要把后端依赖写死成需要目标机装 Python
- 不要删 --hidden-import pynvml，否则显存监控失效
- 不要破坏 agent_stats() 的返回字段名，否则前端要改