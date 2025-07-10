import requests
import json
def local_stream_response(prompt, model_name="mistrial"):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": model_name,
                "prompt": prompt,
                "stream": True
            },
            stream=True  # Important: enables chunked streaming
        )

        for line in response.iter_lines():
            if line:
                try:
                    json_data = line.decode("utf-8")
                    if json_data.startswith("data:"):
                        json_data = json_data[5:]
                    yield json.loads(json_data).get("response", "")
                except Exception:
                    yield ""

    except Exception as e:
        yield f"Stream Error: {e}"

def local_response(user_input, model_name="llama3"):
    import requests
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": model_name,
            "prompt": user_input,
            "stream": False
        }
    )
    return response.json().get("response", "No reply")

