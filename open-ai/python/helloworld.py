from openai import OpenAI
# importing os module for environment variables
import os
# importing necessary functions from dotenv library
from dotenv import load_dotenv, dotenv_values 
# loading variables from .env file
load_dotenv() 

apiKey = os.getenv("apiKey")

client = OpenAI(
    api_key= apiKey
)

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": "What is Hello World AI ?"
        }
    ]
)

print(completion.choices[0].message)