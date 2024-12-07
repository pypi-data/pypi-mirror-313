import warnings

from squadai.agent import Agent
from squadai.crew import Crew
from squadai.flow.flow import Flow
from squadai.knowledge.knowledge import Knowledge
from squadai.llm import LLM
from squadai.process import Process
from squadai.task import Task

warnings.filterwarnings(
    "ignore",
    message="Pydantic serializer warnings:",
    category=UserWarning,
    module="pydantic.main",
)
__version__ = "0.86.0"
__all__ = [
    "Agent",
    "Crew",
    "Process",
    "Task",
    "LLM",
    "Flow",
    "Knowledge",
]
