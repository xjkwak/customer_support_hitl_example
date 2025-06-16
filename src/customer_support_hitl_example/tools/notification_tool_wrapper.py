from crewai.tools import BaseTool
from typing import Type, Optional, Union
from pydantic import BaseModel, Field
from .notification_tool import NotificationTool

class NotificationToolInput(BaseModel):
    """Input schema for NotificationTool."""
    ticket_json_path: str = Field(..., description="Path to the ticket JSON file")
    platform: str = Field(default="both", description="Which platform to send to ('slack', 'telegram', or 'both')")
    slack_channel: Optional[str] = Field(None, description="The Slack channel ID or name")
    telegram_chat_id: Optional[Union[int, str]] = Field(None, description="The Telegram chat ID")

class NotificationToolWrapper(BaseTool):
    name: str = "Notification Tool"
    description: str = (
        "A tool to send ticket summaries to Slack and/or Telegram channels. "
        "It takes a path to a JSON file containing ticket information and sends formatted messages."
    )
    args_schema: Type[BaseModel] = NotificationToolInput
    
    def __init__(self):
        super().__init__()
        self._notification_tool = NotificationTool()
    
    def _run(
        self, 
        ticket_json_path: str, 
        platform: str = "both",
        slack_channel: Optional[str] = None,
        telegram_chat_id: Optional[Union[int, str]] = None
    ) -> str:
        result = self._notification_tool.send_ticket_summary(
            ticket_json_path=ticket_json_path,
            platform=platform,
            slack_channel=slack_channel,
            telegram_chat_id=telegram_chat_id
        )
        
        # Format the response
        success_messages = []
        error_messages = []
        
        for platform_name, platform_result in result.items():
            if platform_result.get("success", False):
                success_messages.append(f"Successfully sent message to {platform_name}")
            else:
                error_messages.append(f"Failed to send message to {platform_name}: {platform_result.get('error', 'Unknown error')}")
        
        if success_messages and not error_messages:
            return "Notification sent successfully to all platforms."
        elif success_messages and error_messages:
            return "Partial success: " + "; ".join(success_messages + error_messages)
        else:
            return "Failed to send notifications: " + "; ".join(error_messages)