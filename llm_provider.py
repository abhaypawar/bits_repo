import os
from langchain_openai import ChatOpenAI
from langchain_mistralai.chat_models import ChatMistralAI

def get_llm():
    """
    Reads the .env file and dynamically initializes the correct LLM
    based on the specified provider.
    """
    provider = os.getenv("LLM_PROVIDER", "openai").lower()
    print(f"🤖 Initializing LLM for provider: {provider}")

    if provider == "openrouter":
        api_key = os.getenv("OPENROUTER_API_KEY")
        model_name = os.getenv("OPENROUTER_MODEL_NAME")
        base_url = os.getenv("OPENROUTER_BASE_URL")

        if not all([api_key, model_name, base_url]):
            raise ValueError("OPENROUTER_API_KEY, OPENROUTER_MODEL_NAME, and OPENROUTER_BASE_URL must be set in .env")

        return ChatOpenAI(
            model=model_name,
            api_key=api_key,
            base_url=base_url,
            default_headers={
                "HTTP-Referer": "http://localhost:5001",
                "X-Title": "MCP SRE Assistant"
            }
        )
    # Add other providers here if needed
    elif provider == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        model_name = os.getenv("OPENAI_MODEL_NAME")
        if not api_key or not model_name:
            raise ValueError("OPENAI_API_KEY and OPENAI_MODEL_NAME must be set in .env")
        return ChatOpenAI(api_key=api_key, model=model_name)
    else:
        raise ValueError(f"Unsupported LLM_PROVIDER: '{provider}'. Check your .env file.")