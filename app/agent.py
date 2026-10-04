from google import genai
from app.config import GEMINI_API_KEY


client = genai.Client(api_key=GEMINI_API_KEY)

MODEL_NAME = "gemini-2.5-flash"


def ask_agent(user_input: str) -> str:
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=user_input
    )

    return response.text