from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

async def llm_tool():
    return ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite")