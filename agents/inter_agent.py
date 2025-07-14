from agents.local_agent import local_stream_response
from agents.cloud_agent import cloud_response


def intermediate_response(user_input: str, local_model: str = "mistral") -> str:
    local_output = ''.join([chunk async for chunk in local_stream_response(user_input, model_name=local_model)])

    failure_signals = ["i don't know", "no response", "error", "not sure", "ollama api error"]
    if not local_output.strip() or any(phrase in local_output.lower() for phrase in failure_signals):
        cloud_output = cloud_response(user_input)
        return f"Local AI ({local_model}): {local_output.strip() or 'No response generated.'}\nCloud AI: {cloud_output}"
