# src/customer_support_hitl_example/utils/test_db_connection.py
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from src.customer_support_hitl_example.database import engine

def test_connection():
    try:
        conn = engine.connect()
        print("Database connection successful!")
        conn.close()
        return True
    except Exception as e:
        print(f"Database connection failed: {e}")
        return False

if __name__ == "__main__":
    test_connection()