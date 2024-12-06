from typing import Any, Callable, Dict, List, Optional, Literal
from entropy_labs.sentinel_api_client.sentinel_api_client.types import UNSET
from enum import Enum
import random
import json
from pydantic import BaseModel, Field
from entropy_labs.mocking.policies import MockPolicy
from threading import Lock
from inspect_ai.solver import TaskState
from inspect_ai.tool import ToolCall, Tool
from inspect_ai.model import ChatMessage, ChatMessageAssistant, ChatMessageTool, ModelOutput, ChatMessageUser, ChatMessageSystem
from uuid import UUID, uuid4
from inspect_ai._util.content import Content, ContentText
from entropy_labs.supervision.langchain.utils import extract_messages_from_events
from entropy_labs.sentinel_api_client.sentinel_api_client.models.task_state import TaskState as APITaskState
from entropy_labs.sentinel_api_client.sentinel_api_client.models.message import Message
from entropy_labs.sentinel_api_client.sentinel_api_client.models.message_role import MessageRole
from entropy_labs.sentinel_api_client.sentinel_api_client.models.message_type import MessageType
from entropy_labs.sentinel_api_client.sentinel_api_client.models.tool_call import ToolCall as ApiToolCall
from entropy_labs.sentinel_api_client.sentinel_api_client.models.tool_call_arguments import ToolCallArguments
from entropy_labs.sentinel_api_client.sentinel_api_client.models.tool import Tool as ApiTool
from entropy_labs.sentinel_api_client.sentinel_api_client.models.output import Output as ApiOutput
import json
import copy
import logging

PREFERRED_LLM_MODEL = "gpt-4o"
DEFAULT_RUN_NAME = "default"




class SupervisionDecisionType(str, Enum):
    APPROVE = "approve"
    REJECT = "reject"
    ESCALATE = "escalate"
    TERMINATE = "terminate"
    MODIFY = "modify"

class ModifiedData(BaseModel):
    tool_args: Optional[List[Any]] = None
    """Modified positional arguments for the tool/function."""

    tool_kwargs: Optional[Dict[str, Any]] = None
    """Modified keyword arguments for the tool/function."""
    
    original_inspect_ai_call: Optional[ToolCall] = None
    """Original InspectAI call that was modified."""
    
    #TODO: Update to support changing the tool call itself

class SupervisionDecision(BaseModel):
    decision: SupervisionDecisionType
    """Supervision decision."""

    modified: Optional[ModifiedData] = Field(default=None)
    """Modified data for decision 'modify'."""

    explanation: Optional[str] = Field(default=None)
    """Explanation for decision."""

