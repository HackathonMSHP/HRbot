from openai import AsyncOpenAI
from constants.config import AI_TOKEN

b = open("deepseek_core/text.txt", 'r')
file_content = b.read().split()
b.close()

client = AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=AI_TOKEN,
)

async def generate(text: str):
    completion = await client.chat.completions.create(
        model="deepseek/deepseek-chat",
        messages=[
            {
                "role": "user",
                "content": f"""{text}. Дипсик, твоя задача обработать данное резюме, и составить краткое облако тегов умений пользователя (В ответ отправь только теги через пробел) (указывай только те сферы, в знаниях создателя резюме которых ты уверен. Иначе выведи пустое значение "None". Тебе необходимо вывести только теги на английском языке (выбирай их среди них: {file_content}), по примеру через пробел. Если пользователь вводит только 1 слово и это есть в навыках, считай что он владеет эти навыком. Если пользователь вводит только язык программирования но не уточняет про библиотеки и дополнения, считай что он владеет только языком программирования"""
            }
        ]
    )
    
    response_content = completion.choices[0].message.content
    if response_content.strip().lower() == "none":
        return []
    
    response_tags = response_content.split()
    ret = list(set(response_tags) & set(file_content))  # Пересечение тегов из ответа и файла
    return ret