from openai import OpenAI

def get_system_prompt(why: str, how: str, what: str, openai_api_key: str) -> str:
    client = OpenAI(api_key=openai_api_key,)
    response = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"""
                    Create a system prompt for a Large Language Model (LLM) to guide its behavior. 
                    The prompt should be structured as follows:
                    - **Why**: {why}
                    - **How**: {how}
                    - **What**: {what}

                    Ensure the system prompt is clear, concise, and provides enough guidance for the model to understand its role, the process, and the expected outcome in first person and paragraph only.
                    """,
                }
            ],
            model="gpt-4o-mini",
        )
    
    return (response.choices[0].message.content)