class SupervisionContext:
    """
    Context for supervision decisions. This is used to store the context of the currently active project including all tasks/runs.
    """
    def __init__(self, pending_functions: Optional[Dict[str, Dict[str, Any]]] = None):
        self.langchain_events: List[dict] = []  # List to store all logged events
        self.lock = Lock()  # Ensure thread safety
        self.metadata: Dict[str, Any] = {}
        self.inspect_ai_state: Optional[TaskState] = None
        self.openai_messages: List[Dict[str, Any]] = []
        self.anthropic_messages: List[Dict[str, Any]] = []
        self.supervised_functions_registry: Dict[str, Dict[str, Any]] = pending_functions or {}
        self.registered_supervisors: Dict[str, UUID] = {}
        self.local_supervisors_by_id: Dict[UUID, Callable] = {}

    def add_event(self, event: dict):
        with self.lock:
            self.langchain_events.append(event)

    def add_metadata(self, key: str, value: Any):
        self.metadata[key] = value

    def to_text(self) -> str:
        """Converts the supervision context into a textual description."""
        texts = []
        with self.lock:
            # Process LangChain events if any
            if self.langchain_events:
                texts.append("## LangChain Events:")
                for event in self.langchain_events:
                    event_description = self._describe_event(event)
                    texts.append(event_description)

            # Process inspect_ai_state if it exists
            if self.inspect_ai_state:
                inspect_ai_text = self._describe_inspect_ai_state()
                texts.append(inspect_ai_text)
                
            # Process OpenAI messages if any
            if self.openai_messages:
                openai_text = self._describe_openai_messages()
                texts.append(openai_text)

        return "\n\n".join(texts)

    def _describe_event(self, event: dict) -> str:
        """Converts a single event into a textual description."""
        event_type = event.get("event", "Unknown Event")
        data = event.get("data", {})
        description = f"### Event: {event_type}\nData:\n```json\n{json.dumps(data, indent=2)}\n```"
        return description

    def _describe_inspect_ai_state(self) -> str:
        """Converts the inspect_ai_state into a textual description."""
        state = self.inspect_ai_state
        texts = []
        
        if state is None:
            return ""

        # Include meta information
        meta_info = f"## Inspect AI State:\n**Model:** {state.model}\n**Sample ID:** {state.sample_id}\n**Epoch:** {state.epoch}"
        texts.append(meta_info)

        # Include messages
        texts.append("### Messages:")
        for message in state.messages:
            message_text = self._describe_chat_message(message)
            texts.append(message_text)

        # Include output if available
        if state.output:
            texts.append("### Output:")
            texts.append(f"```json\n{json.dumps(state.output.dict(), indent=2)}\n```")

        return "\n\n".join(texts)

    def _describe_chat_message(self, message: ChatMessage) -> str:
        """Converts a chat message into a textual description."""
        role = message.role.capitalize()
        text_content = message.text.strip()
        text = f"**{role}:**\n{text_content}"

        if isinstance(message, ChatMessageAssistant) and message.tool_calls:
            text += "\n\n**Tool Calls:**"
            for tool_call in message.tool_calls:
                tool_call_description = self._describe_tool_call(tool_call)
                text += f"\n{tool_call_description}"

        return text

    def _describe_tool_call(self, tool_call: ToolCall) -> str:
        """Converts a ToolCall into a textual description."""
        description = (
            f"- **Tool Call ID:** {tool_call.id}\n"
            f"  - **Function:** {tool_call.function}\n"
            f"  - **Arguments:** `{json.dumps(tool_call.arguments, indent=2)}`\n"
            f"  - **Type:** {tool_call.type}"
        )
        return description

    def _describe_openai_messages(self) -> str:
        """Converts the OpenAI messages into a textual description."""
        messages = [convert_openai_message(msg) for msg in self.openai_messages]
        texts = []
        texts.append("## OpenAI Messages:")
        for message in messages:
            message_text = self._describe_chat_message(message)
            texts.append(message_text)
        return "\n\n".join(texts)

    # Methods to manage the supervised functions registry
    def add_supervised_function(
        self,
        func: Callable,
        supervision_functions: Optional[List[List[Callable]]] = None,
        ignored_attributes: Optional[List[str]] = None,
    ):
        func_name = func.__qualname__
        with self.lock:
            if func_name in self.supervised_functions_registry:
                print(f"Function '{func_name}' is already registered in context. Skipping.")
                return  # Skip adding the duplicate

            self.supervised_functions_registry[func_name] = {
                'supervision_functions': supervision_functions or [],
                'ignored_attributes': ignored_attributes or [],
                'function': func,
            }
            print(f"Registered function '{func_name}' in supervision context")

    def get_supervised_function_entry(self, func_name: str) -> Optional[Dict[str, Any]]:
        with self.lock:
            return self.supervised_functions_registry.get(func_name)

    def update_tool_id(self, func: Callable, tool_id: UUID):
        with self.lock:
            if func.__qualname__ in self.supervised_functions_registry:
                self.supervised_functions_registry[func.__qualname__]['tool_id'] = tool_id
                print(f"Updated tool ID for '{func.__qualname__}' to {tool_id}")

    def add_run_id_to_supervised_function(self, func: Callable, run_id: UUID):
        with self.lock:
            if func.__qualname__ in self.supervised_functions_registry:
                self.supervised_functions_registry[func.__qualname__]['run_id'] = run_id
                print(f"Updated run ID for '{func.__qualname__}' to {run_id}")

    def add_supervisor_id(self, supervisor_name: str, supervisor_id: UUID):
        with self.lock:
            self.registered_supervisors[supervisor_name] = supervisor_id
            print(f"Locally registered supervisor '{supervisor_name}' with ID: {supervisor_id}")

    def get_supervisor_id(self, supervisor_name: str) -> Optional[UUID]:
        with self.lock:
            return self.registered_supervisors.get(supervisor_name)

    def to_task_state(self) -> APITaskState:
        """Converts the supervision context into the API client's TaskState model."""
        if self.inspect_ai_state:
            return convert_task_state(self.inspect_ai_state)
        elif self.openai_messages: #TODO: this is when user uses directly openai messages, update
            # Convert OpenAI messages to TaskState
            messages = [convert_openai_message(msg) for msg in self.openai_messages]
            empty_output = ApiOutput(
                    model=UNSET,
                    choices=UNSET,
                    usage=UNSET
    )
            return APITaskState(
                    messages=messages,
                    tools=[],
                    output=empty_output,
                    completed=False,
                    tool_choice=UNSET,
                )
        
        elif self.anthropic_messages:
            empty_output = ApiOutput(
                    model=UNSET,
                    choices=UNSET,
                    usage=UNSET
    )
            return APITaskState(
                messages=[convert_anthropic_message(msg) for msg in self.anthropic_messages],
                tools=[],
                output=empty_output,
                completed=False,
                tool_choice=UNSET,
            )
        
        elif self.langchain_events:
            messages = extract_messages_from_events(self.langchain_events)

            # Create your custom TaskState object
            # TODO: Initialize direct API TaskState ?
            task_state = TaskState(
                model='model_name',  # TODO: Update with actual model name
                sample_id=str(uuid4()),
                epoch=1,
                input=messages[0].content if messages else "",
                messages=messages,
                completed=False,
                metadata={}
            )
            return convert_task_state(task_state)
        else:
            # Handle case when no messages are available
            return APITaskState(
                messages=[],
                tools=[],
                output=None,
                completed=False,
                tool_choice=None,
            )
        
    def get_api_messages(self) -> List[Message]:
        """Get the messages from the supervision context in the API client's Message model."""
        if self.openai_messages:
            # Convert OpenAI messages to ChatMessage objects
            return [convert_openai_message(msg) for msg in self.openai_messages]
        elif self.anthropic_messages:
            return [convert_anthropic_message(msg) for msg in self.anthropic_messages]
        elif self.langchain_events:
            # Extract messages from LangChain events
            return [convert_message(msg) for msg in extract_messages_from_events(self.langchain_events)]
        elif self.inspect_ai_state:
            # Use messages from inspect_ai_state
            return [convert_message(msg) for msg in self.inspect_ai_state.messages]
        else:
            # No messages available
            return []
        
    def update_messages(self, messages: List[Dict[str, Any]], anthropic: bool = False):
        """Updates the context with a list of OpenAI messages."""
        with self.lock:
            if anthropic:
                self.anthropic_messages = messages.copy()
            else:
                self.openai_messages = messages.copy()

    def add_local_supervisor(self, supervisor_id: UUID, supervisor_func: Callable, supervisor_name: str):
        """Add a supervisor function to the config."""
        self.local_supervisors_by_id[supervisor_id] = supervisor_func

    def get_supervisor_by_id(self, supervisor_id: UUID) -> Optional[Callable]:
        """Retrieve a supervisor function by its ID."""
        return self.local_supervisors_by_id.get(supervisor_id)

