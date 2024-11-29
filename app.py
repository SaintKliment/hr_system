from flask import Flask, render_template, request, redirect, url_for
from db import Database

app = Flask(__name__)
db = Database()


@app.route('/add', methods=['GET', 'POST'])
def add_module():
    if request.method == 'POST':
        # Получаем данные из формы
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
        
        # Логика обработки данных
        # (например, сохранение в базу данных или вывод на экран)
        print("Название модуля:", module_name)
        print("Должности:", positions)
        print("Мероприятия:", activities)
        print("Источник данных:", data_source)
        print("Срок прохождения модуля:", duration)
        print("Ответственное лицо:", responsible)
        
        return "Модуль успешно добавлен!"

    return render_template('add_module.html')

@app.route('/')
def index():
    db.connect()
    modules = db.get_modules()
    db.close()

    return render_template('index.html', modules=modules)

if __name__ == '__main__':
    app.run(debug=True)
