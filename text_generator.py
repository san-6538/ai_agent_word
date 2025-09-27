# text_generator.py
from google import genai
import config

client = genai.Client(api_key=config.GOOGLE_API_KEY)

def generate_text(prompt):
    """Generate text using Google Gemini API."""
    try:
        response = client.responses.create(model="gemini-2.5-flash", input=prompt)
        return response.output_text or "Could not generate text."
    except Exception as e:
        print(f"[Gemini Error] {e}")
        return "Error generating text."
