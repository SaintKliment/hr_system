import re

def validate_fullname(fullname):
    """Валидация ФИО: должно содержать только буквы и пробелы."""
    pattern = r'^[А-ЯЁа-яё\s-]+$'  # Поддержка кириллицы и пробелов
    if re.match(pattern, fullname):
        return True
    return False

def validate_email(email):
    """Валидация электронной почты."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(pattern, email):
        return True
    return False

def validate_password(password):
    """Валидация пароля: минимум 8 символов, включая буквы и цифры."""
    pattern = r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$'
    if re.match(pattern, password):
        return True
    return False

def validate_file_upload(file_name):
    """Валидация имени файла: разрешенные расширения."""
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}
    extension = file_name.rsplit('.', 1)[1].lower() if '.' in file_name else ''
    
    if extension in allowed_extensions:
        return True
    return False

# Примеры использования функций
if __name__ == "__main__":
    # Примеры тестирования функций
    print(validate_fullname("Иванов Иван Иванович"))  # True
    print(validate_email("example@mail.com"))           # True
    print(validate_password("Password123"))              # True
    print(validate_file_upload("image.png"))             # True
