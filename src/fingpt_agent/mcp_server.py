from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="FinGPT MCP Server")

class MCPRequest(BaseModel):
    task: str
    context: Optional[Dict[str, Any]] = None

class MCPResponse(BaseModel):
    status: str
    data: Dict[str, Any]
    message: Optional[str] = None

@app.post("/mcp/request", response_model=MCPResponse)
async def handle_mcp_request(request: MCPRequest):
    """
    Handle incoming MCP requests from the FinGPT agent
    """
    try:
        # Implement the actual logic to handle different tasks
        # currently, we are just returning a simple response
        response_data = {
            "task": request.task,
            "processed": True,
            "result": f"Processed task: {request.task}"
        }
        
        return MCPResponse(
            status="success",
            data=response_data,
            message="Task processed successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 