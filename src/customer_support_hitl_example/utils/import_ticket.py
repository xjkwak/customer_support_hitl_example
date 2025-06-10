# src/customer_support_hitl_example/utils/import_ticket.py
import json
import os
import sys
from pathlib import Path

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from src.customer_support_hitl_example.database import init_db, get_db, Ticket

def import_ticket_from_json(json_file_path):
    """Import ticket data from JSON file into the database."""
    # Initialize the database
    init_db()
    
    # Read the JSON file
    with open(json_file_path, 'r') as file:
        ticket_data = json.load(file)
    
    # Create a new ticket object
    db = get_db()
    try:
        # Check if ticket already exists
        existing_ticket = db.query(Ticket).filter_by(ticket_id=ticket_data["ticket_id"]).first()
        
        if existing_ticket:
            # Update existing ticket
            for key, value in ticket_data.items():
                setattr(existing_ticket, key, value)
            print(f"Updated existing ticket: {ticket_data['ticket_id']}")
        else:
            # Create new ticket
            new_ticket = Ticket(**ticket_data)
            db.add(new_ticket)
            print(f"Created new ticket: {ticket_data['ticket_id']}")
        
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        print(f"Error importing ticket: {e}")
        return False
    finally:
        db.close()

if __name__ == "__main__":
    # Get the path to the ticket.json file
    json_file_path = str(Path(__file__).parent.parent.parent.parent / "ticket.json")
    
    # Import the ticket data
    success = import_ticket_from_json(json_file_path)
    
    if success:
        print("Ticket imported successfully!")
    else:
        print("Failed to import ticket.")