import json
from typing import Generator, List, Union, Optional, Dict, Any
from dataclasses import dataclass
from enum import Enum

from calute.clients import vInferenceChatCompletionClient, ChatMessage
from calute.clients.vinfrence.types import (
	ChatCompletionRequest,
	ChatCompletionResponse,
	ChatCompletionStreamResponse,
)
from calute.types import Agent, Response, AgentFunction, Result
from calute.utils import function_to_json

__CTX_VARS_NAME__ = "context_variables"
SEP = "  "  # two spaces
add_depth = lambda x: x.replace("\n", f"\n{SEP}")  # noqa


class PromptSection(Enum):
	SYSTEM = "system"
	PERSONA = "persona"
	FUNCTIONS = "functions"
	TOOLS = "tools"
	CONTEXT = "context"
	HISTORY = "history"
	RULES = "rules"
	EXAMPLES = "examples"
	CONSTRAINTS = "constraints"


@dataclass
class PromptTemplate:
	"""Configurable template for structuring agent prompts"""

	sections: Dict[PromptSection, str] = None
	section_order: List[PromptSection] = None

	def __post_init__(self):
		# Default section headers
		self.sections = self.sections or {
			PromptSection.SYSTEM: "You are",
			PromptSection.PERSONA: "Your personality and approach:",
			PromptSection.FUNCTIONS: "Available functions:",
			PromptSection.TOOLS: "Tool usage instructions:",
			PromptSection.CONTEXT: "Current context:",
			PromptSection.HISTORY: "Conversation history:",
			PromptSection.RULES: "Rules you must follow:",
			PromptSection.EXAMPLES: "Example interactions:",
			PromptSection.CONSTRAINTS: "Your constraints:",
		}

		# Default section order
		self.section_order = self.section_order or [
			PromptSection.SYSTEM,
			PromptSection.PERSONA,
			PromptSection.CONSTRAINTS,
			PromptSection.FUNCTIONS,
			PromptSection.TOOLS,
			PromptSection.RULES,
			PromptSection.EXAMPLES,
			PromptSection.CONTEXT,
			PromptSection.HISTORY,
		]


