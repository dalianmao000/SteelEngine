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