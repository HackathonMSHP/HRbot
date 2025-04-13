from openai import AsyncOpenAI

b = open("deepseek_core/text.txt", 'r')
file_content = b.read().split()
b.close()

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
                "content": f"""{text}. Дипсик, твоя задача обработать данное резюме, и составить краткое облако тегов умений пользователя (В ответ отправь только теги через пробел) (указывай только те сферы, в знаниях создателя резюме которых ты уверен. Иначе выведи пустое значение "None". Тебе необходимо вывести только теги на английском языке (выбирай их среди них: {file_content}), по примеру через пробел."""
            }
        ]
    )
    
    response_content = completion.choices[0].message.content
    if response_content.strip().lower() == "none":
        return []
    
    response_tags = response_content.split()
    ret = list(set(response_tags) & set(file_content))  # Пересечение тегов из ответа и файла
    return ret