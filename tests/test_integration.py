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
        f"订单PO-20260522-001物流延迟4小时",
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