# 供应链履约Agent系统

基于 Claude Code 原生的生产级 AI Agent 系统，采用 Router + Sub-Agents 架构。

## 简介

本项目实现了一套用于供应链管理的 **Router + Sub-Agents** 架构智能系统，具有以下功能：

- **意图识别**：自动将用户消息路由到合适的 Agent
- **库存管理**：实时仓库库存查询与分配
- **路线规划**：物流成本与时间优化
- **异常处理**：自动化异常检测与处理
- **通知系统**：多渠道告警（微信/邮件/钉钉）

## 架构

```
用户 → 企业微信机器人 → Router Agent → Sub-Agents → MCP Server (Mock APIs)
```

### Agent 组件

| Agent | 职责 |
|-------|------|
| Router Agent | 意图识别、任务路由 |
| Inventory Agent | 仓库库存查询 |
| Routing Agent | 物流路线规划 |
| Exception Agent | 异常处理 |
| Notification Agent | 多渠道通知 |

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 运行测试

```bash
export PYTHONPATH=/path/to/project
pytest tests/ -v
```

### 3. 启动 MCP Server

```bash
python -m mcp_server.server
# 服务运行在 http://0.0.0.0:8080
```

### 4. 测试 API 接口

```bash
# 查询库存
curl -X POST http://localhost:8080/api/inventory/query \
  -H "Content-Type: application/json" \
  -d '{"sku": "Q235B, 12mm", "quantity": 50}'

# 计算路线
curl -X POST http://localhost:8080/api/routing/calculate \
  -H "Content-Type: application/json" \
  -d '{"source": "Shanghai", "destination": "Guangzhou", "weight": 30}'
```

## 项目结构

```
.
├── skills/              # Agent 技能定义
├── agents/              # Agent 实现
│   └── supply_chain/    # 供应链领域 Agents
├── mcp_server/          # MCP Server (Mock APIs)
│   ├── server.py        # FastAPI 服务
│   ├── mock_erp.py      # Mock ERP 系统
│   ├── mock_wms.py      # Mock WMS 系统
│   └── mock_tms.py      # Mock TMS 系统
├── bot/                 # 企业微信机器人集成
├── tests/               # 测试套件
├── docs/                # 文档
├── README.md
├── README_zh.md
├── LICENSE
└── pyproject.toml
```

## 开发

### 运行全部测试

```bash
PYTHONPATH=. pytest tests/ -v
```

### 添加新 Agent

1. 在 `skills/<agent_name>/skill.md` 创建技能定义
2. 在 `agents/supply_chain/<agent_name>.py` 实现 Agent
3. 在 `tests/test_<agent_name>.py` 添加测试
4. 在 Router Agent 中注册路由

## 测试

```bash
# 单元测试
pytest tests/test_router.py -v

# 集成测试
pytest tests/test_integration.py -v

# 全部测试
pytest tests/ -v --tb=short
```

## 验收指标

- 任务完成率 ≥ 85%
- 意图识别准确率 ≥ 90%
- 工具调用成功率 ≥ 95%

## 许可证

MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。

## 联系方式

GitHub: [dalianmao000/SteelEngine](https://github.com/dalianmao000/SteelEngine)

## 贡献

欢迎提交 Issue 和 Pull Request！