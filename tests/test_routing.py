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

    # 1200km * 30吨 * 4元/吨公里 / 1000 = 144
    assert result["routes"][0]["cost"] == 144

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
    assert result["routes"][0]["cost"] < 1440