class Run(BaseModel):
    run_id: UUID
    run_name: str
    supervision_context: SupervisionContext = Field(default_factory=SupervisionContext)

    class Config:
        arbitrary_types_allowed = True

class Task(BaseModel):
    task_id: UUID
    task_name: str
    runs: Dict[str, Run] = Field(default_factory=dict)


class Project(BaseModel):
    project_id: UUID
    project_name: str
    tasks: Dict[str, Task] = Field(default_factory=dict)

class SupervisionConfig:
    def __init__(self):
        self.global_supervision_functions: List[Callable] = []
        self.global_mock_policy = MockPolicy.NO_MOCK
        self.override_local_policy = False
        self.mock_responses: Dict[str, List[Any]] = {}
        self.previous_calls: Dict[str, List[Any]] = {}
        self.llm = None
        self.client = None  # Sentinel API client

        # Hierarchical projects structure
        self.projects: Dict[str, Project] = {}  # Mapping from project_name to Project
        self.projects_by_id: Dict[UUID, Project] = {}
        self.tasks_by_id: Dict[UUID, Task] = {}
        self.runs_by_id: Dict[UUID, Run] = {}
        self.runs_by_name: Dict[str, List[Run]] = {}  # New mapping for runs by name
        self.lock = Lock()  # For thread safety
        self.pending_supervised_functions: Dict[str, Dict[str, Any]] = {}

    def set_global_supervision_functions(self, functions: List[Callable]):
        self.global_supervision_functions = functions

    def set_llm(self, llm):
        self.llm = llm

    def set_mock_policy(self, mock_policy: MockPolicy):
        self.global_mock_policy = mock_policy

    def load_previous_execution_log(self, log_file_path: str, log_format='langchain'):
        """Load and process a previous execution log."""
        with open(log_file_path, 'r') as f:
            log_data = f.readlines()
        
        if log_format == 'langchain':
            for line in log_data:
                try:
                    entry = json.loads(line)
                    if entry['event'] == 'on_tool_end':
                        function_name = entry['data']['kwargs'].get('name')
                        output = entry['data']['output']
                        if function_name:
                            if function_name not in self.previous_calls:
                                self.previous_calls[function_name] = []
                            self.previous_calls[function_name].append(output)
                except json.JSONDecodeError:
                    continue  # Skip lines that are not valid JSON
        else:
            raise ValueError(f"Unsupported log format: {log_format}")
        
        # Update mock_responses with examples from previous calls
        self.mock_responses = self.previous_calls.copy()

    def get_mock_response(self, function_name: str) -> Any:
        """Get a mock response for a specific function."""
        if function_name in self.mock_responses:
            return random.choice(self.mock_responses[function_name])
        else:
            raise ValueError(f"No mock responses available for function: {function_name}")

    # Project methods
    def add_project(self, project_name: str, project_id: UUID):
        """Add a new project."""
        project = Project(project_id=project_id, project_name=project_name)
        self.projects[project_name] = project
        self.projects_by_id[project_id] = project  # Add to ID-based dict

    def get_project(self, project_name: str) -> Optional[Project]:
        """Retrieve a project by its name."""
        return self.projects.get(project_name)

    def get_project_by_id(self, project_id: UUID) -> Optional[Project]:
        """Retrieve a project by its ID."""
        return self.projects_by_id.get(project_id)

    # Task methods
    def add_task(self, project_name: str, task_name: str, task_id: UUID):
        """Add a new task to a project."""
        project = self.get_project(project_name)
        if not project:
            raise ValueError(f"Project '{project_name}' does not exist.")
        task = Task(task_id=task_id, task_name=task_name)
        project.tasks[task_name] = task
        self.tasks_by_id[task_id] = task  # Add to ID-based dict

    def get_task(self, project_name: str, task_name: str) -> Optional[Task]:
        """Retrieve a task by its name under a project."""
        project = self.get_project(project_name)
        if project:
            return project.tasks.get(task_name)
        return None

    def get_task_by_id(self, task_id: UUID) -> Optional[Task]:
        """Retrieve a task by its ID."""
        return self.tasks_by_id.get(task_id)

    # Run methods
    def add_run(self, project_name: str, task_name: str, run_name: str, run_id: UUID):
        """Add a new run to a task under a project."""
        with self.lock:
            task = self.get_task(project_name, task_name)
            if not task:
                raise ValueError(f"Task '{task_name}' does not exist under project '{project_name}'.")

            # Obtain a copy of the pending functions
            supervision_context = SupervisionContext(pending_functions=self.pending_supervised_functions)
            print("Initialized supervised functions registry with pending functions.")

            # Optionally, clear the pending supervised functions
            # self.clear_pending_supervised_functions()

            run = Run(run_id=run_id, run_name=run_name, supervision_context=supervision_context)
            task.runs[run_name] = run
            self.runs_by_id[run_id] = run

            # Add to name-based dict
            if run_name not in self.runs_by_name:
                self.runs_by_name[run_name] = []
            self.runs_by_name[run_name].append(run)

    def get_run(self, project_name: str, task_name: str, run_name: str) -> Optional[Run]:
        """Retrieve a run by its name under a task and project."""
        task = self.get_task(project_name, task_name)
        if task:
            return task.runs.get(run_name)
        return None

    def get_run_by_id(self, run_id: UUID) -> Optional[Run]:
        """Retrieve a run by its ID."""
        return self.runs_by_id.get(run_id)

    def get_run_by_name(self, run_name: str) -> Optional[Run]:
        """Retrieve a run by its name across all projects and tasks."""
        for run in self.runs_by_name.get(run_name, []):
            return run
        return None
    
    def get_all_runs(self) -> List[Run]:
        """Retrieve all runs across all projects and tasks."""
        return list(self.runs_by_id.values())

    # Optional editing methods
    def update_project_id(self, project_name: str, new_project_id: UUID):
        """Update the project ID for a given project name."""
        project = self.projects.get(project_name)
        if project:
            project.project_id = new_project_id
        else:
            raise ValueError(f"Project '{project_name}' does not exist.")

    def update_task_id(self, project_name: str, task_name: str, new_task_id: UUID):
        """Update the task ID for a given task name under a project."""
        project = self.projects.get(project_name)
        if project:
            task = project.tasks.get(task_name)
            if task:
                task.task_id = new_task_id
            else:
                raise ValueError(f"Task '{task_name}' does not exist under project '{project_name}'.")
        else:
            raise ValueError(f"Project '{project_name}' does not exist.")

    def update_run_id(self, project_name: str, task_name: str, run_name: str, new_run_id: UUID):
        """Update the run ID for a given run name under a task and project."""
        project = self.projects.get(project_name)
        if project:
            task = project.tasks.get(task_name)
            if task:
                if run_name in task.runs:
                    task.runs[run_name].run_id = new_run_id
                else:
                    raise ValueError(f"Run '{run_name}' does not exist under task '{task_name}' and project '{project_name}'.")
            else:
                raise ValueError(f"Task '{task_name}' does not exist under project '{project_name}'.")
        else:
            raise ValueError(f"Project '{project_name}' does not exist.")

    def update_supervision_context_by_run_id(self, run_id: UUID, new_supervision_context: SupervisionContext):
        """Update the supervision context for a run specified by run_id."""
        run = self.get_run_by_id(run_id)
        if run:
            run.supervision_context = new_supervision_context
            print(f"Updated supervision context for run_id {run_id}")
        else:
            raise ValueError(f"No run found with run_id {run_id}")

    def update_supervision_context_by_run_name(
        self,
        run_name: str,
        new_supervision_context: SupervisionContext,
    ):
        """Update the supervision context for a run specified by run_name."""
        with self.lock:
            runs = self.runs_by_name.get(run_name)
            if runs:
                if len(runs) == 1:
                    run = runs[0]
                else:
                    raise ValueError(
                        f"Multiple runs found with run_name '{run_name}'. Please specify project and task names."
                    )
                run.supervision_context = new_supervision_context
                print(f"Updated supervision context for run_name '{run_name}'")
            else:
                raise ValueError(f"No run found with run_name '{run_name}'")

    def add_supervised_function_to_all_runs(
        self,
        func: Callable,
        supervision_functions: List[List[Callable]] = [],
        ignored_attributes: List[str] = [],
    ):
        """
        Add supervised functions to the supervision context of each run in the supervision configuration.
        """
        with self.lock:
            for run in self.get_all_runs():
                run.supervision_context.add_supervised_function(func, supervision_functions, ignored_attributes)
                print(f"Added supervised function '{func.__qualname__}' to run '{run.run_name}'")
    # Method to register supervised functions temporarily
    def register_pending_supervised_function(
        self,
        func: Callable,
        supervision_functions: Optional[List[List[Callable]]] = None,
        ignored_attributes: Optional[List[str]] = None,
    ):
        func_name = func.__qualname__
        with self.lock:
            if func_name in self.pending_supervised_functions:
                print(f"Function '{func_name}' is already pending registration. Skipping.")
                return  # Skip adding the duplicate

            self.pending_supervised_functions[func_name] = {
                'supervision_functions': supervision_functions or [],
                'ignored_attributes': ignored_attributes or [],
                'function': func,
            }
            print(f"Registered pending supervised function '{func_name}'")

    def get_pending_supervised_functions(self) -> Dict[str, Dict[str, Any]]:
        """Returns a deep copy of the pending supervised functions."""
        with self.lock:
            return copy.deepcopy(self.pending_supervised_functions)

    # Optionally, clear the pending supervised functions if needed
    def clear_pending_supervised_functions(self):
        with self.lock:
            self.pending_supervised_functions.clear()
            print("Cleared pending supervised functions")

