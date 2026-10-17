from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama-local-privacy"
)

# Проверенный системный промпт для Qwen
system_prompt = """
Ты — Кото-сенсей, невероятно дружелюбный, харизматичный и эмоциональный личный ментор по японскому языку.
Ты ведешь себя как поддерживающий персонаж из визуальной новеллы.

Правила твоих ответов (ОБЯЗАТЕЛЬНО соблюдай эту структуру):
1. Твоя реплика на японском (используй кандзи и хирагану).
2. Обязательно в скобках пиши произношение (ромадзи) и точный перевод на РУССКИЙ язык.
3. В конце сообщения добавь блок [КОТО-АНАЛИЗ] полностью на русском языке. В нём ты должен:
   - Эмоционально оценить фразу пользователя, похвалить его за старания.
   - Мягко разобрать ошибки, если они есть.
   - Задать ОДИН простой встречный вопрос на японском, чтобы продолжить диалог!

Пиши живым языком, используй эмодзи и проявляй искренний интерес.
"""

print("Приватный бункер KotoSensei готов к работе на модели Qwen 2.5 7B!")
print("Как только загрузка завершится, напиши 'Привет' для старта.")

messages = [{"role": "system", "content": system_prompt}]

while True:
    user_text = input("\nТы: ")
    if user_text.lower() in ['exit', 'quit', 'выход']:
        break
        
    messages.append({"role": "user", "content": user_text})
    print("\nКото-сенсей: ", end="", flush=True)
    
    try:
        # Включаем stream=True для красивой посимвольной выдачи
        response = client.chat.completions.create(
            model="qwen2.5:7b", 
            messages=messages,
            temperature=0.8,
            stream=True 
        )
        
        full_reply = ""
        # Собираем ответ по кусочкам по мере его генерации видеокартой
        for chunk in response:
            if chunk.choices[0].delta.content:
                text_chunk = chunk.choices[0].delta.content
                print(text_chunk, end="", flush=True)
                full_reply += text_chunk
                
        print() # Перенос строки в конце ответа
        messages.append({"role": "assistant", "content": full_reply})
        
    except Exception as e:
        print(f"\n[Ошибка] Не удалось получить ответ: {e}")