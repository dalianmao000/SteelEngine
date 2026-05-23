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
        result = self.mcp_client.call("inventory_query", {
            "sku": sku,
            "quantity": quantity,
            "warehouses": warehouses
        })
        return result