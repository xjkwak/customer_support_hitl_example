#!/usr/bin/env python3
import os
import json
import argparse
import logging
from pathlib import Path
from datetime import datetime

# Import the notification tool
from customer_support_hitl_example.tools.notification_tool import NotificationTool

# Configure logging
def setup_logging(log_level=logging.INFO, log_file=None):
    """Configure logging for the notification tool tester."""
    # Create a logger
    logger = logging.getLogger("notification_tool_tester")
    logger.setLevel(log_level)

    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Create file handler if log_file is provided
    if log_file:
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger

def create_sample_ticket_json(output_path, logger):
    """Create a sample ticket JSON file for testing."""
    logger.info(f"Creating sample ticket JSON at {output_path}")
    sample_ticket = {
        "ticket_id": "TEST-123",
        "subject": "Test Notification",
        "description": "This is a test ticket created for testing the notification tool.",
        "first_name": "Test",
        "last_name": "User",
        "email": "test@example.com",
        "device_type": "Desktop",
        "browser": "Chrome 120.0",
        "os_version": "macOS 14.0",
        "steps_to_reproduce": "1. Open application\n2. Click on test button\n3. Observe the error",
        "priority": "Medium",
        "status": "New",
        "screenshot_url": "https://example.com/screenshot.png"
    }

    # Ensure directory exists
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    # Save the sample ticket to a JSON file
    with open(output_path, 'w') as f:
        json.dump(sample_ticket, f, indent=2)

    logger.info(f"Sample ticket JSON created successfully")
    return output_path

def test_notification_tool(ticket_json_path, platform, slack_channel=None, telegram_chat_id=None, logger=None):
    """Test the notification tool with the provided parameters."""
    logger.info("Initializing notification tool test")

    # Initialize the notification tool
    notification_tool = NotificationTool()

    # Log current configuration
    logger.info("=== Notification Tool Test Configuration ===")
    logger.info(f"Ticket JSON Path: {ticket_json_path}")
    logger.info(f"Platform: {platform}")
    logger.info(f"Slack Channel: {slack_channel}")
    logger.info(f"Telegram Chat ID: {telegram_chat_id}")
    logger.info(f"Slack Token Configured: {'Yes' if os.environ.get('SLACK_BOT_TOKEN') else 'No'}")
    logger.info(f"Telegram Token Configured: {'Yes' if os.environ.get('TELEGRAM_BOT_TOKEN') else 'No'}")

    # Print for user feedback
    print("\n=== Notification Tool Test Configuration ===")
    print(f"Ticket JSON Path: {ticket_json_path}")
    print(f"Platform: {platform}")
    print(f"Slack Channel: {slack_channel}")
    print(f"Telegram Chat ID: {telegram_chat_id}")
    print(f"Slack Token Configured: {'Yes' if os.environ.get('SLACK_BOT_TOKEN') else 'No'}")
    print(f"Telegram Token Configured: {'Yes' if os.environ.get('TELEGRAM_BOT_TOKEN') else 'No'}")
    print("=" * 50)

    # Check if the ticket JSON file exists
    if not os.path.exists(ticket_json_path):
        error_msg = f"Ticket JSON file not found: {ticket_json_path}"
        logger.error(error_msg)
        print(f"\n✗ {error_msg}")
        return {"error": error_msg}

    # Validate ticket JSON content
    try:
        with open(ticket_json_path, 'r') as f:
            ticket_data = json.load(f)
            logger.debug(f"Ticket data loaded: {json.dumps(ticket_data)}")
    except json.JSONDecodeError as e:
        error_msg = f"Invalid JSON in ticket file: {str(e)}"
        logger.error(error_msg)
        print(f"\n✗ {error_msg}")
        return {"error": error_msg}

    # Validate platform parameter
    if platform not in ["slack", "telegram", "both"]:
        error_msg = f"Invalid platform: {platform}. Must be 'slack', 'telegram', or 'both'"
        logger.error(error_msg)
        print(f"\n✗ {error_msg}")
        return {"error": error_msg}

    # Validate platform-specific parameters
    if platform in ["slack", "both"] and not slack_channel:
        warning_msg = "Slack channel not provided but platform includes Slack"
        logger.warning(warning_msg)
        print(f"\n⚠️ {warning_msg}")

    if platform in ["telegram", "both"] and not telegram_chat_id:
        warning_msg = "Telegram chat ID not provided but platform includes Telegram"
        logger.warning(warning_msg)
        print(f"\n⚠️ {warning_msg}")

    # Send the notification
    try:
        logger.info(f"Sending notification to {platform}")
        results = notification_tool.send_ticket_summary(
            ticket_json_path=ticket_json_path,
            platform=platform,
            slack_channel=slack_channel,
            telegram_chat_id=telegram_chat_id
        )

        # Log and display results
        logger.info("Notification results:")
        print("\n=== Notification Results ===")
        for platform_name, result in results.items():
            if result.get("success", False):
                success_msg = f"{platform_name.capitalize()}: Message sent successfully"
                logger.info(success_msg)
                print(f"✓ {success_msg}")
            else:
                error_msg = f"{platform_name.capitalize()}: Failed - {result.get('error', 'Unknown error')}"
                logger.error(error_msg)
                print(f"✗ {error_msg}")
        print("=" * 50)

        logger.info(f"Notification test completed with results: {results}")
        return results
    except Exception as e:
        error_msg = f"Error during notification: {str(e)}"
        logger.exception(error_msg)
        print(f"\n✗ {error_msg}")
        return {"error": str(e)}

