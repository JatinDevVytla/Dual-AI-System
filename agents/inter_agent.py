from agents.local_agent import local_response
from agents.cloud_agent import cloud_response
from agents.local_agent import local_stream_response

class IntermediateAgent:
    def __init__(self, user_input, local_model="llama3"):
        self.user_input = user_input
        self.local_model = local_model

    def decide_and_respond(self):
        # Step 1: Try local response
        local_reply = local_response(self.user_input, model_name=self.local_model)

        # Step 2: Check if local response is uncertain
        if any(phrase in local_reply.lower() for phrase in [
            "not sure", "checking", "no response", "error", "ollama api error"
        ]):
            cloud_reply = cloud_response(self.user_input)
            return f"{local_reply}\n{cloud_reply}"

        # Step 3: If local was good enough
        return local_reply

def intermediate_response(user_input: str, local_model: str = "mistrial") -> str:
    # Collect response from local model
    local_output = ''.join(local_stream_response(user_input, model_name=local_model))

    # Fallback condition: local failed or was empty
    if not local_output.strip() or "I don't know" in local_output.lower():
        cloud_output = cloud_response(user_input)
        return f"Local AI ({local_model}): {local_output.strip() or 'No response generated.'}\nCloud AI: {cloud_output}"

    return f"Local AI ({local_model}): {local_output}"

