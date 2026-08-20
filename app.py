from flask import Flask
from flask import render_template, request
from config import Config
from database import init_db

app = Flask(__name__)
app.config.from_object(Config)

init_db()

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

