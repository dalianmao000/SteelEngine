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
    warehouses_found = [a["warehouse"] for a in result["allocations"]]
    assert "B仓" not in warehouses_found