from openai import OpenAI
from config import OPENROUTER_API_KEY

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY
)

def summarize_problems(data):
    prompt = "Here are some Reddit threads:\n"
    for idx, entry in enumerate(data, 1):
        prompt += f"{idx}. Title: {entry['title']}\n   Description: {entry['selftext']}\n"
    prompt += "\nPlease group similar problems and summarize the main challenges users are facing."
    
    try:
        completion = client.chat.completions.create(
            model="deepseek/deepseek-r1-0528:free",
            messages=[{"role": "user", "content": prompt}]
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"LLM error: {e}"

def generate_solutions(summary):
    followup_prompt = f"""
Here are some problems and challenges users are facing, based on Reddit discussions:

{summary}

For each problem, brainstorm practical and monetizable solutions. Suggest step-by-step approaches or product ideas that could address these issues. Also, briefly comment on the feasibility of each solution.

Format your response as:
Problem: <problem statement>
Solution: <detailed, monetizable solution>
Feasibility: <brief feasibility analysis>
Step-by-step Guide: <steps>
"""
    try:
        completion = client.chat.completions.create(
            model="deepseek/deepseek-r1-0528:free",
            messages=[{"role": "user", "content": followup_prompt}]
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"LLM error: {e}"
