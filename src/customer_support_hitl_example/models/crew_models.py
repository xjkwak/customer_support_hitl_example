from typing import Optional

from pydantic import BaseModel, Field

class CrewInput(BaseModel):
    initial_message: str = Field(..., description="Initial message from the customer")

class TicketInfo(BaseModel):
    ticket_id: str = Field(..., description="The ID of the Zendesk ticket")
    subject: str = Field(..., description="Brief summary of the issue")
    description: str = Field(..., description="Detailed explanation of the problem")

    first_name: str = Field(..., description="User's first name")
    last_name: str = Field(..., description="User's last name")
    email: str = Field(..., description="User's email address")
    device_type: str = Field(..., description="Type of device (e.g., laptop, desktop, mobile)")
    browser: str = Field(..., description="Web browser being used (e.g., Chrome, Firefox)")
    os_version: str = Field(..., description="Operating system and version")
    steps_to_reproduce: str = Field(..., description="Steps to recreate the issue")
    priority: str = Field(..., description="How urgent the issue is: low, medium, high")

    # Only these should be optional
    screenshot_url: Optional[str] = Field(None, description="URL to screenshot of the issue")
    status: str = Field("pending_review", description="Current status of the ticket")
