# Programmatic Usage

While LLMling is designed for declarative configuration, it provides a clean Python API for programmatic usage.

## RuntimeConfig

The main interface for using LLMling programmatically is the `RuntimeConfig` class:

```python
from llmling import Config, RuntimeConfig

# Create from YAML file
async with RuntimeConfig.from_file("config.yml") as runtime:
    # Use runtime...
    pass

# Create from Config object
config = Config.from_file("config.yml")
async with RuntimeConfig.from_config(config) as runtime:
    # Use runtime...
    pass

# Create from YAML string
config_yaml = """
resources:
  greeting:
    type: text
    content: "Hello, {name}!"
"""
async with RuntimeConfig.from_yaml(config_yaml) as runtime:
    # Use runtime...
    pass
```

> **Important**
> Always use RuntimeConfig as a context manager to ensure proper resource cleanup.

## Resource Operations

```python
async with RuntimeConfig.from_file("config.yml") as runtime:
    # Load a resource
    resource = await runtime.load_resource("my_resource")
    print(resource.content)
    print(resource.metadata)

    # List available resources
    resources = runtime.list_resources()

    # Get resource URI
    uri = runtime.get_resource_uri("my_resource")

    # Load by URI
    resource = await runtime.load_resource_by_uri(uri)

    # Register new resource
    from llmling.config.models import TextResource

    runtime.register_resource(
        "new_resource",
        TextResource(content="New content"),
        replace=True  # Optional, replace if exists
    )
```

## Prompt Operations

```python
async with RuntimeConfig.from_file("config.yml") as runtime:
    # Format a prompt
    messages = await runtime.render_prompt(
        "my_prompt",
        arguments={"name": "World"}
    )

    # List available prompts
    prompts = runtime.list_prompts()

    # Get prompt by name
    prompt = runtime.get_prompt("my_prompt")

    # Get all prompts
    all_prompts = runtime.get_prompts()
```

## Tool Operations

```python
async with RuntimeConfig.from_file("config.yml") as runtime:
    # Execute a tool
    result = await runtime.execute_tool(
        "my_tool",
        arg1="value1",
        arg2="value2"
    )

    # List available tools
    tools = runtime.list_tools()

    # Get tool by name
    tool = runtime.get_tool("my_tool")

    # Get all tools
    all_tools = runtime.get_tools()
```

## Event Handling

```python
from llmling.core.events import Event, EventHandler

class MyEventHandler(EventHandler):
    async def handle_event(self, event: Event) -> None:
        match event.type:
            case "RESOURCE_MODIFIED":
                print(f"Resource changed: {event.name}")
            case "TOOL_ADDED":
                print(f"New tool: {event.name}")

async with RuntimeConfig.from_file("config.yml") as runtime:
    # Add event handler
    runtime.add_event_handler(MyEventHandler())
```

## Registry Observation

```python
from llmling.core.events import RegistryEvents

class ResourceObserver(RegistryEvents):
    def on_item_added(self, key: str, item: Any) -> None:
        print(f"Resource added: {key}")

    def on_item_modified(self, key: str, item: Any) -> None:
        print(f"Resource modified: {key}")

async with RuntimeConfig.from_file("config.yml") as runtime:
    # Add observers
    runtime.add_resource_observer(ResourceObserver())
    runtime.add_prompt_observer(PromptObserver())
    runtime.add_tool_observer(ToolObserver())
```

## Example: Agent Integration

Here's an example of using LLMling with an agent:

```python
from llmling import RuntimeConfig
from llmling.agents import LLMlingAgent
from pydantic import BaseModel

# Define structured output
class Analysis(BaseModel):
    summary: str
    complexity: int
    suggestions: list[str]

# Create agent with runtime
async with RuntimeConfig.from_file("config.yml") as runtime:
    # Create agent with structured output
    agent = LLMlingAgent[Analysis](
        runtime,
        result_type=Analysis,
        model="openai:gpt-4",
        system_prompt=[
            "You are a code analysis assistant.",
            "Provide structured analysis results.",
        ],
    )

    # Use the agent
    result = await agent.run(
        "Analyze the Python code in resources/main.py"
    )

    # Access structured results
    print(f"Summary: {result.data.summary}")
    print(f"Complexity: {result.data.complexity}")
    for suggestion in result.data.suggestions:
        print(f"- {suggestion}")
```

## Best Practices

### Resource Management
- Always use async context managers
- Clean up resources properly
- Handle exceptions appropriately
- Use type hints consistently

### Error Handling
```python
from llmling.core import exceptions

async with RuntimeConfig.from_file("config.yml") as runtime:
    try:
        resource = await runtime.load_resource("missing")
    except exceptions.ResourceError as e:
        print(f"Resource error: {e}")
    except exceptions.ConfigError as e:
        print(f"Configuration error: {e}")
    except exceptions.LLMLingError as e:
        print(f"General error: {e}")
```

### Async Operations
- Use appropriate async patterns
- Don't block the event loop
- Handle cancellation properly
- Use asyncio.TaskGroup for concurrent operations

### Type Safety
- Use type hints consistently
- Enable type checking in development
- Handle type conversions explicitly
- Validate external data

## Next Steps

For more examples and detailed API documentation, see:
- [API Reference](https://llmling.readthedocs.io/en/latest/api/)
- [Example Gallery](https://llmling.readthedocs.io/en/latest/examples/)
- [Contributing Guide](https://llmling.readthedocs.io/en/latest/contributing/)
