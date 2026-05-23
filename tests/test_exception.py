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