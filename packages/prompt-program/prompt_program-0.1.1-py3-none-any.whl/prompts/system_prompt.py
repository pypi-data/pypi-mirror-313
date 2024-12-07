from openai import OpenAI
import os

def get_from_dict_or_env(env_key: str) -> str:
  """Get a value from a dictionary or an environment variable."""
  if env_key in os.environ and os.environ[env_key]:
      return os.environ[env_key]
  else:
      raise ValueError(
          f"Did not find {env_key}, please add an environment variable"
          f" `{env_key}` which contains it, or pass"
          f"  `{env_key}` as a named parameter."
      )

def get_system_prompt(why: str, how: str, what: str) -> str:
    openai_api_key = get_from_dict_or_env("OPENAI_API_KEY")
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