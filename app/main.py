from fastapi import FastAPI, BackgroundTasks
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.code_executors.local import LocalCommandLineCodeExecutor
from autogen_ext.tools.code_execution import PythonCodeExecutionTool
from redis import Redis
import os
import json
from typing import Dict, Optional
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Simple in-memory storage for development
results_storage = {}

class StockAnalyzerService:
    def __init__(self):
        # Initialize model client
        self.model_client = OpenAIChatCompletionClient(
            model="gpt-4",
            api_key=os.getenv("OPENAI_API_KEY")
        )
        
        # Initialize code execution tool
        self.code_tool = PythonCodeExecutionTool(
            LocalCommandLineCodeExecutor(work_dir="/tmp/analysis")
        )
        
        # Initialize agents
        self.code_generator = AssistantAgent(
            "Code_Generator",
            model_client=self.model_client,
            tools=[self.code_tool],
            system_message="Generate Python code for stock analysis"
        )
        
        self.executor = AssistantAgent(
            "Code_Executor",
            model_client=self.model_client,
            tools=[self.code_tool],
            system_message="Execute and validate analysis code"
        )
        
        self.report_agent = AssistantAgent(
            "Report_Agent",
            model_client=self.model_client,
            system_message="Create comprehensive analysis reports"
        )
        
        # Initialize team
        self.team = RoundRobinGroupChat(
            participants=[self.code_generator, self.executor, self.report_agent],
            max_turns=10
        )
    
    async def run_analysis(self, session_id: str, analysis_params: Dict) -> str:
        """Run analysis and store results"""
        # Store analysis parameters
        results_storage[session_id] = {
            "params": analysis_params,
            "status": "running"
        }
        
        # Run analysis
        result = await self.team.run(
            task=f"Analyze stock {analysis_params.get('ticker')} "
                 f"with parameters {analysis_params}"
        )
        
        # Store results
        results_storage[session_id].update({
            "messages": [str(msg) for msg in result.messages],
            "status": "completed"
        })
        
        return session_id
    
    def get_results(self, session_id: str) -> Optional[Dict]:
        """Retrieve analysis results"""
        return results_storage.get(session_id)

# Initialize service
analyzer = StockAnalyzerService()

@app.post("/analyze")
async def create_analysis(params: Dict, background_tasks: BackgroundTasks):
    session_id = f"analysis_{params.get('ticker')}_{os.urandom(4).hex()}"
    background_tasks.add_task(analyzer.run_analysis, session_id, params)
    return {"session_id": session_id}

@app.get("/results/{session_id}")
async def get_analysis(session_id: str):
    return analyzer.get_results(session_id)

# Add a simple health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/")
async def root():
    return {
        "message": "Stock Analyzer API",
        "endpoints": {
            "analyze": "/analyze - POST request to start analysis",
            "results": "/results/{session_id} - GET request to fetch results",
            "docs": "/docs - API documentation"
        }
    }