"""Router Agent - 任务协调与路由"""

class RouterAgent:
    """Router Agent负责意图识别和任务分发"""

    TASK_TYPES = {
        "inventory": "inventory_agent",
        "route": "routing_agent",
        "exception": "exception_agent",
        "notify": "notification_agent",
        "data": "data_agent"
    }

    def __init__(self):
        self.context = {}

    def parse_message(self, message: str) -> dict:
        """解析用户消息，识别意图"""
        message_lower = message.lower()

        if "库存" in message or "查询" in message:
            return {"intent": "库存查询", "task_type": "inventory"}
        elif "路线" in message or "规划" in message or "运费" in message:
            return {"intent": "路线规划", "task_type": "route"}
        elif "异常" in message or "延迟" in message or "问题" in message:
            return {"intent": "异常处理", "task_type": "exception"}
        elif "通知" in message or "提醒" in message:
            return {"intent": "通知推送", "task_type": "notify"}
        elif "记录" in message or "保存" in message:
            return {"intent": "数据记录", "task_type": "data"}
        else:
            return {"intent": "未知", "task_type": None}

    def route(self, task_type: str) -> str:
        """根据任务类型返回目标Agent"""
        return self.TASK_TYPES.get(task_type, None)

    def process(self, message: str, context: dict = None) -> dict:
        """处理消息并路由到对应Sub-Agent"""
        parsed = self.parse_message(message)
        target_agent = self.route(parsed["task_type"])

        return {
            "intent": parsed["intent"],
            "task_type": parsed["task_type"],
            "sub_agent": target_agent,
            "params": context or {},
            "success": target_agent is not None
        }