from crewai.tools import BaseTool
import chainlit as cl
from chainlit import run_sync

def ask_human(question: str) -> str:
    human_response = run_sync(cl.AskUserMessage(content=f"{question}").send())
    if human_response:
        return human_response["output"]

class HumanInputContextTool(BaseTool):
    name: str = "Ask Human follow up questions to get additonal context"
    description: str = "Use this tool to ask follow-up questions to the human in case additional context is needed"

    def _run(self, question: str) -> str:
        return ask_human(question)
