import streamlit as st
import requests
import json

BASE_URL = "http://127.0.0.1:8000"  # FastAPI server

st.set_page_config(page_title="DAIS", layout="centered")
st.title("🧠 DAIS (Dual AI System)")
st.caption("Running on LLaMA 3 locally via Ollama • Cloud fallback ready")

# Initialize chat memory
if "chat" not in st.session_state:
    st.session_state.chat = []

# Chat input from user
user_input = st.chat_input("Ask something...")

if user_input:
    # Store user message
    st.session_state.chat.append(("user", user_input))
    st.session_state.chat.append(("ai", ""))  # Reserve AI response slot

    ai_placeholder = st.empty()  # Where the AI will type

    with st.spinner("Thinking..."):
        try:
            # Stream response from backend
            with requests.post(
                f"{BASE_URL}/local-stream",
                json={"user_input": user_input, "model_name": "mistrial"},
                stream=True,
            ) as r:
                full_response = ""
                for chunk in r.iter_lines(decode_unicode=True):
                    if chunk:
                        try:
                            data = json.loads(chunk) if chunk.startswith("{") else {"response": chunk}
                            token = data.get("response", "")
                        except Exception:
                            token = chunk  # fallback text
                        full_response += token
                        ai_placeholder.markdown(full_response + "▌")  # Typing effect

                # Finalize the AI message
                ai_placeholder.markdown(full_response)
                st.session_state.chat[-1] = ("ai", full_response)

        except Exception as e:
            error_msg = f"⚠️ Error: {e}"
            ai_placeholder.markdown(error_msg)
            st.session_state.chat[-1] = ("ai", error_msg)

# Display chat messages
for role, msg in st.session_state.chat:
    st.chat_message(role).markdown(msg)
