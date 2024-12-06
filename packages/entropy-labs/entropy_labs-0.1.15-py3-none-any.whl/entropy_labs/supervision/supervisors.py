from typing import Callable, Optional, Protocol, Any
from .config import (
    SupervisionDecision,
    SupervisionDecisionType,
    SupervisionContext,
    PREFERRED_LLM_MODEL,
    ModifiedData,
)
import inspect
import json
from openai import OpenAI
from inspect_ai.tool import ToolCall
from entropy_labs.sentinel_api_client.sentinel_api_client.client import Client
from uuid import UUID

client = OpenAI()

class Supervisor(Protocol):
    """
    Protocol for supervisor functions.
    Defines the expected signature for supervisor callables.
    """

    def __call__(
        self,
        func: Callable,
        supervision_context: SupervisionContext,
        ignored_attributes: list[str],
        tool_args: list[Any],
        tool_kwargs: dict[str, Any],
        supervision_request_id: Optional[UUID],
        decision: Optional[SupervisionDecision] = None,
        **kwargs
    ) -> SupervisionDecision:
        """
        Makes a decision based on the function, its arguments,
        and the supervision context.

        Args:
            func (Callable): The function being supervised.
            supervision_context (SupervisionContext): Additional context.
            ignored_attributes (List[str]): Attributes to ignore.
            tool_args (List[Any]): Positional arguments for the function.
            tool_kwargs (dict[str, Any]): Keyword arguments for the function.
            supervision_request_id (Optional[UUID]): ID of the supervision request.
            decision (Optional[SupervisionDecision]): Decision made by the previous supervisor that escalated to this Supervisor.
        Returns:
            SupervisionDecision: The decision made by the supervisor.
        """
        ...

DEFAULT_SYSTEM_PROMPT = (
    "You are an AI safety reviewer. Your task is to evaluate the following function call "
    "and decide whether it should be approved, rejected, escalated, terminated, or modified. "
    "Provide your decision along with an explanation."
)

def llm_supervisor(
    instructions: str,
    supervisor_name: Optional[str] = None,
    description: Optional[str] = None,
    openai_model: str = PREFERRED_LLM_MODEL,
    system_prompt: Optional[str] = None,
    include_context: bool = False
) -> Supervisor:
    """
    Create a supervisor function that uses an LLM to make a supervision decision.
    """
    if system_prompt is None:
        system_prompt = """
Your goal is to review the agent's function call based on the provided policies, rules, and context. 
You need to decide whether the function call should be approved, rejected, escalated, terminated, or modified. 
Provide your decision along with a clear explanation. If you choose to modify the function call, specify the modified arguments in the following format:

ModifiedData:
- tool_args: [list of modified positional arguments]
- tool_kwargs: {dictionary of modified keyword arguments}
"""

    def supervisor(
        func: Callable,
        supervision_context: SupervisionContext,
        ignored_attributes: list[str],
        tool_args: list[Any],
        tool_kwargs: dict[str, Any],
        decision: Optional[SupervisionDecision] = None,
        **kwargs
    ) -> SupervisionDecision:
        """
        LLM supervisor that makes a decision based on the function call, its arguments, and the supervision instructions.
        """
        # Extract function details
        func_name = func.__qualname__
        func_description = str(func.__doc__) or "No description available."
        try:
            source_lines, _ = inspect.getsourcelines(func)
            # Remove decorator lines before the function definition
            func_def_index = next(
                i for i, line in enumerate(source_lines) if line.lstrip().startswith('def ')
            )
            func_implementation = ''.join(source_lines[func_def_index:])
        except (OSError, StopIteration):
            func_implementation = "Source code not available."
            
        # Prepare tool arguments string
        tool_args_str = ", ".join([f"{i}: {repr(arg)}" for i, arg in enumerate(tool_args)])
        tool_kwargs_str = ", ".join(
            [f"{k}={repr(v)}" for k, v in tool_kwargs.items() if k not in ignored_attributes] +
            [f"{k}=<value hidden> - Assume the value is correct" for k in ignored_attributes]
        )
        if tool_args_str and tool_kwargs_str:
            arguments_str = f"Positional Arguments:\n{tool_args_str}\nKeyword Arguments:\n{tool_kwargs_str}"
        elif tool_args_str:
            arguments_str = f"Positional Arguments:\n{tool_args_str}"
        elif tool_kwargs_str:
            arguments_str = f"Keyword Arguments:\n{tool_kwargs_str}"
        else:
            arguments_str = "The function does not require any arguments."

        # Prepare the assistant's instructions
        instructions_content = "Instructions:\n" + instructions 
        
        if decision is not None:
            instructions_content += "\n\nDecision made by the previous supervisor:\nDecision: " + decision.decision + "\nExplanation: " + decision.explanation

        if include_context and supervision_context:
            # Convert SupervisionContext into a textual description
            context_description = supervision_context.to_text()
            instructions_content += f"""
This is the conversation between the AI customer support assistant and the customer:
{context_description}
"""

        instructions_content += f"""
The AI agent is attempting to call the following function:

Function Name:
{func_name}

Function Description:
{func_description}

Function Implementation:
{func_implementation}

Arguments Passed to the Function:
{arguments_str}

Given the context and your specific instructions, you need to decide whether the function call should be **approved**, **rejected**, **escalated**, **terminated**, or **modified**. Provide your decision along with a clear and concise explanation. If you choose to modify the function call, specify the modified arguments in the following format:

ModifiedData:
- tool_args: [List[Any]
- tool_kwargs: [Dict[str, Any]]
"""

        # Prepare messages
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": instructions_content.strip()},
        ]

        # Define the function schema for SupervisionDecision
        supervision_decision_schema = SupervisionDecision.model_json_schema()

        # Prepare the function definition for the OpenAI API
        functions = [
            {
                "name": "supervision_decision",
                "description": "Make a supervision decision for the given function call. If you modify the function call, include the modified arguments or keyword arguments in the 'modified' field.",
                "parameters": supervision_decision_schema,
            }
        ]

        try:
            # Call the OpenAI API
            completion = client.chat.completions.create(
                model=openai_model,
                messages=messages,
                functions=functions,
                function_call={"name": "supervision_decision"},
            )

            # Extract the function call arguments from the response
            message = completion.choices[0].message
            if message.function_call:
                response_args = message.function_call.arguments
                response_data = json.loads(response_args)
            else:
                raise ValueError("No valid function call in assistant's response.")

            # Parse the 'modified' field, only including fields that have changed
            modified_data = None
            if response_data.get("modified"):
                modified_fields = response_data["modified"]
                modified_data = ModifiedData(
                    tool_args=modified_fields.get("tool_args", tool_args),
                    tool_kwargs=modified_fields.get("tool_kwargs", tool_kwargs)
                )

            decision = SupervisionDecision(
                decision=response_data.get("decision"),
                modified=modified_data,
                explanation=response_data.get("explanation")
            )
            return decision

        except Exception as e:
            print(f"Error during LLM supervision: {str(e)}")
            return SupervisionDecision(
                decision=SupervisionDecisionType.ESCALATE,
                explanation=f"Error during LLM supervision: {str(e)}",
                modified=None
            )

    supervisor.__name__ = supervisor_name if supervisor_name else llm_supervisor.__name__
    supervisor.__doc__ = description if description else supervisor.__doc__
    supervisor.supervisor_attributes = {
        "instructions": instructions,
        "openai_model": openai_model,
        "system_prompt": system_prompt,
        "include_context": include_context
    }
    return supervisor


