import sqlite3
import os

# Путь к файлу базы данных
DB_PATH = r"D:\OllamaModels\koto_wisdom.db"

def init_db():
    """Инициализирует базу данных и создает необходимые таблицы, если их нет."""
    # Проверяем, существует ли данный путь и папки на диске D, если нет — создаем
    db_dir = os.path.dirname(DB_PATH)
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)
        
    # Подключаемся к файлу базы данных (SQLite создаст файл сам, если его нет)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 1. Создаем таблицу профилей пользователей
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id BIGINT UNIQUE NOT NULL,
        current_level TEXT DEFAULT 'N5',
        user_notes TEXT DEFAULT ''
    )
    """)
    
    # 2. Создаем таблицу личного словаря ученика
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vocabulary (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id BIGINT NOT NULL,
        japanese_word TEXT NOT NULL,
        reading TEXT NOT NULL,
        translation TEXT NOT NULL,
        status TEXT DEFAULT 'learning',
        mistake_count INTEGER DEFAULT 0,
        FOREIGN KEY (telegram_id) REFERENCES users (telegram_id)
    )
    """)
    
    # 3. Создаем таблицу истории чата для контекста
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chat_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id BIGINT NOT NULL,
        role TEXT NOT NULL,
        message_text TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (telegram_id) REFERENCES users (telegram_id)
    )
    """)
    
    # Сохраняем изменения и закрываем соединение
    conn.commit()
    conn.close()
    print(f"[Успех] База данных успешно инициализирована по пути: {DB_PATH}")

def save_message(telegram_id: int, role: str, text: str): # Сохраняет реплику диалога в базу данных
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Сначала проверяем, есть ли пользователь в таблице users, если нет - создаем его
    cursor.execute("INSERT OR IGNORE INTO users (telegram_id) VALUES (?)", (telegram_id,))

    # Записываем само сообщение
    cursor.execute("""
        INSERT INTO chat_history (telegram_id, role, message_text)
        VALUES (?, ?, ?)
    """, (telegram_id, role, text))

    conn.commit()
    conn.close()

def get_chat_history(telegram_id: int, limit: int = 10) -> list:
    """Вытаскивает последние N сообщений из базы для контекста ИИ."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Берем последние сообщения, сортируя по ID
    cursor.execute("""
        SELECT role, message_text FROM chat_history 
        WHERE telegram_id = ? 
        ORDER BY id DESC LIMIT ?
    """, (telegram_id, limit))
    
    rows = cursor.fetchall()
    conn.close()

    # Переворачиваем сообщения, чтобы они шли в хронологическом порядке (от старых к новым)
    rows.reverse()
    
    # Превращаем строки из БД в понятный для OpenAI/Ollama формат списка словарей
    formatted_history = []
    for row in rows:
        formatted_history.append({"role": row[0], "content": row[1]})
        
    return formatted_history



# Этот блок выполнится только если запустить файл database.py напрямую
if __name__ == "__main__":
    init_db()
    print("[Успех] Модуль базы данных обновлен и готов к работе!")