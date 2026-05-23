"""Mock TMS物流管理系统"""

from typing import Dict, List, Optional

class MockTMS:
    """模拟TMS系统"""

    def __init__(self):
        self.shipments = {}
        self.routes = {
            ("上海", "广州"): {"distance": 1200, "duration": 20, "cost_per_ton": 4000},
            ("上海", "北京"): {"distance": 1100, "duration": 18, "cost_per_ton": 3600},
            ("上海", "成都"): {"distance": 1800, "duration": 30, "cost_per_ton": 6000},
            ("广州", "北京"): {"distance": 2100, "duration": 35, "cost_per_ton": 7000},
            ("广州", "成都"): {"distance": 1400, "duration": 24, "cost_per_ton": 4800}
        }

    def create_shipment(self, shipment_data: Dict) -> Dict:
        """创建运单"""
        import random
        shipment_id = f"SH-{random.randint(1000, 9999)}"
        self.shipments[shipment_id] = shipment_data
        return {"success": True, "shipment_id": shipment_id}

    def get_shipment(self, shipment_id: str) -> Optional[Dict]:
        """获取运单信息"""
        return self.shipments.get(shipment_id)

    def calculate_route(self, source: str, destination: str, weight: float) -> Dict:
        """计算路线"""
        route_key = (source, destination)
        if route_key not in self.routes:
            distance = 1000
            duration = 20
            cost = distance * weight * 4 / 1000
        else:
            route = self.routes[route_key]
            distance = route["distance"]
            duration = route["duration"]
            cost = route["cost_per_ton"] * weight / 1000

        return {
            "success": True,
            "route": {
                "source": source,
                "destination": destination,
                "distance": distance,
                "duration": duration,
                "cost": int(cost)
            }
        }

    def track(self, shipment_id: str) -> Dict:
        """追踪物流"""
        if shipment_id in self.shipments:
            return {
                "success": True,
                "shipment_id": shipment_id,
                "status": "in_transit",
                "location": "途中",
                "progress": 60
            }
        return {"success": False, "error": "运单不存在"}