class Calute:
	def __init__(
		self,
		client: vInferenceChatCompletionClient,
		template: Optional[PromptTemplate] = None,
	) -> None:
		self.client = client
		self.template = template or PromptTemplate()

	def format_function_parameters(self, parameters: dict) -> str:
		"""Formats function parameters in a clear, structured way"""
		if not parameters.get("properties"):
			return ""

		formatted_params = []
		required_params = parameters.get("required", [])

		for param_name, param_info in parameters["properties"].items():
			if param_name == "context_variables":
				continue

			param_type = param_info.get("type", "any")
			param_desc = param_info.get("description", "")
			required = "(required)" if param_name in required_params else "(optional)"

			param_str = f"    - {param_name}: {param_type} {required}"
			if param_desc:
				param_str += f"\n      Description: {param_desc}"
			if "enum" in param_info:
				param_str += (
					f"\n      Allowed values: {', '.join(str(v) for v in param_info['enum'])}"
				)

			formatted_params.append(param_str)

		return "\n".join(formatted_params)

	def generate_function_section(self, functions: List[AgentFunction]) -> str:
		"""Generates detailed function documentation with improved formatting"""
		if not functions:
			return ""

		function_docs = []
		for func in functions:
			try:
				schema = function_to_json(func)["function"]

				# Format function header with name and description
				doc = [f"Function: {schema['name']}", f"Purpose: {schema['description']}"]

				# Add parameters section if any exist
				params = self.format_function_parameters(schema["parameters"])
				if params:
					doc.append("Parameters:")
					doc.append(params)

				# Add return type if specified
				if "returns" in schema:
					doc.append(f"Returns: {schema['returns']}")

				function_docs.append("\n".join(doc))

			except Exception as e:
				func_name = getattr(func, "__name__", str(func))
				function_docs.append(f"Warning: Unable to parse function {func_name}: {str(e)}")

		return "\n\n".join(function_docs)

	def format_context_variables(self, variables: Dict[str, Any]) -> str:
		"""Formats context variables with type information and improved readability"""
		if not variables:
			return ""

		formatted_vars = []
		for key, value in variables.items():
			var_type = type(value).__name__
			formatted_value = str(value) if len(str(value)) < 50 else f"{str(value)[:47]}..."
			formatted_vars.append(f"- {key} ({var_type}): {formatted_value}")

		return "\n".join(formatted_vars)

	def format_chat_history(self, history: List[ChatMessage]) -> str:
		"""Formats chat history with improved readability and metadata"""
		if not history:
			return ""

		formatted_messages = []
		for msg in history:
			role_display = {
				"user": "User",
				"assistant": "Assistant",
				"system": "System",
				"tool": "Tool",
			}.get(msg.role, msg.role.capitalize())

			# Add timestamp if available
			timestamp = getattr(msg, "timestamp", "")
			time_str = f" at {timestamp}" if timestamp else ""

			formatted_messages.append(f"{role_display}{time_str}:\n{msg.content}")

		return "\n\n".join(formatted_messages)

	def generate_prompt(
		self,
		agent: Agent,
		context_variables: Optional[dict] = None,
		history: Optional[List[ChatMessage]] = None,
	) -> str:
		"""
		Generates a structured prompt using configurable templates and sections
		"""
		if not agent:
			return "You are a helpful assistant."

		sections = {}

		# System and persona
		if agent.name is not None:
			sections[PromptSection.SYSTEM] = (
				f"{self.template.sections[PromptSection.SYSTEM]} {agent.name}."
			)
		instructions = (
			agent.instructions() if callable(agent.instructions) else agent.instructions
		)
		sections[PromptSection.PERSONA] = instructions

		# Functions and tools
		if agent.functions:
			sections[PromptSection.FUNCTIONS] = self.generate_function_section(
				agent.functions
			)
		if agent.tool_choice:
			tool_text = [
				f"Tool mode: {agent.tool_choice}",
				"Multiple parallel tool calls allowed."
				if agent.parallel_tool_calls
				else "Sequential tool calls required.",
			]
			sections[PromptSection.TOOLS] = "\n".join(tool_text)

		# Context and rules
		if context_variables:
			sections[PromptSection.CONTEXT] = self.format_context_variables(context_variables)
		if agent.rules:
			rules = agent.rules() if callable(agent.rules) else agent.rules
			sections[PromptSection.RULES] = "\n".join(
				f"{SEP}{i+1}. {rule}" for i, rule in enumerate(rules)
			)

		# Examples (if provided)
		if hasattr(agent, "examples") and agent.examples:
			sections[PromptSection.EXAMPLES] = "\n\n".join(agent.examples)

		# History
		if history:
			sections[PromptSection.HISTORY] = self.format_chat_history(history)

		# Build final prompt following template order
		prompt_parts = []
		for section in self.template.section_order:
			if section in sections and sections[section]:
				prompt_parts.append(f"{self.template.sections[section]}\n {sections[section]}")

		return "\n\n".join(prompt_parts)

	def handle_function_result(self, result, debug) -> Result:
		match result:
			case Result() as result:
				return result

			case Agent() as agent:
				return Result(
					value=json.dumps({"assistant": agent.name}),
					agent=agent,
				)
			case _:
				try:
					return Result(value=str(result))
				except Exception as e:
					error_message = f"Failed to cast response to string: {result}. Make sure agent functions return a string or Result object. Error: {str(e)}"
					raise TypeError(error_message) from e

	def handle_tool_calls(
		self,
		tool_calls,
		functions: List[AgentFunction],
		context_variables: dict,
		debug: bool,
	) -> Response:
		function_map = {f.__name__: f for f in functions}
		partial_response = Response(messages=[], agent=None, context_variables={})

		for tool_call in tool_calls:
			name = tool_call.function.name
			# handle missing tool case, skip to next tool
			if name not in function_map:
				partial_response.messages.append(
					{
						"role": "tool",
						"tool_call_id": tool_call.id,
						"tool_name": name,
						"content": f"Error: Tool {name} not found.",
					}
				)
				continue
			args = json.loads(tool_call.function.arguments)

			func = function_map[name]
			if __CTX_VARS_NAME__ in func.__code__.co_varnames:
				args[__CTX_VARS_NAME__] = context_variables
			raw_result = function_map[name](**args)

			result: Result = self.handle_function_result(raw_result, debug)
			partial_response.messages.append(
				{
					"role": "tool",
					"tool_call_id": tool_call.id,
					"tool_name": name,
					"content": result.value,
				}
			)
			partial_response.context_variables.update(result.context_variables)
			if result.agent:
				partial_response.agent = result.agent

		return partial_response

	def create_response(
		self,
		agent: Agent,
		context_variables: Optional[dict] = None,
		history: Optional[List[ChatMessage]] = None,
		*,
		stream: bool = True,
	) -> Generator[
		Union[ChatCompletionStreamResponse, ChatCompletionResponse],
		None,
		None,
	]:
		prompt = self.generate_prompt(
			agent=agent,
			context_variables=context_variables,
			history=history,
		) 
		
		return self.client.create_chat_completion(
			ChatCompletionRequest(
				model=agent.model,
				stream=stream,
				messages=[ChatMessage(role="user", content=prompt)],
			)
		)