def main():
    """Main function to run the notification tool test."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Test the Notification Tool for Slack and Telegram")
    parser.add_argument("--ticket-path", type=str, help="Path to existing ticket JSON file")
    parser.add_argument("--create-sample", action="store_true", help="Create a sample ticket JSON file")
    parser.add_argument("--output-path", type=str, default="test_ticket.json", help="Path to save the sample ticket JSON")
    parser.add_argument("--platform", type=str, default="both", choices=["slack", "telegram", "both"], help="Platform to send notification to")
    parser.add_argument("--slack-channel", type=str, help="Slack channel to send notification to")
    parser.add_argument("--telegram-chat-id", type=str, help="Telegram chat ID to send notification to")
    parser.add_argument("--log-file", type=str, help="Path to log file")
    parser.add_argument("--log-level", type=str, default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
                        help="Logging level")

    args = parser.parse_args()

    # Set up logging
    log_level = getattr(logging, args.log_level)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = args.log_file or f"logs/notification_test_{timestamp}.log"
    logger = setup_logging(log_level=log_level, log_file=log_file)

    logger.info("Starting notification tool test")
    logger.info(f"Command line arguments: {args}")

    # Determine the ticket JSON path
    ticket_json_path = args.ticket_path
    if args.create_sample or not ticket_json_path:
        ticket_json_path = create_sample_ticket_json(args.output_path, logger)

    # Get environment variables if not provided as arguments
    slack_channel = args.slack_channel or os.environ.get("SLACK_CHANNEL")
    logger.info(f"Using Slack channel: {slack_channel if slack_channel else 'Not configured'}")

    telegram_chat_id = args.telegram_chat_id or os.environ.get("TELEGRAM_CHAT_ID")
    logger.info(f"Using Telegram chat ID: {telegram_chat_id if telegram_chat_id else 'Not configured'}")

    if not slack_channel and args.platform in ["slack", "both"]:
        logger.warning("No Slack channel provided. Using environment variable or will fail.")

    if not telegram_chat_id and args.platform in ["telegram", "both"]:
        logger.warning("No Telegram chat ID provided. Using environment variable or will fail.")

    # Test the notification tool
    test_notification_tool(
        ticket_json_path=ticket_json_path,
        platform=args.platform,
        slack_channel=slack_channel,
        telegram_chat_id=telegram_chat_id,
        logger=logger
    )

    logger.info("Notification tool test completed")

if __name__ == "__main__":
    main()