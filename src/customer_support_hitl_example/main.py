#!/usr/bin/env python
import asyncio
import sys
import warnings
import logging
from datetime import datetime

import chainlit as cl
from dotenv import load_dotenv

from customer_support_hitl_example.crew import CustomerSupportHitlExample
from customer_support_hitl_example.models import CrewInput

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

load_dotenv(override=True)
warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    inputs = {
        'topic': 'AI LLMs',
        'current_year': str(datetime.now().year)
    }
    
    try:
        CustomerSupportHitlExample().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        CustomerSupportHitlExample().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        CustomerSupportHitlExample().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        CustomerSupportHitlExample().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")


my_crew = CustomerSupportHitlExample().crew()

@cl.on_chat_start
async def on_chat_start():
    logger.info("Starting new chat session")
    await cl.Message(content="Hello I am your personal Assistant. How can I help?").send()


@cl.on_message
async def on_message(message: cl.Message):
    # This function will be called when user sends their first and subsequent messages
    logger.info(f"Received message from user: {message.content[:50]}...")

    try:
        input_data = CrewInput(initial_message=message.content)
        logger.info(f"Created CrewInput object with message content: {input_data.initial_message}")

        logger.info("Starting crew.kickoff in separate thread")
        result = await asyncio.to_thread(lambda: my_crew.kickoff(inputs=input_data.model_dump()))
        logger.info(f"Received result from crew: {str(result)[:50]}...")

        await cl.Message(content=str(result)).send()
        logger.info("Sent response back to user")
    except Exception as e:
        error_msg = f"Error processing message: {str(e)}"
        logger.error(error_msg, exc_info=True)
        await cl.Message(content=f"Sorry, an error occurred: {str(e)}").send()
