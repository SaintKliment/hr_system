import psycopg2
from config import DATABASE

class Database:
    def __init__(self):
        self.conn = None

    def connect(self):
        try:
            self.conn = psycopg2.connect(**DATABASE)
            print("Успешно подключено к базе данных.")
        except Exception as e:
            print(f"Ошибка подключения к базе данных: {e}")


    def close(self):
        if self.conn is not None:
            self.conn.close()
            print("Соединение с базой данных закрыто.")

    def insert_module(self, name, positions, events, data_source, deadline, responsible):
        if self.conn is not None:
            print("Соединение с базой данных не установлено.")
            return None
        

    def get_modules(self):
        if self.conn is not None:
            print("Соединение с базой данных не установлено.")
            return None