# main.py
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
from agents.local_agent import local_response, local_stream_response
from agents.cloud_agent import cloud_response
from agents.inter_agent import intermediate_response

app = FastAPI(title="Dual AI System API")

class Query(BaseModel):
    user_input: str
    model_name: str = "mistral"

@app.get("/")
def root():
    return {"message": "Dual AI API is running"}

@app.post("/local")
def get_local(query: Query):
    response = local_response(query.user_input, model_name=query.model_name)
    return {"source": "local", "model": query.model_name, "response": response}

@app.post("/cloud")
def get_cloud(query: Query):
    response = cloud_response(query.user_input)
    return {"source": "cloud", "response": response}

@app.post("/intermediate")
def get_intermediate(query: Query):
    response = intermediate_response(query.user_input, local_model=query.model_name)
    return {"source": "intermediate", "local_model": query.model_name, "response": response}

@app.post("/local-stream")
async def stream_local(query: Query):
    async def event_stream():
        async for chunk in local_stream_response(query.user_input, query.model_name):
            yield chunk
    return StreamingResponse(event_stream(), media_type="text/plain")
