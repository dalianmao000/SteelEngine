# 供应链履约Agent系统实施方案

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 构建供应链履约Agent系统，Router + Sub-Agents架构，企业微信机器人接入，Mock API模拟

**Architecture:** 采用Claude Code原生Agents能力，通过Skill定义每个Agent的prompt模板与工具集，MCP Server连接Mock API，企业微信机器人作为用户交互入口。

**Tech Stack:** Claude Code Agents, Skills, MCP Server, FastAPI (Mock), 企业微信Hook

---

## 一、项目文件结构

```
/Users/yinjili/p48_SteelEngine/
├── docs/
│   └── superpowers/
│       ├── specs/
│       │   └── 2026-05-23-supply-chain-agent-design.md
│       └── plans/
│           └── 2026-05-23-supply-chain-agent-plan.md
├── skills/
│   ├── router_agent/
│   │   └── skill.md
│   ├── inventory_agent/
│   │   └── skill.md
│   ├── routing_agent/
│   │   └── skill.md
│   ├── exception_agent/
│   │   └── skill.md
│   ├── notification_agent/
│   │   └── skill.md
│   └── data_agent/
│       └── skill.md
├── agents/
│   └── supply_chain/
│       ├── __init__.py
│       ├── router.py
│       ├── inventory.py
│       ├── routing.py
│       ├── exception.py
│       ├── notification.py
│       └── data.py
├── mcp_server/
│   ├── __init__.py
│   ├── server.py
│   ├── mock_erp.py
│   ├── mock_wms.py
│   └── mock_tms.py
├── bot/
│   ├── __init__.py
│   └── wechat_bot.py
├── tests/
│   ├── test_router.py
│   ├── test_inventory.py
│   ├── test_routing.py
│   ├── test_exception.py
│   ├── test_notification.py
│   └── test_integration.py
├── skills.md
└── CLAUDE.md
```

---

## 二、任务分解

### Task 1: 项目初始化与目录结构

**Files:**
- Create: `/Users/yinjili/p48_SteelEngine/skills.md`
- Create: `/Users/yinjili/p48_SteelEngine/CLAUDE.md`
- Create: `/Users/yinjili/p48_SteelEngine/agents/__init__.py`
- Create: `/Users/yinjili/p48_SteelEngine/mcp_server/__init__.py`
- Create: `/Users/yinjili/p48_SteelEngine/bot/__init__.py`

- [ ] **Step 1: 创建项目目录结构**

```bash
mkdir -p /Users/yinjili/p48_SteelEngine/{skills/{router_agent,inventory_agent,routing_agent,exception_agent,notification_agent,data_agent},agents/supply_chain,mcp_server,bot,tests}
touch /Users/yinjili/p48_SteelEngine/agents/__init__.py /Users/yinjili/p48_SteelEngine/mcp_server/__init__.py /Users/yinjili/p48_SteelEngine/bot/__init__.py
```

- [ ] **Step 2: 创建 skills.md**

```markdown
# Supply Chain Agent Skills

## Agent Skills

| Skill | Description |
|-------|-------------|
| router_agent | 任务协调与路由 |
| inventory_agent | 库存查询 |
| routing_agent | 路线规划 |
| exception_agent | 异常处理 |
| notification_agent | 通知推送 |
| data_agent | 数据记录 |
```

- [ ] **Step 3: 创建 CLAUDE.md**

```markdown
# Supply Chain Agent System

## Project Overview
- 供应链履约Agent系统
- Router + Sub-Agents 架构
- 企业微信机器人接入

## Architecture
- Router Agent: 任务协调与路由
- Sub-Agents: inventory, routing, exception, notification, data

## Tech Stack
- Claude Code Agents
- MCP Server (FastAPI)
- 企业微信Hook
```

- [ ] **Step 4: 提交**

```bash
git init
git add -A
git commit -m "feat: initialize supply chain agent project structure"
```

---

### Task 2: Router Agent Skill 定义

**Files:**
- Create: `/Users/yinjili/p48_SteelEngine/skills/router_agent/skill.md`
- Create: `/Users/yinjili/p48_SteelEngine/agents/supply_chain/router.py`

- [ ] **Step 1: 创建 router_agent skill.md**

```markdown
# Router Agent Skill

## 角色定义
你是一个供应链履约系统的Router Agent，负责协调整个订单履约流程。

## 核心能力
1. 意图识别：解析用户/系统消息，判断任务类型
2. 任务分发：将任务路由到对应的Sub-Agent
3. 结果聚合：收集Sub-Agent返回结果
4. 流程编排：处理多步骤复杂任务

## 任务类型定义
| task_type | 路由方向 | 描述 |
|-----------|---------|------|
| inventory_query | inventory_agent | 库存查询 |
| route_plan | routing_agent | 路线规划 |
| exception_handle | exception_agent | 异常处理 |
| notification | notification_agent | 通知推送 |
| data_record | data_agent | 数据记录 |

## 输入格式
```json
{
  "message": "用户消息或系统事件",
  "context": {
    "order_id": "订单号",
    "sku": "商品规格",
    "quantity": 数量,
    "source": "来源仓库",
    "destination": "目的地"
  }
}
```

## 输出格式
```json
{
  "intent": "识别到的意图",
  "task_type": "任务类型",
  "sub_agent": "目标Sub-Agent",
  "params": "传递给Sub-Agent的参数",
  "response": "返回给用户的响应"
}
```

## 处理流程
1. 解析输入消息
2. 识别用户意图
3. 确定任务类型
4. 路由到对应Sub-Agent
5. 收集结果并返回
```

