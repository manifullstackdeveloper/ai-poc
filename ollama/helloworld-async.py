import asyncio
from ollama import AsyncClient

########################################################################################################
# This ollama running locally .. Thats why you dont see any api key such as open ai, huggingface etc.,
########################################################################################################

async def chat():
    """
    Stream a chat from Llama using the AsyncClient.
    """
    message = {
        "role": "user",
        "content": "Tell me an interesting fact about elephants"
    }
    async for part in await AsyncClient().chat(
        model="llama3", messages=[message], stream=True
    ):
        print(part["message"]["content"], end="", flush=True)


asyncio.run(chat())