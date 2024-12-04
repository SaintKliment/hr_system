from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
from flask_bootstrap import Bootstrap
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS
from db import db
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from models.User import User
from validate import validate_fullname, validate_email, validate_password, validate_file_upload, validate_positions,validate_activity_content,validate_module_name,validate_number
from db import db 
from models.models import db, Module
    
app = Flask(__name__)
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
app.config['UPLOAD_FOLDER'] = './uploads'
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024  # 20 MB

app.secret_key = os.urandom(24)  # Для безопасности сессий
db.init_app(app)


@app.route('/view_modules')
def view_modules():
    modules = Module.query.all()  # Получаем все модули
    return render_template('view_modules.html', modules=modules)



# Декоратор для проверки аутентификации
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:  # Проверяем, есть ли пользователь в сессии
            flash("Сначала войдите в систему.", "warning")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Маршрут для добавления модуля (только для зарегистрированных пользователей)
@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_module():
    if request.method == 'POST':
        module_name = request.form['module_name']
        positions = request.form.getlist('positions')
        activities = [
            {
                'name': request.form.getlist('activity_name[]')[i],
                'type': request.form.getlist('activity_type[]')[i],
                'content': request.form.getlist('activity_content[]')[i]
            }
            for i in range(len(request.form.getlist('activity_name[]')))
        ]
        data_source = request.form['data_source']
        duration = request.form['duration']
        responsible = request.form['responsible']

        print("Название модуля:", module_name)
        print("Должности:", positions)
        print("Мероприятия:", activities)
        print("Источник данных:", data_source)
        print("Срок прохождения модуля:", duration)
        print("Ответственное лицо:", responsible)
        
        uploaded_files = request.files.getlist('materials[]')  # Получить все файлы
        for file in uploaded_files:
            if file.filename != '':
                file.save(f"./uploads/{file.filename}")  # Сохранение файлов


        return redirect(url_for('index'))
    return render_template('add_module.html')

# Маршрут для черновиков (только для зарегистрированных пользователей)
@app.route('/draft', methods=['GET', 'POST'])
@login_required
def draft():
    if request.method == 'POST':
        module_name = request.form['module_name']
        positions = request.form.getlist('positions')
        activities = [
            {
                'name': request.form.getlist('activity_name[]')[i],
                'type': request.form.getlist('activity_type[]')[i],
                'content': request.form.getlist('activity_content[]')[i]
            }
            for i in range(len(request.form.getlist('activity_name[]')))
        ]
        data_source = request.form['data_source']
        duration = request.form['duration']
        responsible = request.form['responsible']

        print("Название модуля:", module_name)
        print("Должности:", positions)
        print("Мероприятия:", activities)
        print("Источник данных:", data_source)
        print("Срок прохождения модуля:", duration)
        print("Ответственное лицо:", responsible)
        
        return redirect(url_for('index'))
    return render_template('draft.html')

# Регистрация
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        full_name = request.form['full_name']
        email = request.form['email']
        password = request.form['password']
        position = request.form.get('position', '')
        
        user = User.query.filter_by(email=email).first()
        if user:
            flash("Пользователь с таким email уже существует!", "danger")
            return redirect(url_for('signup'))

        hashed_password = generate_password_hash(password)
        new_user = User(full_name=full_name, email=email, password=hashed_password, position=position)
        db.session.add(new_user)
        db.session.commit()

        flash("Регистрация прошла успешно!", "success")
        return redirect(url_for('login'))
    return render_template('signup.html')

# Вход
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['user_name'] = user.full_name
            flash("Вход выполнен успешно!", "success")
            return redirect(url_for('index'))
        flash("Неверный email или пароль.", "danger")
    return render_template('login.html')

# Выход
@app.route('/logout')
def logout():
    session.clear()
    flash("Вы успешно вышли из системы.", "success")
    return redirect(url_for('login'))

# Главная страница (только для зарегистрированных пользователей)
@app.route('/')
@login_required
def index():
    return render_template('index.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Создать таблицы, если их нет
        print("Таблицы успешно созданы.")
    app.run(debug=True)
