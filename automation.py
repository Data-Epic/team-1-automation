import pandas as pd
import os
from dotenv import load_dotenv
import cohere


# Load environment variables from .env file
load_dotenv()

# Initialize the Cohere and OpenAI clients
API_KEY = os.getenv('COHERE_API_KEY')
if API_KEY is None:
    raise ValueError("Please set the COHERE_API_KEY environment variable.")
co = cohere.ClientV2(API_KEY)