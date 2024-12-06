from typing import List, Callable, Union, Optional
from pydantic import BaseModel

AgentFunction = Callable[[], Union[str, "Agent", dict]]


class Agent(BaseModel):
	model: str
	name: Optional[str] = None
	instructions: Union[str, Callable[[], str]] = "You are a helpful agent."
	rules: Optional[Union[List[str], Callable[[], List[str]]]] = None
	examples: Optional[List[str]] = None
	functions: List[AgentFunction] = []
	tool_choice: str = None
	parallel_tool_calls: bool = True


class Response(BaseModel):
	messages: List = []
	agent: Optional[Agent] = None
	context_variables: dict = {}


class Result(BaseModel):
	"""
	Encapsulates the possible return values for an agent function.

	Attributes:
	    value (str): The result value as a string.
	    agent (Agent): The agent instance, if applicable.
	    context_variables (dict): A dictionary of context variables.
	"""

	value: str = ""
	agent: Optional[Agent] = None
	context_variables: dict = {}
