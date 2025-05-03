import os
from dotenv import load_dotenv, find_dotenv

# Load environment variables from .env file
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

# Model settings
DEFAULT_MODEL = os.getenv('DEFAULT_MODEL', 'gemini-1.5-flash-8b')
MODEL_PROVIDER = os.getenv('MODEL_PROVIDER', 'gemini')  
# 'gemini' (Google) / 'openai' (OpenAI) / 'hf' (HuggingFace)

# API key settings
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
HF_API_KEY = os.getenv('HF_API_KEY', '')

# Additional settings
DEBUG_MODE = os.getenv('DEBUG_MODE', 'false').lower() == 'true'
