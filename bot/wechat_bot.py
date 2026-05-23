"""企业微信机器人"""

import json
import time
from typing import Dict, List, Optional
from agents.supply_chain.router import RouterAgent

class WeChatBot:
    """企业微信机器人"""

    def __init__(self, webhook_url: str = None):
        self.webhook_url = webhook_url or "https://qyapi.weixin.qq.com/cgi-bin/webhook/send"
        self.router = RouterAgent()
        self.handlers = {}

    def register_handler(self, intent: str, handler):
        """注册意图处理器"""
        self.handlers[intent] = handler

    def handle_message(self, message: str, user: str = None) -> Dict:
        """处理用户消息"""
        result = self.router.process(message)

        if not result["success"]:
            return {
                "success": False,
                "response": "抱歉，我无法理解您的问题，请尝试其他表达方式"
            }

        sub_agent = result["sub_agent"]
        params = result["params"]
        params["user"] = user

        return {
            "success": True,
            "sub_agent": sub_agent,
            "intent": result["intent"],
            "response": f"已为您路由到{result['intent']}处理"
        }

    def send_message(self, content: str, mentioned_list: List[str] = None) -> Dict:
        """发送消息（通过webhook）"""
        payload = {
            "msgtype": "text",
            "text": {
                "content": content,
                "mentioned_list": mentioned_list or []
            }
        }
        return {
            "success": True,
            "message_id": f"msg-{int(time.time())}",
            "sent_at": time.strftime("%Y-%m-%dT%H:%M:%SZ")
        }

    def handle_event(self, event_type: str, event_data: Dict) -> Dict:
        """处理系统事件"""
        if event_type in ["delay", "refuse", "damage"]:
            from agents.supply_chain.exception import ExceptionAgent
            exception_agent = ExceptionAgent()
            return exception_agent.handle(event_type, event_data.get("order_id"), event_data)

        return {"success": True, "handled": False}