# Global instance of SupervisionConfig
supervision_config = SupervisionConfig()

def get_supervision_config():
    return supervision_config

def get_supervision_context(run_id: UUID, project_name: Optional[str] = None, task_name: Optional[str] = None, run_name: Optional[str] = None) -> SupervisionContext:
    if project_name and task_name and run_name:
        run = supervision_config.get_run(project_name, task_name, run_name)
    else:
        run = supervision_config.get_run_by_id(run_id)
    if run:
        return run.supervision_context
    else:
        raise ValueError(f"No run found with run_id {run_id}")

def set_global_supervision_functions(functions: List[Callable]):
    supervision_config.set_global_supervision_functions(functions)

def set_global_mock_policy(mock_policy: MockPolicy, override_local_policy: bool = False):
    supervision_config.set_mock_policy(mock_policy)
    supervision_config.override_local_policy = override_local_policy

def setup_sample_from_previous_calls(log_file_path: str):
    """Set up the SAMPLE_FROM_PREVIOUS_CALLS mock policy."""
    supervision_config.load_previous_execution_log(log_file_path)
    set_global_mock_policy(MockPolicy.SAMPLE_PREVIOUS_CALLS, override_local_policy=True)

def convert_task_state(task_state: TaskState) -> APITaskState:
    """
    Converts Inspect AI TaskState object into the Sentinel API client's TaskState model.
    They should be identical when serialized.
    """
    from entropy_labs.sentinel_api_client.sentinel_api_client.types import UNSET
    from entropy_labs.sentinel_api_client.sentinel_api_client.models.task_state import TaskState as APITaskState

    # Convert messages
    messages = [convert_message(msg) for msg in task_state.messages]

    # Convert tools - we can't do this because Inspect AI doesn't have tool names    
    tools: list[ApiTool] = []

    # Convert output
    output = convert_output(task_state.output)

    # Convert tool_choice
    tool_choice = UNSET

    return APITaskState(
        messages=messages,
        tools=tools,
        output=output,
        completed=False,
        tool_choice=tool_choice,
    )