- [ ] **Step 2: 创建 router.py**

```python
"""Router Agent - 任务协调与路由"""

class RouterAgent:
    """Router Agent负责意图识别和任务分发"""

    TASK_TYPES = {
        "inventory": "inventory_agent",
        "route": "routing_agent",
        "exception": "exception_agent",
        "notify": "notification_agent",
        "data": "data_agent"
    }

    def __init__(self):
        self.context = {}

    def parse_message(self, message: str) -> dict:
        """解析用户消息，识别意图"""
        message_lower = message.lower()

        if "库存" in message or "查询" in message:
            return {"intent": "库存查询", "task_type": "inventory"}
        elif "路线" in message or "规划" in message or "运费" in message:
            return {"intent": "路线规划", "task_type": "route"}
        elif "异常" in message or "延迟" in message or "问题" in message:
            return {"intent": "异常处理", "task_type": "exception"}
        elif "通知" in message or "提醒" in message:
            return {"intent": "通知推送", "task_type": "notify"}
        elif "记录" in message or "保存" in message:
            return {"intent": "数据记录", "task_type": "data"}
        else:
            return {"intent": "未知", "task_type": None}

    def route(self, task_type: str) -> str:
        """根据任务类型返回目标Agent"""
        return self.TASK_TYPES.get(task_type, None)

    def process(self, message: str, context: dict = None) -> dict:
        """处理消息并路由到对应Sub-Agent"""
        parsed = self.parse_message(message)
        target_agent = self.route(parsed["task_type"])

        return {
            "intent": parsed["intent"],
            "task_type": parsed["task_type"],
            "sub_agent": target_agent,
            "params": context or {},
            "success": target_agent is not None
        }
```

- [ ] **Step 3: 创建测试文件 test_router.py**

```python
"""Router Agent测试"""

import pytest
from agents.supply_chain.router import RouterAgent

def test_parse_inventory_query():
    agent = RouterAgent()
    result = agent.parse_message("查询库存：Q235B 12mm 50吨")
    assert result["intent"] == "库存查询"
    assert result["task_type"] == "inventory"

def test_parse_route_plan():
    agent = RouterAgent()
    result = agent.parse_message("计算运费从上海到广州")
    assert result["intent"] == "路线规划"
    assert result["task_type"] == "route"

def test_parse_exception():
    agent = RouterAgent()
    result = agent.parse_message("订单异常：物流延迟2小时")
    assert result["intent"] == "异常处理"
    assert result["task_type"] == "exception"

def test_route_inventory():
    agent = RouterAgent()
    target = agent.route("inventory")
    assert target == "inventory_agent"

def test_route_unknown():
    agent = RouterAgent()
    target = agent.route("unknown_type")
    assert target is None

def test_process_full_flow():
    agent = RouterAgent()
    result = agent.process("查询库存：Q235B 12mm 50吨")
    assert result["success"] is True
    assert result["sub_agent"] == "inventory_agent"
```

- [ ] **Step 4: 运行测试验证**

```bash
cd /Users/yinjili/p48_SteelEngine
pytest tests/test_router.py -v
```

Expected: PASS (5 tests passed)

- [ ] **Step 5: 提交**

```bash
git add skills/router_agent/skill.md agents/supply_chain/router.py tests/test_router.py
git commit -m "feat: add router agent skill and implementation"
```

---

### Task 3: Inventory Agent (库存查询Sub-Agent)

**Files:**
- Create: `/Users/yinjili/p48_SteelEngine/skills/inventory_agent/skill.md`
- Create: `/Users/yinjili/p48_SteelEngine/agents/supply_chain/inventory.py`
- Test: `/Users/yinjili/p48_SteelEngine/tests/test_inventory.py`

- [ ] **Step 1: 创建 inventory_agent skill.md**

```markdown
# Inventory Agent Skill

## 角色定义
你是一个库存查询专家Agent，负责查询各仓库的库存水位和可用量。

## 核心能力
1. 根据SKU和数量查询库存匹配方案
2. 支持多仓库联合查询
3. 返回最优库存分配建议

## 输入参数
| 参数 | 类型 | 描述 |
|------|------|------|
| sku | string | 商品规格（如：Q235B, 12mm） |
| quantity | int | 需求数量（吨） |
| warehouses | list | 仓库列表（可选，默认全部） |

## 输出格式
```json
{
  "success": true,
  "allocations": [
    {"warehouse": "A仓", "available": 30, "allocated": 30},
    {"warehouse": "B仓", "available": 20, "allocated": 20}
  ],
  "total_available": 50,
  "shortage": 0
}
```

## Mock API
调用 `/api/inventory/query` 接口获取库存数据
```

- [ ] **Step 2: 创建 inventory.py**

