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
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP);
    '''
    )

    conn.commit() #фиксируем изменения
    conn.close()
    print('инициализация бд закончена')

def create_user(username, email, password):
    conn = get_db()
    cur = conn.cursor()

    try:
        cur.execute(
            'INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
            (username, email, password)
        )
        conn.commit()
        user_id = cur.lastrowid #создание уникального индетификатора
        conn.close()
        return user_id

    except sqlite3.IntegrityError as e: #ошибка целостности данных
        if 'username' in str(e):
            raise ValueError('Пользователь с таким именем уже существует')
        elif 'email' in str(e):
            raise ValueError('Пользователь с таким email уже зарегистрирован')
        else:
            raise e

def get_user_by_username(username):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone() #служит для получения одной первой или следующей строки из результата SQL-запроса
    conn.close()
    return user

def get_user_by_email(email):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
    user = cursor.fetchone()
    conn.close()
    return user

def get_user_by_id(user_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

def get_user_by_login_or_email(login):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ? OR email = ?', (login, login))
    user = cursor.fetchone()
    conn.close()
    return user

