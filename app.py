from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mail import Mail, Message
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
from models.Module import Module
from flask_socketio import SocketIO, emit

    
app = Flask(__name__)
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
app.config['UPLOAD_FOLDER'] = './uploads'
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024  # 20 MB
app.config.from_object('config_smtp')  # Загрузка конфигурации из файла config.py
mail = Mail(app)
socketio = SocketIO(app)
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
        # state = "согласование",
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

        materials_json = json.dumps(materials)



        new_module = Module(
        # state = "согласование",
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
    count_modules = Module.query.filter(Module.state == 'новый').count()
    user_logged_in = 'user_id' in session  
    return render_template('index.html', modules=modules, count_modules=count_modules, user_logged_in=user_logged_in)


@app.route('/hr_add', methods=['GET', 'POST'])
@login_required
def hr_add():
    if request.method == 'POST':
        # Получаем данные из формы
        code_name = request.form.get('module_name')
        responsible_user_ids = request.form.getlist('responsible_users')
        duration_develop = request.form.get('duration')
        importance = request.form.get('importance')
        state = "новый"


        new_module = Module(
        code_name=code_name,
        state=state,
        responsible_user_ids=responsible_user_ids,
        duration_develop=duration_develop,
        importance=importance
        )

        # Добавление записи в сессию и сохранение в базе данных
        try:
            db.session.add(new_module)
            db.session.commit()
            print("Новый модуль успешно добавлен в базу данных.")
            users = User.query.filter(User.id.in_(responsible_user_ids)).all()
            emails = [user.email for user in users]

            for email in emails:
                print(email)
                # send_email(email) # отправка шаблонного сообщения - уведомления о новом модуле
        except Exception as e:
            db.session.rollback()
            print(f"Произошла ошибка при добавлении модуля: {str(e)}")
        finally:
            db.session.close()

        return redirect(url_for('index'))
    
    users = User.query.all()
    return render_template('hr_add.html', users=users)  

@app.route('/view_modules', methods=['GET'])
@login_required
def view_modules():
    modules = Module.query.filter(Module.state.in_( ['новый', 'черновик'] )).all()
    return render_template('modules.html', modules=modules)  


@app.route('/joint_development/<int:module_id>', methods=['GET'])
@login_required
def joint_development_detail(module_id):
    module = Module.query.get_or_404(module_id)  # Получаем модуль по ID или 404, если не найден
    return render_template('module_correct.html', module=module)

@app.route('/joint_development', methods=['GET'])
@login_required
def joint_development():
    current_user_id = session['user_id']

    modules = Module.query.filter(
        Module.state.in_(['новый', 'черновик']),
        Module.responsible_user_ids.like(f'%{current_user_id}%')  # Проверяем наличие ID в строке
    ).all()

    return render_template('joint_modules.html', modules=modules)  

@socketio.on('update_module')
def handle_update(data):
    module_id = data.get('module_id')
    new_name = data.get('module_name')
    new_source = data.get('data_source')
    new_duration = data.get('duration')
    new_responsible = data.get('responsible')

    new_duration = int(new_duration) if new_duration else None
    
    MAX_INT = 1000000 
    MIN_INT = 1   

    if new_duration is not None:
        if new_duration > MAX_INT or new_duration < MIN_INT:
            new_duration = None

    # Обновление записи в БД
    module = Module.query.get(module_id)
    if module:
        module.module_name = new_name
        module.data_source = new_source 
        module.duration = new_duration 
        module.responsible = new_responsible 
        db.session.commit()

        # Рассылка обновленного имени всем клиентам
        socketio.emit('module_name', {'module_id': module_id, 'module_name': new_name, 'data_source': new_source,'duration': new_duration,'responsible': new_responsible,})

@app.route('/module/<int:module_id>', methods=['GET'])
@login_required
def module_detail(module_id):
    module = Module.query.get_or_404(module_id)  # Получаем модуль по ID или 404, если не найден
    return render_template('module_detail.html', module=module)

def send_email(recipient):
    msg = Message("Назначение разработчиком адаптационного модуля",
                  recipients=[recipient])
    msg.body = "Добрый день, коллеги.\nВы назначены разработчиком адаптационного модуля. Просим ознакомиться с приказом и приступить к работе."
    msg.html = "<p>Добрый день, коллеги.</p><p>Вы назначены разработчиком адаптационного модуля. Просим ознакомиться с приказом и приступить к работе.</p>"
    
    with app.app_context():
        mail.send(msg)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Создать таблицы, если их нет
        print("Таблицы успешно созданы.")
    socketio.run(app, debug=True)