def human_supervisor(
    timeout: int = 300,
    n: int = 1,
) -> Supervisor:
    """
    Create a supervisor function that requires human approval via backend API or CLI.

    Args:
        timeout (int): Timeout in seconds for waiting for the human decision.
        n (int): Number of approvals required.

    Returns:
        Supervisor: A supervisor function that implements human supervision.
    """
    def supervisor(
        func: Callable,
        supervision_context: SupervisionContext,
        ignored_attributes: list[str],
        tool_args: list[Any],
        tool_kwargs: dict[str, Any],
        supervision_request_id: UUID,
        decision: Optional[SupervisionDecision] = None,
        **kwargs
    ) -> SupervisionDecision:
        """
        Human supervisor that requests approval via backend API or CLI.

        Args:
            func (Callable): The function being supervised.
            supervision_context (SupervisionContext): Additional context.
            tool_args (List[Any]): Positional arguments for the function.
            tool_kwargs (dict[str, Any]): Keyword arguments for the function.

        Returns:
            SupervisionDecision: The decision made by the supervisor.
        """
        from .common import human_supervisor_wrapper
        from .config import supervision_config

        # Create TaskState from supervision_context
        task_state = supervision_context.to_task_state()

        # Create a ToolCall object representing the function call
        tool_call = ToolCall(
            id="tool_id",  # Use an appropriate ID if available
            function=func.__qualname__,
            arguments=tool_kwargs,
            type='function'
        )

        # Initialize client if needed
        client = supervision_config.client  # Assuming supervision_config is accessible

        # Get the human supervision decision
        supervisor_decision = human_supervisor_wrapper(
            task_state=task_state,
            call=tool_call,
            timeout=timeout,
            use_inspect_ai=False,
            n=n,
            supervision_request_id=supervision_request_id,
            client=client
        )

        return supervisor_decision

    supervisor.__name__ = human_supervisor.__name__
    supervisor.supervisor_attributes = {"timeout": timeout, "n": n}
    return supervisor


def auto_approve_supervisor() -> Supervisor:
    """Creates a supervisor that automatically approves any input."""
    def supervisor(
        func: Callable,
        supervision_context: SupervisionContext,
        ignored_attributes: list[str],
        tool_args: list[Any],
        tool_kwargs: dict[str, Any],
        **kwargs
    ) -> SupervisionDecision:
        return SupervisionDecision(
            decision=SupervisionDecisionType.APPROVE,
            explanation="No supervisor found for this function. It's automatically approved.",
            modified=None
        )
    supervisor.__name__ = auto_approve_supervisor.__name__
    supervisor.supervisor_attributes = {}
    return supervisor
