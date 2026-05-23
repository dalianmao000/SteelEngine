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

## 项目进度

### 已完成 ✅

| 模块 | 功能 | 状态 | 说明 |
|------|------|------|------|
| **Router Agent** | 意图识别、任务路由 | ✅ 完成 | 支持库存/路线/异常/通知/数据5种意图识别 |
| **Inventory Agent** | 仓库库存查询 | ✅ 完成 | Mock模式，支持多仓库联合查询 |
| **Routing Agent** | 物流路线规划 | ✅ 完成 | 支持公路/铁路/水运3种方式 |
| **Exception Agent** | 异常处理 | ✅ 完成 | 支持delay/refuse/damage/missing4种类型 |
| **Notification Agent** | 多渠道通知 | ✅ 完成 | 支持微信/钉钉/邮件 |
| **MCP Server** | Mock API服务 | ✅ 完成 | FastAPI实现，含ERP/WMS/TMS模拟 |
| **WeChat Bot** | 企业微信接入 | ✅ 完成 | 消息处理与事件触发 |
| **测试套件** | 单元/集成测试 | ✅ 完成 | 29个测试用例全部通过 |
| **CI/CD** | GitHub Actions | ✅ 完成 | CI构建 + CodeQL安全扫描 |
| **开源配置** | LICENSE/文档 | ✅ 完成 | MIT协议，英文/中文README |

### 待开发 🔄

| 模块 | 功能 | 优先级 | 说明 |
|------|------|--------|------|
| **Data Agent** | 数据记录与持久化 | P1 | 当前仅为占位模块 |
| **真实系统对接** | ERP/WMS/TMS真实API | P1 | 替换Mock为真实系统 |
| **客户画像** | 客户数据分析 | P2 | 支持精准营销 |
| **价格预测** | AI动态定价 | P2 | 需求预测模型 |
| **智能客服** | 多轮对话能力 | P2 | RAG知识库增强 |
| **风控Agent** | 信用评估/反欺诈 | P2 | 金融场景 |
| **跨境服务** | 多语言/合规审查 | P3 | 国际化支持 |
| **HITL审批** | 人工确认节点 | P2 | 关键决策人工介入 |
| **RAG知识库** | SOP/历史案例 | P2 | 增强Agent能力 |
| **模型路由** | 大小模型自动选择 | P3 | 成本优化 |
| **可视化调试** | LangSmith集成 | P3 | 可观测性增强 |
| **性能监控** | Grafana看板 | P3 | 生产监控 |

### 技术演进路线

| 阶段 | MVP | Core | Scale | Opt |
|------|-----|------|-------|-----|
| 名称 | 单Agent | 多Agent | 全链路 | 智能化 |
| 周期 | 1-2月 | 3-4月 | 5-6月 | 6-12月 |

### 技术演进路线（Mermaid）

```mermaid
flow LR
    A[MVP<br>单Agent] --> B[Core<br>多Agent]
    B --> C[Scale<br>全链路]
    C --> D[Opt<br>智能化]
```

## 贡献

欢迎提交 Issue 和 Pull Request！