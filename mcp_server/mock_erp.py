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