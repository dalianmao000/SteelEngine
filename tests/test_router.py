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