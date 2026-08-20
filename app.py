import sqlite3

from flask import Flask, render_template, request, redirect, url_for, session, flash
from config import Config
from database import init_db, create_user, get_user_by_username, get_user_by_email,  get_user_by_login_or_email, get_user_by_id
from utils import hash_password, generate_captcha, verify_password

app = Flask(__name__)
app.config.from_object(Config)

init_db()

# try:
#     create_user('testuser', 'test@example.com', '124124124')
#     print("Тестовый пользователь создан")
# except ValueError as e:
#     print(e)


@app.route('/')
def hello():
    return ''

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET' or 'captcha_question' not in session:
        question, answer = generate_captcha()
        session['captcha_question'] = question
        session['captcha_answer'] = answer

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        password_confirm = request.form.get('password_confirm', '')
        captcha_input = request.form.get('captcha', '').strip()

        errors = {}

        if not username:
            errors['username'] = 'Имя пользователя обязательно'
        elif not (username.isalnum() and  3 <= len(username) <= 20):
            errors['username'] = 'Имя должно содержать только латиницу и цифры, от 3 до 20 символов'
        else:
            existing_user = get_user_by_username(username)
            if existing_user:
                errors['username'] = 'Пользователь с таким именем уже существует'


        if not email:
            errors['email'] = 'Email обязателен'
        elif '@' not in email or '.' not in email.split('@')[-1]:
            errors['email'] = 'Введите корректный email (с @ и доменом)'
        else:
            existing_email = get_user_by_email(email)
            if existing_email:
                errors['email'] = 'Пользователь с таким email уже зарегистрирован'

        if not password:
            errors['password'] = 'Пароль обязателен'
        elif len(password) < 6 or not any(c.isalpha() for c in password) or not any(c.isdigit() for c in password):
            errors['password'] = 'Пароль должен содержать минимум 6 символов, буквы и цифры'
        if password != password_confirm:
            errors['password_confirm'] = 'Пароли не совпадают'



        if not captcha_input:
            errors['captcha'] = 'Введите ответ капчи'
        else:
            stored_answer = session.get('captcha_answer')
            if stored_answer is None or str(captcha_input).strip() != str(stored_answer):
                errors['captcha'] = 'Неверный ответ капчи'
            session.pop('captcha_answer', None)
            session.pop('captcha_question', None)

        if errors:
            question, answer = generate_captcha()
            session['captcha_question'] = question
            session['captcha_answer'] = answer
            return render_template('register.html', errors=errors, username=username, email=email)

        try:
            password_hash = hash_password(password)
            user_id = create_user(username, email, password_hash)
            flash('Регистрация успешна! Войдите в систему.', 'success')
            return redirect(url_for('login'))
        except ValueError as e:
            flash(str(e), 'danger')
            question, answer = generate_captcha()
            session['captcha_question'] = question
            session['captcha_answer'] = answer
            return render_template('register.html', errors={}, username=username, email=email)

        # username = request.form['username']
        # email = request.form['email']
        # password = request.form['password']
        # password_confirm = request.form['password_confirm']
        # print(f"Данные: {username}, {email}, {password}, {password_confirm}")
        # return "Форма отправлена"

    return render_template('register.html', errors={}, username='', email='')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET' or 'captcha_question' not in session:
        question, answer = generate_captcha()
        session['captcha_question'] = question
        session['captcha_answer'] = answer

    if request.method == 'POST':
        login_input = request.form.get('login', '').strip()
        password = request.form.get('password', '')
        captcha_input = request.form.get('captcha', '').strip()

        errors = {}


        if not captcha_input:
            errors['captcha'] = 'Введите ответ капчи'
        else:
            stored_answer = session.get('captcha_answer')
            if stored_answer is None or str(captcha_input).strip() != str(stored_answer):
                errors['captcha'] = 'Неверный ответ капчи'

            session.pop('captcha_answer', None)
            session.pop('captcha_question', None)

        if errors:
            question, answer = generate_captcha()
            session['captcha_question'] = question
            session['captcha_answer'] = answer
            return render_template('login.html', errors=errors, login=login_input)


        user = get_user_by_login_or_email(login_input)
        if user is None:
            flash('Неверный логин или пароль', 'danger')
            question, answer = generate_captcha()
            session['captcha_question'] = question
            session['captcha_answer'] = answer
            return render_template('login.html', errors={}, login=login_input)

        if not verify_password(password, user['password_hash']):
            flash('Неверный логин или пароль', 'danger')
            question, answer = generate_captcha()
            session['captcha_question'] = question
            session['captcha_answer'] = answer
            return render_template('login.html', errors={}, login=login_input)


        session['user_id'] = user['id']
        session['username'] = user['username']
        return redirect(url_for('profile'))

    return render_template('login.html', errors={}, login='')


@app.route('/profile')
def profile():
    if 'user_id' not in session:
        flash('Пожалуйста, войдите в систему', 'warning')
        return redirect(url_for('login'))

    user = get_user_by_id(session['user_id'])
    if user is None:
        session.clear()
        flash('Сессия недействительна', 'danger')
        return redirect(url_for('login'))

    return render_template('profile.html', user=user)


@app.route('/logout')
def logout():
    session.clear()
    flash('Вы вышли из системы', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)

