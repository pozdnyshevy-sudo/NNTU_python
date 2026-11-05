from repositories import user_repository

def authenticate(login: str, password: str):
    user = user_repository.get_by_login(login)
    if user and user.password == password:
        return user
    return None