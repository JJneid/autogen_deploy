# Deploying AutoGen Applications with FastAPI

A guide on wrapping AutoGen agents with FastAPI and containerizing the application.
Project Structure

```
autogen_app/
├── app/
│   ├── __init__.py
│   └── main.py         # FastAPI + AutoGen implementation
├── requirements.txt    # Dependencies
└── Dockerfile         # Container configuration
```
# Quick Start

## Set Up Environment

```
# Create virtual environment
python -m venv venv
source venv/bin/activate  
```

## Install dependencies
pip install fastapi uvicorn autogen-agentchat "autogen-ext[openai]" python-dotenv pydantic

## Create Configuration

```
#Create .env file
echo "OPENAI_API_KEY=your_key_here" > .env
```

Run Locally

```
#Navigate to app directory
cd app
```

```
#Start server
python -m uvicorn main:app --reload
```

## Testing the API

### Health Check

```curl 
http://localhost:8000/health
```

## Start Analysis

```curl 
-X POST http://localhost:8000/analyze \
     -H "Content-Type: application/json" \
     -d '{"task": "your task description"}'
```
#### Check Results

```bash

 http://localhost:8000/results/{session_id}
 ```

## Docker Deployment

### Build Container

```bash
#Build image
docker build -t autogen-app .
```

### Run container
```
docker run -p 8000:8000 --env-file .env autogen-app
```
### API Endpoints

```
GET /health - Health check
POST /analyze - Start new analysis
GET /results/{session_id} - Get analysis results
```


Notes

Server runs on http://localhost:8000
API documentation at http://localhost:8000/docs
Real-time logs with --reload flag

Dependencies

FastAPI
Uvicorn
AutoGen
Python-dotenv
Pydantic