import sqlite3
import os

DATABASE_PATH = os.path.join(os.path.dirname(__file__), "database.db")
'''#абсолютный путь к файлу бд __file__ — встроенная переменная, которая содержит путь к текущему файлу скрипта'''

def get_db(): #Устанавливает соединение с базой данных
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row # .Row возвращает индексы как словари
    return conn


def init_db():
    conn = get_db()
    cur = conn.cursor() #создаём объект курсора чтобы выполнять SQL КОМАНДЫ
    cur.execute(
    '''
    CREATE TABLE IF NOT EXISTS users (
    id INTEGER AUTO_INCREMENT PRIMARY KEY ,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP);
    '''
    )

    conn.commit() #фиксируем изменения
    conn.close()
    print('инициализация бд закончена')