def convert_message(msg: ChatMessage) -> Message:
    """
    Converts a ChatMessage to a Message in the API model.
    """

    # Convert content to a string
    if isinstance(msg.content, str):
        content_str = msg.content
    elif isinstance(msg.content, list):
        content_str = "\n".join([convert_content(content) for content in msg.content])
    else:
        content_str = ""
        
    if isinstance(msg, ChatMessageTool):
        tool_call_id = msg.tool_call_id
        function = msg.function
        content_str = f"Function {function} has been executed with result: {msg.content}."
        if msg.error:
            content_str = f"Function {function} has been executed with error: {msg.error}"
    else:
        tool_call_id = UNSET
        function = UNSET

    if isinstance(msg, ChatMessageAssistant) and msg.tool_calls:
        tool_calls = [convert_tool_call(tool_call) for tool_call in msg.tool_calls]
    else:
        tool_calls = UNSET

    return Message( 
        source=msg.source if msg.source else UNSET,
        role=MessageRole(msg.role) if msg.role != 'tool' else MessageRole.ASSISTANT,
        content=content_str,
        tool_calls=tool_calls,
        type=MessageType.TEXT #TODO: Add support for audio messages and images
    )

def convert_anthropic_message(msg: Dict) -> Message:
    """
    Converts an Anthropic message dict to a Message object in the API model.
    """

    from entropy_labs.sentinel_api_client.sentinel_api_client.models.message import Message
    from entropy_labs.sentinel_api_client.sentinel_api_client.models.message_type import MessageType
    from entropy_labs.sentinel_api_client.sentinel_api_client.models.message_role import MessageRole
    from entropy_labs.sentinel_api_client.sentinel_api_client.types import UNSET

    # Extract role
    role_str = msg.get('role', 'assistant')
    role_mapping = {
        'assistant': MessageRole.ASSISTANT,
        'user': MessageRole.USER,
        'system': MessageRole.SYSTEM,
    }
    role = role_mapping.get(role_str, MessageRole.ASSISTANT)

    # Extract content
    content = msg.get('content', '')

    content_str = ''
    tool_calls = []
    message_type = MessageType.TEXT  # Default to text

    if isinstance(content, str):
        # Content is a simple string
        content_str = content
    elif isinstance(content, list):
        # Content is a list of content blocks
        for content_block in content:
            block_type = content_block.get('type', 'text')
            if block_type == 'image':
                # Process image content blocks
                image_source = content_block.get('source', {})
                image_data = image_source.get('data', '')
                media_type = image_source.get('media_type', '')
                # Format content as data URI
                content_str = f"data:{media_type};base64,{image_data}"
                message_type = MessageType.IMAGE
                break  # Assume only one image per message
            elif block_type == 'text':
                text = content_block.get('text', '')
                content_str += text + '\n'
            elif block_type == 'tool_use':
                # Process as a tool use
                tool_use = content_block
                api_tool_call = convert_anthropic_tool_call(tool_use)
                tool_calls.append(api_tool_call)
            else:
                # Handle other content block types if needed; for now, we skip
                pass
        else:
            # No image found; set message type to text
            content_str = content_str.strip()
            message_type = MessageType.TEXT
    else:
        # Content is neither string nor list; convert to string
        content_str = str(content)

    # Construct the Message object
    message = Message(
        role=role,
        content=content_str,
        type=message_type,
        tool_calls=tool_calls if tool_calls else UNSET,
    )
    return message


