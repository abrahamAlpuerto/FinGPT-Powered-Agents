# FinGPT Agent with Local MCP Server

This is a simple implementation of a FinGPT-powered agent that communicates with a local MCP (Message Control Protocol) server.

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file in the project root with any necessary environment variables:
```
OPENAI_API_KEY=your_api_key_here
```

## Running the System

1. Start the MCP server:
```bash
python src/fingpt_agent/mcp_server.py
```

2. In a separate terminal, run the FinGPT agent:
```bash
python src/fingpt_agent/agent.py
```

## Architecture

The system consists of two main components:

1. **MCP Server**: A FastAPI-based server that handles incoming requests from the FinGPT agent. It processes tasks and returns responses.

2. **FinGPT Agent**: A client that communicates with the MCP server to process tasks. It can send requests with tasks and context, and receive responses.

## Example Usage

```python
from fingpt_agent.agent import FinGPTAgent

# Create an agent instance
agent = FinGPTAgent()

# Process a task
result = agent.process_task(
    task="analyze_market_data",
    context={"symbol": "AAPL", "timeframe": "1d"}
)
print(result)
```

## API Endpoints

The MCP server exposes the following endpoint:

- `POST /mcp/request`: Accepts task requests from the FinGPT agent
  - Request body: `{"task": "task_name", "context": {...}}`
  - Response: `{"status": "success", "data": {...}, "message": "..."}`

## Extending the System

To add new functionality:

1. Add new task handlers in the MCP server's `handle_mcp_request` function
2. Create new methods in the FinGPTAgent class to handle specific types of tasks
3. Update the response models in `mcp_server.py` as needed 