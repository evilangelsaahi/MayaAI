from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# WatsonX Configuration
WATSONX_APIKEY = os.getenv('WATSONX_APIKEY')
WATSONX_PROJECT_ID = os.getenv('WATSONX_PROJECT_ID')
WATSONX_URL = os.getenv('WATSONX_URL')
WATSONX_PLATFORM_URL = os.getenv('WATSONX_PLATFORM_URL')
WATSONX_MODEL_ID = os.getenv('WATSONX_MODEL_ID')

# Model Parameters
DECODING_METHOD = os.getenv('DECODING_METHOD')
MAX_NEW_TOKENS = int(os.getenv('MAX_NEW_TOKENS', 200))
MIN_NEW_TOKENS = int(os.getenv('MIN_NEW_TOKENS', 0))
TEMPERATURE = float(os.getenv('TEMPERATURE', 0))
TOP_K = int(os.getenv('TOP_K', 1))
TOP_P = float(os.getenv('TOP_P', 1))

# Serper Configuration
SERPER_API_KEY = os.getenv('SERPER_API_KEY')

# NewsAPI Configuration
NEWS_API_KEY = os.getenv('NEWS_API_KEY')

# OpenWeatherMap Configuration
OPENWEATHERMAP_API_KEY = os.getenv('OPENWEATHERMAP_API_KEY')

# Validate required environment variables
required_vars = [
    'WATSONX_APIKEY',
    'WATSONX_PROJECT_ID',
    'WATSONX_URL',
    'WATSONX_PLATFORM_URL',
    'WATSONX_MODEL_ID',
    'SERPER_API_KEY',
    'OPENWEATHERMAP_API_KEY'
]

missing_vars = [var for var in required_vars if not globals()[var]]
if missing_vars:
    raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}") 