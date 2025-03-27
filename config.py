
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    MODEL_NAME = "qwen-2.5-32b"  
    
    LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2") == "true"
    LANGCHAIN_ENDPOINT = os.getenv("LANGCHAIN_ENDPOINT", "https://api.smith.langchain.com")
    LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")
    LANGCHAIN_PROJECT = os.getenv("LANGCHAIN_PROJECT", "default")
    
    if not GROQ_API_KEY:
        raise ValueError("Missing GROQ_API_KEY in .env file")
    if LANGCHAIN_TRACING_V2 and not LANGCHAIN_API_KEY:
        raise ValueError("Missing LANGCHAIN_API_KEY in .env file when tracing is enabled")

if Config.LANGCHAIN_TRACING_V2:
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_ENDPOINT"] = Config.LANGCHAIN_ENDPOINT
    os.environ["LANGCHAIN_API_KEY"] = Config.LANGCHAIN_API_KEY
    os.environ["LANGCHAIN_PROJECT"] = Config.LANGCHAIN_PROJECT