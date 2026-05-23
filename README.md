# 供应链履约Agent系统

## 项目概述

基于Claude Code原生的供应链履约Agent系统，采用Router + Sub-Agents架构，通过企业微信机器人接入用户。

## 系统架构

```
用户 → 企业微信机器人 → Router Agent → Sub-Agents → MCP Server(Mock API)
```

## Agent组件

| Agent | 职责 |
|-------|------|
| Router Agent | 意图识别、任务路由 |
| Inventory Agent | 库存查询 |
| Routing Agent | 路线规划 |
| Exception Agent | 异常处理 |
| Notification Agent | 通知推送 |

## 快速开始

### 1. 安装依赖
```bash
pip install fastapi uvicorn pydantic pytest
```

### 2. 启动MCP Server
```bash
python -m mcp_server.server
```

### 3. 运行测试
```bash
pytest tests/ -v
```

## 目录结构

```
├── skills/          # Agent Skill定义
├── agents/          # Agent实现
├── mcp_server/      # MCP Server (Mock API)
├── bot/             # 企业微信机器人
└── tests/           # 测试文件
```

## 验收指标

- 任务完成率 ≥ 85%
- 意图识别准确率 ≥ 90%
- 工具调用成功率 ≥ 95%