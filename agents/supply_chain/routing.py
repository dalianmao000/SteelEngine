"""Routing Agent - 路线规划"""

class RoutingAgent:
    """路线规划Agent"""

    def __init__(self, mcp_client=None):
        self.mcp_client = mcp_client

    def calculate(self, source: str, destination: str, weight: float, transport_type: str = "公路") -> dict:
        """计算路线方案"""
        if self.mcp_client:
            return self._calculate_from_api(source, destination, weight, transport_type)
        return self._mock_calculate(source, destination, weight, transport_type)

    def _mock_calculate(self, source: str, destination: str, weight: float, transport_type: str = "公路") -> dict:
        """Mock计算 - 模拟路线数据"""
        distance_map = {
            ("上海", "广州"): 1200,
            ("上海", "北京"): 1100,
            ("上海", "成都"): 1800,
            ("广州", "北京"): 2100,
            ("广州", "成都"): 1400
        }

        distance = distance_map.get((source, destination), 800)

        if transport_type == "公路":
            cost_per_km = 4
        elif transport_type == "铁路":
            cost_per_km = 3
        else:
            cost_per_km = 2

        distance_cost = distance * weight * cost_per_km / 1000

        if transport_type == "公路":
            hours_per_km = 1 / 60
        elif transport_type == "铁路":
            hours_per_km = 1 / 80
        else:
            hours_per_km = 1 / 30

        duration = int(distance * hours_per_km)

        routes = [{
            "route_id": f"{source[0]}{destination[0]}001",
            "transport_type": transport_type,
            "distance": distance,
            "duration": duration,
            "cost": int(distance_cost),
            "recommend": True
        }]

        return {
            "success": True,
            "routes": routes,
            "recommended": routes[0]["route_id"]
        }

    def _calculate_from_api(self, source: str, destination: str, weight: float, transport_type: str) -> dict:
        """从API计算路线"""
        result = self.mcp_client.call("routing_calculate", {
            "source": source,
            "destination": destination,
            "weight": weight,
            "transport_type": transport_type
        })
        return result