from ui.auth import login
from ui.menus import client_menu, trainer_menu, admin_menu

def main():
    while True:
        print("\n=== Система учёта спортивного инвентаря ===")
        print("1. Войти")
        print("0. Выход")
        choice = input("Выберите действие: ")

        if choice == "1":
            user = login()
            if user:
                if user.role_id == 1:
                    admin_menu(user)
                elif user.role_id == 2:
                    trainer_menu(user)
                elif user.role_id == 3:
                    client_menu(user)
        elif choice == "0":
            print("До свидания!")
            break
        else:
            print("Неверный выбор")

if __name__ == "__main__":
    main()