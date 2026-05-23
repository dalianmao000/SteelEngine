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