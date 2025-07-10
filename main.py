from fastapi import FastAPI
from pydantic import BaseModel
from agents.local_agent import local_response
from agents.cloud_agent import cloud_response
from agents.inter_agent import intermediate_response
from fastapi.responses import StreamingResponse
from agents.local_agent import local_stream_response  # Make sure this exists

app = FastAPI(title="Dual AI System API")

# Request body model
class Query(BaseModel):
    user_input: str
    model_name: str = "llama3"  # Default local model (can be "phi3", "mistral", etc.)

# Health check
@app.get("/")
def root():
    return {"message": "Dual AI API is running 🚀"}

# Endpoint: Local AI
@app.post("/local")
def get_local(query: Query):
    response = local_response(query.user_input, model_name=query.model_name)
    return {"source": "local", "model": query.model_name, "response": response}

# Endpoint: Cloud AI
@app.post("/cloud")
def get_cloud(query: Query):
    response = cloud_response(query.user_input)
    return {"source": "cloud", "response": response}

# Endpoint: Intermediate (local first, fallback to cloud)
@app.post("/intermediate")
def get_intermediate(query: Query):
    response = intermediate_response(query.user_input, local_model=query.model_name)
    return {"source": "intermediate", "local_model": query.model_name, "response": response}

# Endpoint: Streaming Local AI response
@app.post("/local-stream")
def stream_local(query: Query):
    def event_stream():
        for chunk in local_stream_response(query.user_input, query.model_name):
            yield chunk
    return StreamingResponse(event_stream(), media_type="text/plain")

