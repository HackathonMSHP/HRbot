from openai import AsyncOpenAI
#from core.config import AI_TOKEN



client = AsyncOpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key="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",
)
async def generate(text: str):
    completion = await client.chat.completions.create(
    model="deepseek/deepseek-chat",
    messages=[
        {
        "role": "user",
        "content": text
        }
    ]
    )
    print(completion)
    return completion.choices[0].message.content