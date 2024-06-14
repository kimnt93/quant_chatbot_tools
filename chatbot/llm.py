from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    HarmBlockThreshold,
    HarmCategory,
)
from langchain_groq import ChatGroq
import os


GEMINI_FLASH_MODEL = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    safety_settings={
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
    },
)  # Gemini 1.5 Flash does not support multi-functions return yet

LLAMA_70B_MODEL = ChatGroq(
    groq_api_key=os.environ['GROQ_API_KEY'],
    model_name="llama3-70b-8192"
)

LLAMA_8B_MODEL = ChatGroq(
    groq_api_key=os.environ['GROQ_API_KEY'],
    model_name="llama3-8b-8192"
)

EXTRACT_COMPANY_LLM = LLAMA_8B_MODEL
FUNCTION_CALLING_LLM = LLAMA_70B_MODEL
SYNTHETIC_LLM = LLAMA_8B_MODEL
