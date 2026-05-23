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