def convert_anthropic_tool_call(tool_use: Dict) -> ApiToolCall:
    """
    Converts an Anthropic tool use dict to an ApiToolCall object.
    """
    from entropy_labs.sentinel_api_client.sentinel_api_client.models.tool_call import ToolCall as ApiToolCall
    from entropy_labs.sentinel_api_client.sentinel_api_client.models.tool_call_arguments import ToolCallArguments
    from entropy_labs.sentinel_api_client.sentinel_api_client.types import UNSET

    id_ = tool_use.get('id', '')
    name = tool_use.get('name', '')
    input_args = tool_use.get('input', {})
    type_ = 'tool_use'  # Define the type as 'tool_use'
    parse_error = UNSET  # No parse error in this context

    # Convert input_args to ToolCallArguments
    arguments_obj = ToolCallArguments.from_dict(input_args)

    tool_call = ApiToolCall(
        id=id_ if id_ else UNSET,
        function=name,
        arguments=arguments_obj,
        type=type_,
        parse_error=parse_error,
    )

    return tool_call


def convert_content(content: Content) -> str:
    # Convert Content to a string representation
    if isinstance(content, ContentText):
        return content.text
    elif hasattr(content, 'data_url'):
        return content.data_url  # For images or other content types
    else:
        return str(content)

