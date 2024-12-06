import os
import asyncio
import time
from openai import AsyncOpenAI

input_text = "http://127.0.0.1:8011/v1"

client = AsyncOpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    base_url=input_text
)


async def main(stream: bool) -> None:
    start_time = time.time()

    chat_completion = await client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "介绍一下地球",
            }
        ],
        model="llama3.1:8b",
        stream=stream
    )
    models = await client.models.list()
    print(models.data[0].id)
    print(chat_completion)


asyncio.run(main(stream=False))  # 或者 main(stream=False)
