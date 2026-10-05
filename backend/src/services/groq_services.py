import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

def get_groq_client() :
    return Groq(api_key = os.environ.get("GROQ_API_KEY"))