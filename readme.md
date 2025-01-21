# Stock Analyzer API with AutoGen and FastAPI

A RESTful API service that wraps AutoGen's multi-agent system for stock analysis, featuring session management and stateful results storage.

## Architecture

- **FastAPI** for RESTful API endpoints
- **AutoGen** for multi-agent coordination
- **In-memory/Redis** for session storage
- **Background Tasks** for asynchronous processing

## Core Components

### 1. Agent Team Structure
```python
- Code Generator Agent: Creates analysis code
- Executor Agent: Runs and validates code
- Report Agent: Generates comprehensive reports
```

### 2. Session Management
- Unique session ID format: `analysis_{ticker}_{random_hex}`
- Stateful storage of analysis parameters and results
- Background task processing for long-running analyses

### 3. API Endpoints

#### Health Check
```bash
GET /health
Response: {"status": "healthy"}
```

#### Root Information
```bash
GET /
Response: API information and available endpoints
```

#### Start Analysis
```bash
POST /analyze
Body: {
    "ticker": "AAPL",
    "period": "1y",
    ...additional parameters
}
Response: {
    "session_id": "analysis_AAPL_1234abcd"
}
```

#### Get Results
```bash
GET /results/{session_id}
Response: {
    "params": original_parameters,
    "status": "running|completed",
    "messages": [agent_messages]
}
```

## Storage Implementation

### Development (In-Memory)
```python
results_storage = {}
```

### Production (Redis-Ready)
```python
from redis import Redis
redis_client = Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379))
)
```

## Quick Start

1. **Environment Setup**
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install fastapi uvicorn autogen-agentchat "autogen-ext[openai]" python-dotenv redis
```

2. **Configuration**
```bash
# Create .env file
OPENAI_API_KEY=your_key_here
```

3. **Run Development Server**
```bash
python -m uvicorn main:app --reload
```

## API Usage Examples

1. **Start Stock Analysis**
```bash
curl -X POST http://localhost:8000/analyze \
     -H "Content-Type: application/json" \
     -d '{
           "ticker": "AAPL",
           "period": "1y",
           "analysis_type": "technical"
         }'
```

2. **Check Analysis Results**
```bash
curl http://localhost:8000/results/analysis_AAPL_1234abcd
```

## Features
- Asynchronous processing
- Session-based result tracking
- AutoGen multi-agent coordination
- Stateful analysis storage
- Interactive API documentation (/docs)

## Dependencies
```
fastapi
uvicorn
autogen-agentchat
autogen-ext[openai]
python-dotenv
redis (optional)
```

## Notes
- API runs on http://localhost:8000
- Swagger documentation at /docs
- Background tasks handle long-running analyses
- Session results persist until server restart (in-memory) or Redis cleanup

## Future Enhancements
1. Implement Redis for production storage
2. Add result expiration
3. Implement error handling and retries
4. Add authentication
5. Add result pagination

## Contributing
Feel free to submit issues and enhancement requests!

## License
MIT