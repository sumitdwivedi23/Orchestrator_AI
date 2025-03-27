from typing import TypedDict, Annotated, List
from langchain_core.messages import BaseMessage
from langgraph.graph import add_messages

class ArchitectureState(TypedDict):
    requirements: str
    messages: Annotated[List[BaseMessage], add_messages]
    design_spec: str
    synthesized_plan: str
    iteration_count: int
    max_iterations: int