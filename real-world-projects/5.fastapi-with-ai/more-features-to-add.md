## suggesting features to add

1. create db table and connection using sqlmodel 
2. oauth2 and jwt
3. add rate limit "throttling" with redis and fastapi-limiter 
    - Why use Redis
        - Stores counters per user/IP efficiently
        - Survives app restarts (unlike your in-memory defaultdict)
        - Used in real production systems
4. Add OpenAI or HuggingFace integration
    - What they are:
        - OpenAI: Provides GPT models (ChatGPT, GPT-4o, etc.)
        - HuggingFace: Provides many open-source LLMs (free or hosted)
    - You can show multi-model AI integration:
        - Gemini for Google
        - OpenAI for GPT
        - HuggingFace for open-source models
5. realtime chat
    - it’s for real-time streaming responses from the AI model or chatting live with the API.
    - Examples:
        - Stream Gemini’s response word by word
        - Display messages instantly in frontend
6. add testing 
7. deploy with docker and ci/cd pipelines using github actions
    

