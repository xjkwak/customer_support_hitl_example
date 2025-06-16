# src/customer_support_hitl_example/tools/notification_tool.py

import json
import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import telegram
from typing import Optional, Union

class NotificationTool:
    """Tool to send notifications to Slack and Telegram channels."""
    
    def __init__(self):
        # Initialize Slack client if credentials are available
        self.slack_client = None
        if os.environ.get("SLACK_BOT_TOKEN"):
            self.slack_client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))
        
        # Initialize Telegram bot if credentials are available
        self.telegram_bot = None
        if os.environ.get("TELEGRAM_BOT_TOKEN"):
            self.telegram_bot = telegram.Bot(token=os.environ.get("TELEGRAM_BOT_TOKEN"))
    
    def send_to_slack(self, channel: str, message: str) -> dict:
        """
        Send a message to a Slack channel.
        
        Args:
            channel: The Slack channel ID or name to send the message to
            message: The message text to send
            
        Returns:
            A dictionary containing the success status and response/error
        """
        if not self.slack_client:
            return {"success": False, "error": "Slack client not configured. Set SLACK_BOT_TOKEN environment variable."}
        
        try:
            response = self.slack_client.chat_postMessage(
                channel=channel,
                text=message
            )
            return {"success": True, "response": response}
        except SlackApiError as e:
            return {"success": False, "error": str(e)}
    
    def send_to_telegram(self, chat_id: Union[int, str], message: str) -> dict:
        """
        Send a message to a Telegram chat.
        
        Args:
            chat_id: The Telegram chat ID to send the message to
            message: The message text to send
            
        Returns:
            A dictionary containing the success status and response/error
        """
        if not self.telegram_bot:
            return {"success": False, "error": "Telegram bot not configured. Set TELEGRAM_BOT_TOKEN environment variable."}
        
        try:
            response = self.telegram_bot.send_message(
                chat_id=chat_id,
                text=message,
                parse_mode='Markdown'
            )
            return {"success": True, "response": response}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def send_ticket_summary(self, 
                           ticket_json_path: str,
                           platform: str = "both",
                           slack_channel: Optional[str] = None,
                           telegram_chat_id: Optional[Union[int, str]] = None) -> dict:
        """
        Send a ticket summary to the specified platform(s).
        
        Args:
            ticket_json_path: Path to the ticket JSON file
            platform: Which platform to send to ('slack', 'telegram', or 'both')
            slack_channel: The Slack channel ID or name (required if platform includes 'slack')
            telegram_chat_id: The Telegram chat ID (required if platform includes 'telegram')
            
        Returns:
            A dictionary containing the success status and responses/errors
        """
        try:
            with open(ticket_json_path, 'r') as f:
                ticket_data = json.load(f)
                
            # Format the ticket data into a readable message
            message = self._format_ticket_summary(ticket_data)
            
            results = {}
            
            # Send to Slack if requested
            if platform in ["slack", "both"]:
                if not slack_channel:
                    results["slack"] = {"success": False, "error": "Slack channel not provided"}
                else:
                    results["slack"] = self.send_to_slack(slack_channel, message)
            
            # Send to Telegram if requested
            if platform in ["telegram", "both"]:
                if not telegram_chat_id:
                    results["telegram"] = {"success": False, "error": "Telegram chat ID not provided"}
                else:
                    results["telegram"] = self.send_to_telegram(telegram_chat_id, message)
            
            return results
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _format_ticket_summary(self, ticket_data: dict) -> str:
        """
        Format ticket data into a readable message.
        
        Args:
            ticket_data: The ticket data dictionary
            
        Returns:
            A formatted message string
        """
        # Create a formatted message
        message = f"*New Support Ticket:* #{ticket_data['ticket_id']}\n\n"
        message += f"*Subject:* {ticket_data['subject']}\n"
        message += f"*Priority:* {ticket_data.get('priority', 'Not set')}\n"
        message += f"*Status:* {ticket_data.get('status', 'New')}\n\n"
        
        message += f"*Customer:* {ticket_data['first_name']} {ticket_data['last_name']}\n"
        message += f"*Email:* {ticket_data['email']}\n\n"
        
        message += f"*Device:* {ticket_data.get('device_type', 'Not available')}\n"
        message += f"*Browser:* {ticket_data.get('browser', 'Not available')}\n"
        message += f"*OS:* {ticket_data.get('os_version', 'Not available')}\n\n"
        
        message += f"*Description:*\n{ticket_data['description']}\n\n"
        
        if ticket_data.get('steps_to_reproduce'):
            message += f"*Steps to Reproduce:*\n{ticket_data['steps_to_reproduce']}\n"
        
        return message