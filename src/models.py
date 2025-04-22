import os

groq_api_key = os.getenv("GROQ_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")
model_alias = "models"

model_list = [
    # {
    #     "model_name": model_alias,
    #     "litellm_params": {"model": "groq/llama3-70b-8192", "api_key": groq_api_key},
    # },
    # {
    #      "model_name": model_alias,
    #      "litellm_params": {"model": "groq/gemma2-9b-it", "api_key": groq_api_key},
    # },
    # {
    #       "model_name": model_alias,
    #       "litellm_params": {"model": "openai/gpt-4o-mini", "api_key": openai_api_key},
    # },
    {
          "model_name": model_alias,
          "litellm_params": {"model": "openai/gpt-4.1-mini", "api_key": openai_api_key},
    },
]
