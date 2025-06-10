from typing import Optional

from pydantic import BaseModel, Field

class CrewInput(BaseModel):
    initial_message: str = Field(..., description="Initial message from the customer")

class TicketInfo(BaseModel):
    ticket_id: str = Field(..., description="The ID of the Zendesk ticket")
    subject: str
    description: str

    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]
    device_type: Optional[str]
    browser: Optional[str]
    os_version: Optional[str]
    screenshot_url: Optional[str]
    steps_to_reproduce: Optional[str]
    priority: Optional[str]
    status: Optional[str] = "pending_review"
