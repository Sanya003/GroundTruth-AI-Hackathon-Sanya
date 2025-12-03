from google import genai
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
# genai.configure(api_key=api_key)
client = genai.Client()

def build_prompt(kpis, num_insights=4):
    lines = [
        f"Using the following Facebook ad campaign KPIs, generate {num_insights} concise but detailed executive insights (max 25 words each).",
        "Each insight should be one point that includes:",
        "1. Performance interpretation (e.g., trends, highs/lows, comparisons).",
        "2. Business impact of the metric.",
        "3. Suggested action or recommendation based on the metric.",
        "Format as bullet points."
        ]
    for k, v in kpis.items():
        lines.append(f"- {k}: {v}")
    return "\n".join(lines)

def generate_insights(prompt):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text
