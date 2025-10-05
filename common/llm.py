import os
from common.config import load_config
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()
_cfg = load_config()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def get_llm():
    return ChatGroq(
        model=_cfg["llm"]["model"],
        temperature=_cfg["llm"]["temperature"]
    )