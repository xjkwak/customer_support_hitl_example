# src/customer_support_hitl_example/tools/db_tool.py
from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
from pathlib import Path
import sys

# Add the project root to the Python path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from src.customer_support_hitl_example.utils.import_ticket import import_ticket_from_json

class SaveTicketInput(BaseModel):
    """Input schema for SaveTicketTool."""
    ticket_path: str = Field(
        default="ticket.json", 
        description="Path to the ticket.json file relative to project root"
    )

class SaveTicketTool(BaseTool):
    name: str = "Save Ticket to Database"
    description: str = (
        "Saves the ticket information from the specified JSON file to the MySQL database. "
        "This tool reads the ticket data from the JSON file and either creates a new ticket "
        "in the database or updates an existing one with the same ticket_id. "
        "Use this tool after the ticket information has been collected and saved to ticket.json."
    )

    args_schema: Type[BaseModel] = SaveTicketInput

    def _run(self, ticket_path: str = "ticket.json") -> str:
        # Get absolute path from relative path
        if not ticket_path.startswith('/'):
            absolute_path = str(project_root / ticket_path)
        else:
            absolute_path = ticket_path
            
        success = import_ticket_from_json(absolute_path)
        
        if success:
            return "Ticket was successfully saved to the database."
        else:
            return "Failed to save ticket to the database. Please check the logs for more information."