"""Notification Agent - 通知推送"""

import time

class NotificationAgent:
    """通知推送Agent"""

    CHANNELS = ["wechat", "dingtalk", "email"]

    def __init__(self, bot_client=None):
        self.bot_client = bot_client

    def send(self, recipients: list, message: str, channel: str = "wechat", template_id: str = None) -> dict:
        """发送通知"""
        if channel not in self.CHANNELS:
            return {
                "success": False,
                "error": f"Unsupported channel: {channel}"
            }

        if self.bot_client:
            return self._send_via_api(recipients, message, channel)
        return self._mock_send(recipients, message, channel)

    def _mock_send(self, recipients: list, message: str, channel: str) -> dict:
        """Mock发送"""
        return {
            "success": True,
            "channel": channel,
            "recipients": recipients,
            "message": message,
            "message_id": f"msg-{int(time.time())}",
            "sent_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }

    def _send_via_api(self, recipients: list, message: str, channel: str) -> dict:
        """通过API发送"""
        result = self.bot_client.send({
            "recipients": recipients,
            "message": message,
            "channel": channel
        })
        return result

    def build_message(self, template_id: str, params: dict) -> str:
        """根据模板构建消息"""
        templates = {
            "order_delayed": "订单{order_id}物流延迟，预计晚{delay_hours}小时",
            "order_arrived": "订单{order_id}已到达目的地{location}",
            "payment_received": "客户{client_name}付款已到账，金额{amount}元"
        }

        template = templates.get(template_id, "{message}")
        return template.format(**params)