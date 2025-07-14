from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def cloud_response(user_input: str) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": user_input}
            ]
        )
        return f"Cloud AI: {response.choices[0].message.content.strip()}"
    except Exception as e:
        return f"Cloud AI Error: {e}"