```python
"""Inventory Agent - 库存查询"""

class InventoryAgent:
    """库存查询Agent"""

    def __init__(self, mcp_client=None):
        self.mcp_client = mcp_client

    def query(self, sku: str, quantity: int, warehouses: list = None) -> dict:
        """查询库存并返回分配方案"""
        if self.mcp_client:
            return self._query_from_api(sku, quantity, warehouses)
        return self._mock_query(sku, quantity, warehouses)

    def _mock_query(self, sku: str, quantity: int, warehouses: list = None) -> dict:
        """Mock查询 - 模拟库存数据"""
        mock_inventory = {
            "Q235B, 12mm": {
                "A仓": 30,
                "B仓": 0,
                "C仓": 20
            },
            "Q235B, 14mm": {
                "A仓": 15,
                "B仓": 25,
                "C仓": 10
            }
        }

        warehouse_data = mock_inventory.get(sku, {})
        if warehouses:
            warehouse_data = {k: v for k, v in warehouse_data.items() if k in warehouses}

        allocations = []
        remaining = quantity
        total_available = 0

        for warehouse, available in warehouse_data.items():
            if remaining <= 0:
                break
            allocated = min(available, remaining)
            if allocated > 0:
                allocations.append({
                    "warehouse": warehouse,
                    "available": available,
                    "allocated": allocated
                })
                remaining -= allocated
                total_available += available

        return {
            "success": True,
            "allocations": allocations,
            "total_available": total_available,
            "shortage": max(0, quantity - total_available)
        }

    def _query_from_api(self, sku: str, quantity: int, warehouses: list = None) -> dict:
        """从API查询库存"""
        # 调用MCP Server
        result = self.mcp_client.call("inventory_query", {
            "sku": sku,
            "quantity": quantity,
            "warehouses": warehouses
        })
        return result
```

- [ ] **Step 3: 创建测试文件 test_inventory.py**

```python
"""Inventory Agent测试"""

import pytest
from agents.supply_chain.inventory import InventoryAgent

def test_mock_query_sufficient():
    agent = InventoryAgent()
    result = agent.query("Q235B, 12mm", 50)

    assert result["success"] is True
    assert result["shortage"] == 0
    assert len(result["allocations"]) == 2  # A仓30 + C仓20

def test_mock_query_insufficient():
    agent = InventoryAgent()
    result = agent.query("Q235B, 12mm", 100)

    assert result["success"] is True
    assert result["shortage"] == 50  # 100 - 50 available

def test_mock_query_partial():
    agent = InventoryAgent()
    result = agent.query("Q235B, 12mm", 25)

    assert result["success"] is True
    assert result["allocations"][0]["allocated"] == 25
    assert result["allocations"][0]["warehouse"] == "A仓"

def test_filter_warehouses():
    agent = InventoryAgent()
    result = agent.query("Q235B, 12mm", 30, warehouses=["A仓", "B仓"])

    assert result["success"] is True
    # B仓库存为0，不应出现在分配中
    warehouses_found = [a["warehouse"] for a in result["allocations"]]
    assert "B仓" not in warehouses_found
```

- [ ] **Step 4: 运行测试验证**

```bash
cd /Users/yinjili/p48_SteelEngine
pytest tests/test_inventory.py -v
```

Expected: PASS (4 tests passed)

- [ ] **Step 5: 提交**

```bash
git add skills/inventory_agent/skill.md agents/supply_chain/inventory.py tests/test_inventory.py
git commit -m "feat: add inventory agent skill and implementation"
```

---

### Task 4: Routing Agent (路线规划Sub-Agent)

**Files:**
- Create: `/Users/yinjili/p48_SteelEngine/skills/routing_agent/skill.md`
- Create: `/Users/yinjili/p48_SteelEngine/agents/supply_chain/routing.py`
- Test: `/Users/yinjili/p48_SteelEngine/tests/test_routing.py`

- [ ] **Step 1: 创建 routing_agent skill.md**

```markdown
# Routing Agent Skill

## 角色定义
你是一个物流路线规划专家Agent，负责计算最优物流路线、运费和时间。

## 核心能力
1. 根据起止地点计算最优路线
2. 估算运费和运输时间
3. 提供多方案比较

## 输入参数
| 参数 | 类型 | 描述 |
|------|------|------|
| source | string | 起始地 |
| destination | string | 目的地 |
| weight | float | 货物重量（吨） |
| transport_type | string | 运输方式（可选：公路/铁路/水运） |

## 输出格式
```json
{
  "success": true,
  "routes": [
    {
      "route_id": "R001",
      "transport_type": "公路",
      "distance": 1200,
      "duration": 18,
      "cost": 4800,
      "recommend": true
    }
  ],
  "recommended": "R001"
}
```

## Mock API
调用 `/api/routing/calculate` 接口获取路线数据
```

- [ ] **Step 2: 创建 routing.py**

```python
"""Routing Agent - 路线规划"""

class RoutingAgent:
    """路线规划Agent"""

    def __init__(self, mcp_client=None):
        self.mcp_client = mcp_client

    def calculate(self, source: str, destination: str, weight: float, transport_type: str = "公路") -> dict:
        """计算路线方案"""
        if self.mcp_client:
            return self._calculate_from_api(source, destination, weight, transport_type)
        return self._mock_calculate(source, destination, weight, transport_type)

    def _mock_calculate(self, source: str, destination: str, weight: float, transport_type: str = "公路") -> dict:
        """Mock计算 - 模拟路线数据"""
        # 距离估算（简化模型：按城市对）
        distance_map = {
            ("上海", "广州"): 1200,
            ("上海", "北京"): 1100,
            ("上海", "成都"): 1800,
            ("广州", "北京"): 2100,
            ("广州", "成都"): 1400
        }

        distance = distance_map.get((source, destination), 800)

        # 计算运费（公路：4元/吨公里）
        if transport_type == "公路":
            cost_per_km = 4
        elif transport_type == "铁路":
            cost_per_km = 3
        else:  # 水运
            cost_per_km = 2

        distance_cost = distance * weight * cost_per_km / 1000

        # 计算时间（公路：60km/h）
        if transport_type == "公路":
            hours_per_km = 1 / 60
        elif transport_type == "铁路":
            hours_per_km = 1 / 80
        else:
            hours_per_km = 1 / 30

        duration = int(distance * hours_per_km)

        routes = [{
            "route_id": f"{source[0]}{destination[0]}001",
            "transport_type": transport_type,
            "distance": distance,
            "duration": duration,
            "cost": int(distance_cost),
            "recommend": True
        }]

        return {
            "success": True,
            "routes": routes,
            "recommended": routes[0]["route_id"]
        }

    def _calculate_from_api(self, source: str, destination: str, weight: float, transport_type: str) -> dict:
        """从API计算路线"""
        result = self.mcp_client.call("routing_calculate", {
            "source": source,
            "destination": destination,
            "weight": weight,
            "transport_type": transport_type
        })
        return result
```

