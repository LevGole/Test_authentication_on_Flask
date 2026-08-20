import sqlite3

from flask import Flask
from flask import render_template, request
from config import Config
from database import init_db, get_db
from database import create_user

app = Flask(__name__)
app.config.from_object(Config)

init_db()

try:
    create_user('testuser', 'test@example.com', '124124124')
    print("Тестовый пользователь создан")
except ValueError as e:
    print(e)


@app.route('/')
def hello():
    return ''

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        password_confirm = request.form['password_confirm']
        print(f"Данные: {username}, {email}, {password}, {password_confirm}")
        return "Форма отправлена"
    return render_template('register.html')


if __name__ == '__main__':
    app.run(debug=True)

