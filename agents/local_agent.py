import httpx
import json

async def local_stream_response(prompt, model_name="mistral"):
    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            async with client.stream("POST", "http://localhost:11434/api/generate", json={
                "model": model_name,
                "prompt": prompt,
                "stream": True
            }) as response:
                async for line in response.aiter_lines():
                    if line:
                        try:
                            if line.startswith("data:"):
                                line = line[5:]
                            yield json.loads(line).get("response", "")
                        except Exception:
                            yield ""
    except Exception as e:
        yield f"Stream Error: {e}"

def local_response(user_input, model_name="mistral"):
    try:
        response = httpx.post(
            "http://localhost:11434/api/generate",
            json={
                "model": model_name,
                "prompt": user_input,
                "stream": False
            },
            timeout=15.0
        )
        response.raise_for_status()
        return response.json().get("response", "No reply")
    except Exception as e:
        return f"Local AI Error: {e}"