- [ ] **Step 3: 创建测试文件 test_routing.py**

```python
"""Routing Agent测试"""

import pytest
from agents.supply_chain.routing import RoutingAgent

def test_mock_calculate_highway():
    agent = RoutingAgent()
    result = agent.calculate("上海", "广州", 30, "公路")

    assert result["success"] is True
    assert len(result["routes"]) == 1
    assert result["routes"][0]["transport_type"] == "公路"

def test_mock_calculate_cost():
    agent = RoutingAgent()
    result = agent.calculate("上海", "广州", 30, "公路")

    # 1200km * 30吨 * 4元/吨公里 / 1000 = 1440
    assert result["routes"][0]["cost"] == 1440

def test_mock_calculate_duration():
    agent = RoutingAgent()
    result = agent.calculate("上海", "广州", 30, "公路")

    # 1200km / 60kmh = 20小时
    assert result["routes"][0]["duration"] == 20

def test_rail_transport():
    agent = RoutingAgent()
    result = agent.calculate("上海", "广州", 30, "铁路")

    assert result["success"] is True
    assert result["routes"][0]["transport_type"] == "铁路"
    # 铁路更便宜
    assert result["routes"][0]["cost"] < 1440
```

- [ ] **Step 4: 运行测试验证**

```bash
cd /Users/yinjili/p48_SteelEngine
pytest tests/test_routing.py -v
```

Expected: PASS (4 tests passed)

- [ ] **Step 5: 提交**

```bash
git add skills/routing_agent/skill.md agents/supply_chain/routing.py tests/test_routing.py
git commit -m "feat: add routing agent skill and implementation"
```

---

### Task 5: Exception Agent (异常处理Sub-Agent)

**Files:**
- Create: `/Users/yinjili/p48_SteelEngine/skills/exception_agent/skill.md`
- Create: `/Users/yinjili/p48_SteelEngine/agents/supply_chain/exception.py`
- Test: `/Users/yinjili/p48_SteelEngine/tests/test_exception.py`

- [ ] **Step 1: 创建 exception_agent skill.md**

```markdown
# Exception Agent Skill

## 角色定义
你是一个异常处理专家Agent，负责检测异常、触发重路由、生成处理建议。

## 核心能力
1. 检测物流异常（延迟、拒收、破损）
2. 触发重路由和替代方案
3. 生成处理建议并通知相关方

## 输入参数
| 参数 | 类型 | 描述 |
|------|------|------|
| exception_type | string | 异常类型（delay/refuse/damage） |
| order_id | string | 订单号 |
| details | dict | 异常详情 |

## 输出格式
```json
{
  "success": true,
  "severity": "high",
  "actions": [
    {"action": "reroute", "target": "备用路线"},
    {"action": "notify", "recipients": ["销售", "客户"]}
  ],
  "suggestion": "建议重新规划路线并通知客户"
}
```

## 异常等级定义
- high: 需要立即处理，可能影响交付
- medium: 需要关注，24小时内处理
- low: 记录观察，常规处理
```

- [ ] **Step 2: 创建 exception.py**

```python
"""Exception Agent - 异常处理"""

class ExceptionAgent:
    """异常处理Agent"""

    EXCEPTION_TYPES = {
        "delay": {"severity": "medium", "description": "物流延迟"},
        "refuse": {"severity": "high", "description": "拒收"},
        "damage": {"severity": "high", "description": "货物破损"},
        "missing": {"severity": "high", "description": "货物丢失"}
    }

    def __init__(self, notification_agent=None, routing_agent=None):
        self.notification_agent = notification_agent
        self.routing_agent = routing_agent

    def handle(self, exception_type: str, order_id: str, details: dict = None) -> dict:
        """处理异常并生成处理方案"""
        exception_info = self.EXCEPTION_TYPES.get(exception_type, {"severity": "low", "description": "未知异常"})

        severity = exception_info["severity"]
        description = exception_info["description"]

        # 生成处理动作
        actions = self._generate_actions(exception_type, order_id, details)

        suggestion = self._generate_suggestion(exception_type, severity, details)

        return {
            "success": True,
            "exception_type": exception_type,
            "description": description,
            "severity": severity,
            "order_id": order_id,
            "actions": actions,
            "suggestion": suggestion
        }

    def _generate_actions(self, exception_type: str, order_id: str, details: dict = None) -> list:
        """生成处理动作"""
        actions = []

        if exception_type == "delay":
            actions.append({
                "action": "reroute",
                "target": "备用路线",
                "reason": "原路线延迟"
            })
            actions.append({
                "action": "notify",
                "recipients": ["销售", "客户"],
                "message": f"订单{order_id}物流延迟，请知悉"
            })
        elif exception_type == "refuse":
            actions.append({
                "action": "return",
                "target": "原仓库",
                "reason": "客户拒收"
            })
            actions.append({
                "action": "notify",
                "recipients": ["销售", "客服"],
                "message": f"订单{order_id}被客户拒收，需要处理"
            })
        elif exception_type == "damage":
            actions.append({
                "action": "claim",
                "target": "保险公司",
                "reason": "货物破损"
            })
            actions.append({
                "action": "notify",
                "recipients": ["销售", "客户", "理赔"],
                "message": f"订单{order_id}货物破损，请跟进理赔"
            })
        else:
            actions.append({
                "action": "investigate",
                "target": "物流公司",
                "reason": "异常待查"
            })

        return actions

    def _generate_suggestion(self, exception_type: str, severity: str, details: dict = None) -> str:
        """生成处理建议"""
        if severity == "high":
            return "紧急：建议立即联系客户和物流公司，评估是否需要重新发货或启动理赔流程"
        elif severity == "medium":
            return "建议：24小时内跟进处理，更新客户发货时间，评估是否需要补偿"
        else:
            return "记录：持续观察，纳入日报告"
```

