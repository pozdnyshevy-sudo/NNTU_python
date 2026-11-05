from services import auth_service

def login():
    print("\n=== Авторизация ===")
    login_value = input("Логин: ")
    password_value = input("Пароль: ")
    user = auth_service.authenticate(login_value, password_value)
    if not user:
        print("Неверный логин или пароль")
        return None
    print(f"Добро пожаловать, {user.full_name}!")
    return user