import requests
from typing import Dict, Any, Optional
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class FinGPTAgent:
    def __init__(self, mcp_server_url: str = "http://localhost:8000"):
        self.mcp_server_url = mcp_server_url
        self.session = requests.Session()

    def send_request(self, task: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Send a request to the MCP server
        """
        try:
            response = self.session.post(
                f"{self.mcp_server_url}/mcp/request",
                json={
                    "task": task,
                    "context": context or {}
                }
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to communicate with MCP server: {str(e)}")

    def process_task(self, task: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Process a task using the MCP server
        """
        return self.send_request(task, context)

def main():
    # example 
    agent = FinGPTAgent()
    
    # task example
    task = "analyze_market_data"
    context = {
        "symbol": "AAPL",
        "timeframe": "1d"
    }
    
    try:
        result = agent.process_task(task, context)
        print("Task Result:", result)
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main() 