- [ ] **Step 3: 创建测试文件 test_exception.py**

```python
"""Exception Agent测试"""

import pytest
from agents.supply_chain.exception import ExceptionAgent

def test_handle_delay():
    agent = ExceptionAgent()
    result = agent.handle("delay", "PO-20260522-001", {"delay_hours": 4})

    assert result["success"] is True
    assert result["severity"] == "medium"
    assert result["exception_type"] == "delay"
    assert len(result["actions"]) > 0

def test_handle_refuse():
    agent = ExceptionAgent()
    result = agent.handle("refuse", "PO-20260522-002")

    assert result["success"] is True
    assert result["severity"] == "high"
    assert any(a["action"] == "return" for a in result["actions"])

def test_handle_damage():
    agent = ExceptionAgent()
    result = agent.handle("damage", "PO-20260522-003")

    assert result["success"] is True
    assert result["severity"] == "high"
    assert any(a["action"] == "claim" for a in result["actions"])

def test_suggestion_content():
    agent = ExceptionAgent()
    result = agent.handle("refuse", "PO-20260522-004")

    assert "紧急" in result["suggestion"]
```

- [ ] **Step 4: 运行测试验证**

```bash
cd /Users/yinjili/p48_SteelEngine
pytest tests/test_exception.py -v
```

Expected: PASS (4 tests passed)

- [ ] **Step 5: 提交**

```bash
git add skills/exception_agent/skill.md agents/supply_chain/exception.py tests/test_exception.py
git commit -m "feat: add exception agent skill and implementation"
```

---

### Task 6: Notification Agent (通知推送Sub-Agent)

**Files:**
- Create: `/Users/yinjili/p48_SteelEngine/skills/notification_agent/skill.md`
- Create: `/Users/yinjili/p48_SteelEngine/agents/supply_chain/notification.py`
- Test: `/Users/yinjili/p48_SteelEngine/tests/test_notification.py`

- [ ] **Step 1: 创建 notification_agent skill.md**

```markdown
# Notification Agent Skill

## 角色定义
你是一个通知推送专家Agent，负责通过企业微信/钉钉/邮件等渠道发送消息。

## 核心能力
1. 统一消息推送接口
2. 支持多渠道（企业微信/钉钉/邮件）
3. 消息模板管理

## 输入参数
| 参数 | 类型 | 描述 |
|------|------|------|
| recipients | list | 接收人列表 |
| message | string | 消息内容 |
| channel | string | 渠道（wechat/dingtalk/email） |
| template_id | string | 消息模板ID（可选） |

## 输出格式
```json
{
  "success": true,
  "channel": "wechat",
  "recipients": ["张三", "李四"],
  "message_id": "msg-001",
  "sent_at": "2026-05-23T10:00:00Z"
}
```
```

- [ ] **Step 2: 创建 notification.py**

```python
"""Notification Agent - 通知推送"""

import time

class NotificationAgent:
    """通知推送Agent"""

    CHANNELS = ["wechat", "dingtalk", "email"]

    def __init__(self, bot_client=None):
        self.bot_client = bot_client

    def send(self, recipients: list, message: str, channel: str = "wechat", template_id: str = None) -> dict:
        """发送通知"""
        if channel not in self.CHANNELS:
            return {
                "success": False,
                "error": f"Unsupported channel: {channel}"
            }

        if self.bot_client:
            return self._send_via_api(recipients, message, channel)
        return self._mock_send(recipients, message, channel)

    def _mock_send(self, recipients: list, message: str, channel: str) -> dict:
        """Mock发送"""
        return {
            "success": True,
            "channel": channel,
            "recipients": recipients,
            "message": message,
            "message_id": f"msg-{int(time.time())}",
            "sent_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }

    def _send_via_api(self, recipients: list, message: str, channel: str) -> dict:
        """通过API发送"""
        result = self.bot_client.send({
            "recipients": recipients,
            "message": message,
            "channel": channel
        })
        return result

    def build_message(self, template_id: str, params: dict) -> str:
        """根据模板构建消息"""
        templates = {
            "order_delayed": "订单{order_id}物流延迟，预计晚{_delay_hours}小时",
            "order_arrived": "订单{order_id}已到达目的地{location}",
            "payment_received": "客户{client_name}付款已到账，金额{amount}元"
        }

        template = templates.get(template_id, "{message}")
        return template.format(**params)
```

- [ ] **Step 3: 创建测试文件 test_notification.py**

