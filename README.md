# Dual-AI-System
#     DAIS

**DAIS (Dual AI System)** is a modular AI assistant that runs a local model (like [Mistral](https://ollama.com/library/mistral) via [Ollama](https://ollama.com/)) and intelligently falls back to the cloud (OpenAI GPT) if needed. It features:
- ⚡ Fast local AI responses (offline-capable)
- ☁️ Cloud fallback using OpenAI GPT-4o
- 🧠 Intermediate agent for intelligent routing
- 📦 FastAPI backend + Streamlit chat frontend
- 🧩 Easily extendable with other models

## 🚀 Features
- ✅ Streamed, real-time responses with typing effect
- ✅ Smart fallback logic for when local AI isn't enough
- ✅ Clean UI using Streamlit
- ✅ Modular design for agents: local, cloud, intermediate
