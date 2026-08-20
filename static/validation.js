document.addEventListener('DOMContentLoaded', function() {
    const registerForm = document.querySelector('form[action*="register"]');
    if (registerForm) {
        registerForm.addEventListener('submit', function(e) {
            const username = document.querySelector('input[name="username"]').value.trim();
            const email = document.querySelector('input[name="email"]').value.trim();
            const password = document.querySelector('input[name="password"]').value;
            const passwordConfirm = document.querySelector('input[name="password_confirm"]').value;
            const captcha = document.querySelector('input[name="captcha"]').value.trim();

            let errors = [];
            if (username.length < 3 || username.length > 20 || !/^[a-zA-Z0-9]+$/.test(username)) {
                errors.push('Имя пользователя: 3-20 латиница и цифры.');
            }
            if (!email.includes('@') || !email.split('@')[1].includes('.')) {
                errors.push('Введите корректный email.');
            }
            if (password.length < 6 || !/[a-zA-Z]/.test(password) || !/[0-9]/.test(password)) {
                errors.push('Пароль: минимум 6 символов, буквы и цифры.');
            }
            if (password !== passwordConfirm) {
                errors.push('Пароли не совпадают.');
            }
            if (captcha === '') {
                errors.push('Введите ответ капчи.');
            }

            if (errors.length > 0) {
                alert('Ошибки:\n' + errors.join('\n'));
                e.preventDefault();
            }
        });
    }
});