```python
"""Notification Agent测试"""

import pytest
from agents.supply_chain.notification import NotificationAgent

def test_mock_send_wechat():
    agent = NotificationAgent()
    result = agent.send(["张三", "李四"], "订单已发货", "wechat")

    assert result["success"] is True
    assert result["channel"] == "wechat"
    assert result["recipients"] == ["张三", "李四"]
    assert "message_id" in result

def test_mock_send_email():
    agent = NotificationAgent()
    result = agent.send(["admin@example.com"], "系统告警", "email")

    assert result["success"] is True
    assert result["channel"] == "email"

def test_unsupported_channel():
    agent = NotificationAgent()
    result = agent.send(["张三"], "测试", "sms")

    assert result["success"] is False
    assert "error" in result

def test_build_message():
    agent = NotificationAgent()
    message = agent.build_message("order_delayed", {
        "order_id": "PO-001",
        "delay_hours": 4
    })

    assert "PO-001" in message
    assert "4" in message
```

- [ ] **Step 4: 运行测试验证**

```bash
cd /Users/yinjili/p48_SteelEngine
pytest tests/test_notification.py -v
```

Expected: PASS (4 tests passed)

- [ ] **Step 5: 提交**

```bash
git add skills/notification_agent/skill.md agents/supply_chain/notification.py tests/test_notification.py
git commit -m "feat: add notification agent skill and implementation"
```

---

### Task 7: MCP Server (Mock APIs)

**Files:**
- Create: `/Users/yinjili/p48_SteelEngine/mcp_server/server.py`
- Create: `/Users/yinjili/p48_SteelEngine/mcp_server/mock_erp.py`
- Create: `/Users/yinjili/p48_SteelEngine/mcp_server/mock_wms.py`
- Create: `/Users/yinjili/p48_SteelEngine/mcp_server/mock_tms.py`

- [ ] **Step 1: 创建 mock_erp.py**

```python
"""Mock ERP系统"""

from typing import Dict, List, Optional
import random

class MockERP:
    """模拟ERP系统"""

    def __init__(self):
        self.orders = {}
        self.customers = {}

    def get_order(self, order_id: str) -> Optional[Dict]:
        """获取订单信息"""
        if order_id in self.orders:
            return self.orders[order_id]
        # Mock数据
        return {
            "order_id": order_id,
            "customer": "测试客户",
            "sku": "Q235B, 12mm",
            "quantity": 50,
            "status": "pending",
            "created_at": "2026-05-23T10:00:00Z"
        }

    def update_order_status(self, order_id: str, status: str) -> Dict:
        """更新订单状态"""
        if order_id in self.orders:
            self.orders[order_id]["status"] = status
        return {"success": True, "order_id": order_id, "status": status}

    def create_order(self, order_data: Dict) -> Dict:
        """创建订单"""
        order_id = order_data.get("order_id", f"PO-{random.randint(1000, 9999)}")
        self.orders[order_id] = order_data
        return {"success": True, "order_id": order_id}
```

- [ ] **Step 2: 创建 mock_wms.py**

```python
"""Mock WMS仓储管理系统"""

from typing import Dict, List, Optional

class MockWMS:
    """模拟WMS系统"""

    def __init__(self):
        self.inventory = {
            "Q235B, 12mm": {
                "A仓": {"total": 100, "available": 30},
                "B仓": {"total": 80, "available": 0},
                "C仓": {"total": 60, "available": 20}
            },
            "Q235B, 14mm": {
                "A仓": {"total": 50, "available": 15},
                "B仓": {"total": 80, "available": 25},
                "C仓": {"total": 40, "available": 10}
            }
        }
        self.warehouses = ["A仓", "B仓", "C仓"]

    def query_inventory(self, sku: str, warehouses: List[str] = None) -> Dict:
        """查询库存"""
        if warehouses:
            filtered = {k: v for k, v in self.inventory.get(sku, {}).items() if k in warehouses}
        else:
            filtered = self.inventory.get(sku, {})

        result = []
        for warehouse, data in filtered.items():
            result.append({
                "warehouse": warehouse,
                "total": data["total"],
                "available": data["available"]
            })

        return {"success": True, "inventory": result}

    def allocate(self, sku: str, quantity: int, warehouse: str) -> Dict:
        """分配库存"""
        if sku in self.inventory and warehouse in self.inventory[sku]:
            available = self.inventory[sku][warehouse]["available"]
            if available >= quantity:
                self.inventory[sku][warehouse]["available"] -= quantity
                return {"success": True, "allocated": quantity}
        return {"success": False, "error": "库存不足"}

    def get_warehouses(self) -> List[str]:
        """获取仓库列表"""
        return self.warehouses
```

- [ ] **Step 3: 创建 mock_tms.py**

```python
"""Mock TMS物流管理系统"""

from typing import Dict, List, Optional

class MockTMS:
    """模拟TMS系统"""

    def __init__(self):
        self.shipments = {}
        self.routes = {
            ("上海", "广州"): {"distance": 1200, "duration": 20, "cost_per_ton": 4000},
            ("上海", "北京"): {"distance": 1100, "duration": 18, "cost_per_ton": 3600},
            ("上海", "成都"): {"distance": 1800, "duration": 30, "cost_per_ton": 6000},
            ("广州", "北京"): {"distance": 2100, "duration": 35, "cost_per_ton": 7000},
            ("广州", "成都"): {"distance": 1400, "duration": 24, "cost_per_ton": 4800}
        }

    def create_shipment(self, shipment_data: Dict) -> Dict:
        """创建运单"""
        import random
        shipment_id = f"SH-{random.randint(1000, 9999)}"
        self.shipments[shipment_id] = shipment_data
        return {"success": True, "shipment_id": shipment_id}

    def get_shipment(self, shipment_id: str) -> Optional[Dict]:
        """获取运单信息"""
        return self.shipments.get(shipment_id)

    def calculate_route(self, source: str, destination: str, weight: float) -> Dict:
        """计算路线"""
        route_key = (source, destination)
        if route_key not in self.routes:
            # 默认路线
            distance = 1000
            duration = 20
            cost = distance * weight * 4 / 1000
        else:
            route = self.routes[route_key]
            distance = route["distance"]
            duration = route["duration"]
            cost = route["cost_per_ton"] * weight / 1000

        return {
            "success": True,
            "route": {
                "source": source,
                "destination": destination,
                "distance": distance,
                "duration": duration,
                "cost": int(cost)
            }
        }

    def track(self, shipment_id: str) -> Dict:
        """追踪物流"""
        if shipment_id in self.shipments:
            return {
                "success": True,
                "shipment_id": shipment_id,
                "status": "in_transit",
                "location": "途中",
                "progress": 60
            }
        return {"success": False, "error": "运单不存在"}
```

