DATABASE = {
    'dbname': 'hr_system',
    'user': 'postgres',
    'password': 'lomalsteklo',
    'host': 'localhost',  # или IP-адрес вашего сервера
    'port': '5432'  # стандартный порт PostgreSQL
}
# 1234567890

SQLALCHEMY_DATABASE_URI = (
    f"postgresql://{DATABASE['user']}:{DATABASE['password']}@"
    f"{DATABASE['host']}:{DATABASE['port']}/{DATABASE['dbname']}?client_encoding=utf8"
)

SQLALCHEMY_TRACK_MODIFICATIONS = False
