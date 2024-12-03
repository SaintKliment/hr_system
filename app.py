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


app = Flask(__name__)
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/add', methods=['GET', 'POST'])
def add_module():
    if request.method == 'POST':
        module_name = request.form['module_name']
        positions = ', '.join(request.form.getlist('positions'))  
        activities = []
        
        
        for i in range(len(request.form.getlist('activity_name[]'))):
            activities.append({
                'name': request.form.getlist('activity_name[]')[i],
                'type': request.form.getlist('activity_type[]')[i],
                'content': request.form.getlist('activity_content[]')[i]
            })

        data_source = request.form['data_source']
        duration = request.form['duration']
        responsible = request.form['responsible']

        
        new_module = Module(
            module_name=module_name,
            positions=positions,
            activities=str(activities),  
            data_source=data_source,
            duration=duration,
            responsible=responsible
        )

        db.session.add(new_module)
        db.session.commit()

        print("Название модуля:", module_name)
        print("Должности:", positions)
        print("Мероприятия:", activities)
        print("Источник данных:", data_source)
        print("Срок прохождения модуля:", duration)
        print("Ответственное лицо:", responsible)

        return redirect(url_for('index'))

    return render_template('add_module.html')

@app.route('/draft', methods=['GET', 'POST'])
def draft():
    if request.method == 'POST':
        module_name = request.form['module_name']
        positions = request.form.getlist('positions')
        activities = []
        for i in range(len(request.form.getlist('activity_name[]'))):
            activities.append({
                'name': request.form.getlist('activity_name[]')[i],
                'type': request.form.getlist('activity_type[]')[i],
                'content': request.form.getlist('activity_content[]')[i]
            })
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

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    with app.app_context():
        # Создать таблицы, если их нет
        db.create_all()
        print("Таблицы успешно созданы.")

    app.run(debug=True)