- [ ] **Step 4: 创建 server.py (MCP Server)**

```python
"""MCP Server - Mock API集成服务器"""

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, List, Dict
import uvicorn

from mock_erp import MockERP
from mock_wms import MockWMS
from mock_tms import MockTMS

app = FastAPI(title="Supply Chain MCP Server")

# 初始化Mock系统
erp = MockERP()
wms = MockWMS()
tms = MockTMS()

# 请求模型
class InventoryQuery(BaseModel):
    sku: str
    quantity: int
    warehouses: Optional[List[str]] = None

class RoutingCalculate(BaseModel):
    source: str
    destination: str
    weight: float
    transport_type: str = "公路"

class ShipmentCreate(BaseModel):
    order_id: str
    source: str
    destination: str
    weight: float

# ERP接口
@app.post("/api/erp/order/get")
async def get_order(order_id: str):
    return erp.get_order(order_id)

@app.post("/api/erp/order/update")
async def update_order(order_id: str, status: str):
    return erp.update_order_status(order_id, status)

# WMS接口
@app.post("/api/inventory/query")
async def query_inventory(query: InventoryQuery):
    return wms.query_inventory(query.sku, query.warehouses)

@app.post("/api/inventory/allocate")
async def allocate_inventory(sku: str, quantity: int, warehouse: str):
    return wms.allocate(sku, quantity, warehouse)

# TMS接口
@app.post("/api/routing/calculate")
async def calculate_routing(params: RoutingCalculate):
    return tms.calculate_route(params.source, params.destination, params.weight)

@app.post("/api/shipment/create")
async def create_shipment(data: ShipmentCreate):
    return tms.create_shipment(data.dict())

@app.get("/api/shipment/track/{shipment_id}")
async def track_shipment(shipment_id: str):
    return tms.track(shipment_id)

@app.get("/health")
async def health():
    return {"status": "ok", "service": "supply-chain-mcp"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
```

- [ ] **Step 5: 启动测试MCP Server**

```bash
cd /Users/yinjili/p48_SteelEngine
pip install fastapi uvicorn pydantic
python -m mcp_server.server &
```

Expected: Server running on http://0.0.0.0:8080

- [ ] **Step 6: 测试API端点**

```bash
curl -X POST http://localhost:8080/api/inventory/query \
  -H "Content-Type: application/json" \
  -d '{"sku": "Q235B, 12mm", "quantity": 50}'

curl -X POST http://localhost:8080/api/routing/calculate \
  -H "Content-Type: application/json" \
  -d '{"source": "上海", "destination": "广州", "weight": 30, "transport_type": "公路"}'
```

- [ ] **Step 7: 提交**

```bash
git add mcp_server/
git commit -m "feat: add MCP server with mock ERP/WMS/TMS APIs"
```

---

### Task 8: 企业微信机器人接入

**Files:**
- Create: `/Users/yinjili/p48_SteelEngine/bot/wechat_bot.py`
- Create: `/Users/yinjili/p48_SteelEngine/tests/test_bot.py`

- [ ] **Step 1: 创建 wechat_bot.py**

```python
"""企业微信机器人"""

import json
import time
from typing import Dict, List, Optional
from agents.supply_chain.router import RouterAgent

class WeChatBot:
    """企业微信机器人"""

    def __init__(self, webhook_url: str = None):
        self.webhook_url = webhook_url or "https://qyapi.weixin.qq.com/cgi-bin/webhook/send"
        self.router = RouterAgent()
        self.handlers = {}

    def register_handler(self, intent: str, handler):
        """注册意图处理器"""
        self.handlers[intent] = handler

    def handle_message(self, message: str, user: str = None) -> Dict:
        """处理用户消息"""
        # 路由消息
        result = self.router.process(message)

        if not result["success"]:
            return {
                "success": False,
                "response": "抱歉，我无法理解您的问题，请尝试其他表达方式"
            }

        # 调用对应的Sub-Agent
        sub_agent = result["sub_agent"]
        params = result["params"]
        params["user"] = user

        # 这里应该调用实际的Sub-Agent
        # 简化处理返回路由结果
        return {
            "success": True,
            "sub_agent": sub_agent,
            "intent": result["intent"],
            "response": f"已为您路由到{result['intent']}处理"
        }

    def send_message(self, content: str, mentioned_list: List[str] = None) -> Dict:
        """发送消息（通过webhook）"""
        payload = {
            "msgtype": "text",
            "text": {
                "content": content,
                "mentioned_list": mentioned_list or []
            }
        }
        # Mock发送成功
        return {
            "success": True,
            "message_id": f"msg-{int(time.time())}",
            "sent_at": time.strftime("%Y-%m-%dT%H:%M:%SZ")
        }

    def handle_event(self, event_type: str, event_data: Dict) -> Dict:
        """处理系统事件"""
        # 异常事件自动触发exception_agent
        if event_type in ["delay", "refuse", "damage"]:
            from agents.supply_chain.exception import ExceptionAgent
            exception_agent = ExceptionAgent()
            return exception_agent.handle(event_type, event_data.get("order_id"), event_data)

        return {"success": True, "handled": False}
```

