from database import get_db
with get_db() as conn:
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    rows = cursor.fetchall()
    print("Текущие пользователи в БД:", [dict(row) for row in rows])