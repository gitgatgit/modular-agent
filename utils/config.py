from dotenv import load_dotenv
import os

load_dotenv()

def get_openai_api_key():
    """Returns OpenAI API key from environment"""
    return os.getenv("OPENAI_API_KEY")