- [ ] **Step 2: 创建测试文件 test_bot.py**

```python
"""WeChat Bot测试"""

import pytest
from bot.wechat_bot import WeChatBot

def test_handle_inventory_query():
    bot = WeChatBot()
    result = bot.handle_message("查询库存：Q235B 12mm 50吨", user="张三")

    assert result["success"] is True
    assert result["sub_agent"] == "inventory_agent"

def test_handle_route_plan():
    bot = WeChatBot()
    result = bot.handle_message("计算运费从上海到广州", user="李四")

    assert result["success"] is True
    assert result["sub_agent"] == "routing_agent"

def test_handle_exception_event():
    bot = WeChatBot()
    result = bot.handle_event("delay", {"order_id": "PO-001", "delay_hours": 4})

    assert result["success"] is True
    assert result["severity"] == "medium"

def test_send_message():
    bot = WeChatBot()
    result = bot.send_message("测试消息", mentioned_list=["张三"])

    assert result["success"] is True
    assert "message_id" in result
```

- [ ] **Step 3: 运行测试验证**

```bash
cd /Users/yinjili/p48_SteelEngine
pytest tests/test_bot.py -v
```

Expected: PASS (4 tests passed)

- [ ] **Step 4: 提交**

```bash
git add bot/wechat_bot.py tests/test_bot.py
git commit -m "feat: add WeChat bot integration"
```

---

### Task 9: 集成测试

**Files:**
- Create: `/Users/yinjili/p48_SteelEngine/tests/test_integration.py`

- [ ] **Step 1: 创建集成测试 test_integration.py**

```python
"""供应链履约Agent系统集成测试"""

import pytest
from agents.supply_chain.router import RouterAgent
from agents.supply_chain.inventory import InventoryAgent
from agents.supply_chain.routing import RoutingAgent
from agents.supply_chain.exception import ExceptionAgent
from agents.supply_chain.notification import NotificationAgent

def test_order_fulfillment_flow():
    """测试订单履约完整流程"""
    # 1. 库存查询
    inventory_agent = InventoryAgent()
    inv_result = inventory_agent.query("Q235B, 12mm", 50)
    assert inv_result["success"] is True
    assert inv_result["shortage"] == 0

    # 2. 路线规划
    routing_agent = RoutingAgent()
    route_result = routing_agent.calculate("上海", "广州", 30, "公路")
    assert route_result["success"] is True
    assert len(route_result["routes"]) == 1

    print(f"库存分配: {inv_result['allocations']}")
    print(f"路线: {route_result['routes'][0]}")

def test_exception_handling_flow():
    """测试异常处理流程"""
    # 1. 异常检测
    exception_agent = ExceptionAgent()
    exc_result = exception_agent.handle("delay", "PO-20260522-001", {"delay_hours": 4})
    assert exc_result["success"] is True
    assert exc_result["severity"] == "medium"

    # 2. 发送通知
    notification_agent = NotificationAgent()
    notif_result = notification_agent.send(
        ["销售", "客户"],
        f"订单{PO-20260522-001}物流延迟4小时",
        "wechat"
    )
    assert notif_result["success"] is True

    print(f"异常处理: {exc_result['suggestion']}")
    print(f"通知状态: {notif_result['message_id']}")

def test_router_integration():
    """测试Router与Sub-Agent集成"""
    router = RouterAgent()
    inventory = InventoryAgent()

    # Router解析消息
    route_result = router.process("查询库存：Q235B 12mm 50吨")
    assert route_result["success"] is True
    assert route_result["sub_agent"] == "inventory_agent"

    # 调用Sub-Agent
    if route_result["sub_agent"] == "inventory_agent":
        inv_result = inventory.query("Q235B, 12mm", 50)
        assert inv_result["success"] is True

    print(f"路由结果: {route_result}")
    print(f"库存结果: {inv_result}")
```

- [ ] **Step 2: 运行集成测试**

```bash
cd /Users/yinjili/p48_SteelEngine
pytest tests/test_integration.py -v
```

Expected: PASS (3 tests passed)

- [ ] **Step 3: 提交**

```bash
git add tests/test_integration.py
git commit -m "test: add integration tests for supply chain agent system"
```

---

### Task 10: 最终验收与文档

**Files:**
- Create: `/Users/yinjili/p48_SteelEngine/README.md`

- [ ] **Step 1: 创建 README.md**

```markdown
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
```

- [ ] **Step 2: 运行全量测试**

```bash
cd /Users/yinjili/p48_SteelEngine
pytest tests/ -v --tb=short
```

Expected: ALL TESTS PASS

- [ ] **Step 3: 最终提交**

```bash
git add -A
git commit -m "feat: complete supply chain agent system v1.0"
git status
```

---

## 实施检查清单

- [ ] Task 1: 项目初始化
- [ ] Task 2: Router Agent
- [ ] Task 3: Inventory Agent
- [ ] Task 4: Routing Agent
- [ ] Task 5: Exception Agent
- [ ] Task 6: Notification Agent
- [ ] Task 7: MCP Server
- [ ] Task 8: WeChat Bot
- [ ] Task 9: 集成测试
- [ ] Task 10: 最终验收

---

*计划完成，等待实施*