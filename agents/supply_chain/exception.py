"""Exception Agent - 异常处理"""

class ExceptionAgent:
    """异常处理Agent"""

    EXCEPTION_TYPES = {
        "delay": {"severity": "medium", "description": "物流延迟"},
        "refuse": {"severity": "high", "description": "拒收"},
        "damage": {"severity": "high", "description": "货物破损"},
        "missing": {"severity": "high", "description": "货物丢失"}
    }

    def __init__(self, notification_agent=None, routing_agent=None):
        self.notification_agent = notification_agent
        self.routing_agent = routing_agent

    def handle(self, exception_type: str, order_id: str, details: dict = None) -> dict:
        """处理异常并生成处理方案"""
        exception_info = self.EXCEPTION_TYPES.get(exception_type, {"severity": "low", "description": "未知异常"})

        severity = exception_info["severity"]
        description = exception_info["description"]

        actions = self._generate_actions(exception_type, order_id, details)
        suggestion = self._generate_suggestion(exception_type, severity, details)

        return {
            "success": True,
            "exception_type": exception_type,
            "description": description,
            "severity": severity,
            "order_id": order_id,
            "actions": actions,
            "suggestion": suggestion
        }

    def _generate_actions(self, exception_type: str, order_id: str, details: dict = None) -> list:
        """生成处理动作"""
        actions = []

        if exception_type == "delay":
            actions.append({
                "action": "reroute",
                "target": "备用路线",
                "reason": "原路线延迟"
            })
            actions.append({
                "action": "notify",
                "recipients": ["销售", "客户"],
                "message": f"订单{order_id}物流延迟，请知悉"
            })
        elif exception_type == "refuse":
            actions.append({
                "action": "return",
                "target": "原仓库",
                "reason": "客户拒收"
            })
            actions.append({
                "action": "notify",
                "recipients": ["销售", "客服"],
                "message": f"订单{order_id}被客户拒收，需要处理"
            })
        elif exception_type == "damage":
            actions.append({
                "action": "claim",
                "target": "保险公司",
                "reason": "货物破损"
            })
            actions.append({
                "action": "notify",
                "recipients": ["销售", "客户", "理赔"],
                "message": f"订单{order_id}货物破损，请跟进理赔"
            })
        else:
            actions.append({
                "action": "investigate",
                "target": "物流公司",
                "reason": "异常待查"
            })

        return actions

    def _generate_suggestion(self, exception_type: str, severity: str, details: dict = None) -> str:
        """生成处理建议"""
        if severity == "high":
            return "紧急：建议立即联系客户和物流公司，评估是否需要重新发货或启动理赔流程"
        elif severity == "medium":
            return "建议：24小时内跟进处理，更新客户发货时间，评估是否需要补偿"
        else:
            return "记录：持续观察，纳入日报告"