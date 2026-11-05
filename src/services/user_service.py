from repositories import user_repository

def register_user(first_name: str, second_name: str, login: str, password: str, role_id: int):
    if not first_name.strip() or not second_name.strip():
        raise Exception("Имя и фамилия не могут быть пустыми")
    if not login.strip() or not password.strip():
        raise Exception("Логин и пароль не могут быть пустыми")
    if user_repository.get_by_login(login):
        raise Exception("Пользователь с таким логином уже существует")
    user_repository.create(first_name, second_name, login, password, role_id)