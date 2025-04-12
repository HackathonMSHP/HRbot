from openai import AsyncOpenAI
#from core.config import AI_TOKEN


file = open("text.txt", 'r')
file = file.readline()
file.split(" ")
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
        "content": f"""{text}. Дипсик, твоя задача обработать данное резюме, и составить краткое облкао тегов умений пользователя (указывай только те сферы, в знаниях создателя резюме которых ты уверен (чем тегов меньше и чем они содержательнее, тем лучше). иначе выведи пустое значение "None"). Тебе необходимо вывести только теги на английском языке (выбирай их среди них: {file}), по примеру через пробел.    """
        }
    ]
    )
    print(completion)
    return completion.choices[0].message.content