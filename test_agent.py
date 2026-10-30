from openai import OpenAI
# Импортируем функции из созданного модуля database.py
from database import init_db, save_message, get_chat_history

# Инициализируем базу данных при старте (если файлов нет - они создадутся)
init_db()

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

# Временный текстовый ID, пока не перешёл в Telegram
USER_ID = 12345

print("==========================================================")
print("Приватный бункер KotoSensei готов к работе на модели Qwen 2.5 7B!")
print("==========================================================")
print("Как только загрузка завершится, напиши 'Привет' для старта.")

# Шаг 1 - Вместо пустого списка, подгружаем ИСТОРИЮ прошлых диалогов из базы данных!
messages = [{"role": "system", "content": system_prompt}] # Список где хранится история всего диалога, чтобы бот помнил контекст общения 
past_history = get_chat_history(USER_ID, limit=10)
messages.extend(past_history)

if past_history:
    print(f"Загружено {len(past_history)} реплик из твоей прошлой беседы на диске D. Сенсей всё помнит!")
else:
    print("Это твой первый урок. Напиши 'Привет' для старта.")

while True:
    user_text = input("\nТы: ")
    if user_text.lower() in ['exit', 'quit', 'выход']:
        break

    if not user_text.strip():
        continue
        
    # Добавляем сообщение в оперативную память и сразу сохраняем на диск D
    messages.append({"role": "user", "content": user_text}) # Добавление фразы пользователя в историю
    save_message(USER_ID, "user", user_text)
    
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
        
        # Добавляем ответ ИИ в оперативную память и СРАЗУ сохраняем на диск D
        messages.append({"role": "assistant", "content": full_reply}) # Сохранение ответа агента в историю
        save_message(USER_ID, "assistant", full_reply)
        
    except Exception as e:
        print(f"\n[Ошибка] Не удалось получить ответ: {e}")