def convert_tool_call(tool_call: ToolCall) -> ApiToolCall:
    return ApiToolCall(
        id=tool_call.id,
        function=tool_call.function,
        arguments=ToolCallArguments.from_dict(tool_call.arguments),
        type=tool_call.type
    )


def convert_output(output: ModelOutput) -> ApiOutput:
    from entropy_labs.sentinel_api_client.sentinel_api_client.models.output import Output as ApiOutput

    return ApiOutput(
        model=output.model if output.model else UNSET,
        choices=UNSET, #TODO: Implement if needed
        usage=UNSET
    )

def convert_openai_message(openai_msg: Dict[str, Any]) -> Message:
    """
    Converts an OpenAI message dict to a Message object in the API model.
    """
    from entropy_labs.sentinel_api_client.sentinel_api_client.models.message import Message
    from entropy_labs.sentinel_api_client.sentinel_api_client.models.message_role import MessageRole
    from entropy_labs.sentinel_api_client.sentinel_api_client.models.message_type import MessageType
    from entropy_labs.sentinel_api_client.sentinel_api_client.types import UNSET

    role_str = openai_msg.get('role')
    content = openai_msg.get('content', '') or ''
    message_id = openai_msg.get('id', UNSET)
    source = openai_msg.get('source', UNSET)
    tool_calls_data = openai_msg.get('tool_calls', UNSET)

    # Map role string to MessageRole enum
    role_mapping = {
        'assistant': MessageRole.ASSISTANT,
        'user': MessageRole.USER,
        'system': MessageRole.SYSTEM,
        # 'tool': MessageRole.TOOL,
    }

    role = role_mapping.get(role_str, MessageRole.USER)

    # Determine message type and content
    message_type = MessageType.TEXT  # Default to TEXT
    if isinstance(content, list):
        if len(content) > 1:
            logging.warning("Message has multiple items in content")
        for item in content:
            if item.get('type') == 'image_url':
                message_type = MessageType.IMAGE_URL
                content = item['image_url']['url']
                if content.startswith("data"):
                    message_type = MessageType.IMAGE
                content = item['image_url']['url']
                break
            elif item.get('type') == 'text':
                content = item['text']

    # Convert tool_calls if any
    if tool_calls_data and tool_calls_data is not UNSET:
        tool_calls = [convert_openai_tool_call(tc) for tc in tool_calls_data]
    else:
        tool_calls = UNSET

    message = Message(
        role=role,
        content=content,
        id=message_id,
        type=message_type,
        source=source,
        tool_calls=tool_calls,
    )

    return message

def convert_openai_tool_call(tool_call_dict: Dict[str, Any]) -> ApiToolCall:
    """
    Converts an OpenAI tool call dict to a ToolCall object in the API model.
    """

    id_ = tool_call_dict.get('id', '')
    function = tool_call_dict.get('function', '')
    arguments = tool_call_dict.get('arguments', {})
    type_ = tool_call_dict.get('type', '')
    parse_error = tool_call_dict.get('parse_error', UNSET)
    
    # Ensure 'function' is a string
    if isinstance(function, dict):
        function = function.get('name', '')
    elif not isinstance(function, str):
        function = str(function)

    # Convert arguments to ToolCallArguments
    if isinstance(arguments, dict):
        arguments_obj = ToolCallArguments.from_dict(arguments)
    elif isinstance(arguments, str):
        try:
            arguments_obj = ToolCallArguments.from_dict(json.loads(arguments))
        except json.JSONDecodeError:
            arguments_obj = ToolCallArguments()
    else:
        arguments_obj = ToolCallArguments()

    tool_call = ApiToolCall(
        id=id_,
        function=function,
        arguments=arguments_obj,
        type=type_,
        parse_error=parse_error,
    )

    return tool_call

