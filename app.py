from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
import json
from werkzeug.utils import secure_filename 
import io
from flask_bootstrap import Bootstrap
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS
from db import db
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from models.User import User
from flask_migrate import Migrate
from models.module import Module
    
app = Flask(__name__)
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
app.config['UPLOAD_FOLDER'] = './uploads'
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024  # 20 MB

app.secret_key = os.urandom(24)  # Для безопасности сессий
db.init_app(app)
migrate = Migrate(app, db)


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
        
        print("Files in request:", request.files)
        print("Materials files:", request.files.getlist('materials[]'))

        materials = []
        for file in request.files.getlist('materials[]'):
            print("Processing file:", file.filename)
            if file and file.filename:
                filename = secure_filename(file.filename)
                file_data = file.read()
                materials.append({
                    'filename': filename,
                    'data': str(file_data)  # Преобразуем в строку для отладки
                })
            else:
                print("Empty file or filename")

        print("Materials before JSON conversion:", materials)
        materials_json = json.dumps(materials)
        print("Materials JSON:", materials_json)



        new_module = Module(
        module_name=module_name,
        positions=positions,
        activities=activities,
        data_source=data_source,
        duration=duration,
        responsible=responsible,
        materials=materials_json
        )

        # Добавление записи в сессию и сохранение в базе данных
        try:
            db.session.add(new_module)
            db.session.commit()
            print("Новый модуль успешно добавлен в базу данных.")
        except Exception as e:
            db.session.rollback()
            print(f"Произошла ошибка при добавлении модуля: {str(e)}")
        finally:
            db.session.close()

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

        new_module = Module(
        module_name=module_name,
        positions=positions,
        activities=activities,
        data_source=data_source,
        duration=duration,
        responsible=responsible
        )

        # Добавление записи в сессию и сохранение в базе данных
        try:
            db.session.add(new_module)
            db.session.commit()
            print("Новый модуль успешно добавлен в базу данных.")
        except Exception as e:
            db.session.rollback()
            print(f"Произошла ошибка при добавлении модуля: {str(e)}")
        finally:
            db.session.close()
        
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
    modules = Module.query.all() 
    return render_template('index.html', modules=modules)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Создать таблицы, если их нет
        print("Таблицы успешно созданы.")
    app.run(debug=True)
