from services import booking_service, equipment_service, user_service
from repositories import equipment_repository, booking_repository, user_repository

def client_menu(user):
    while True:
        print(f"\n===== Клиент: {user.full_name} =====")
        print("1. Просмотр доступного инвентаря")
        print("2. Забронировать инвентарь")
        print("3. Мои бронирования")
        print("4. Вернуть инвентарь")
        print("0. Выход")
        choice = input("Выберите действие: ")

        if choice == "1":
            print("\n--- Доступный инвентарь ---")
            for eq in equipment_repository.get_all():
                status = "Доступен" if equipment_service.is_equipment_available(eq.equipment_id) else "Занят"
                print(f"[{eq.equipment_id}] {eq.equipment_name} ({eq.view_inventory}) — Автор: {eq.author_name} | {status}")

        elif choice == "2":
            try:
                eq_id = int(input("Введите ID инвентаря: "))
                booking_service.create_booking(user.user_id, eq_id)
                print("Успешно забронировано!")
            except ValueError:
                print("Ошибка: введите число")
            except Exception as e:
                print(f"Ошибка: {e}")

        elif choice == "3":
            print("\n--- Мои бронирования ---")
            bookings = [b for b in booking_repository.get_all() if b.user_id == user.user_id]
            if not bookings:
                print("Бронирований нет.")
            for b in bookings:
                print(f"[{b.booking_id}] {b.equipment_name} от {b.booking_date} — {b.status}")

        elif choice == "4":
            try:
                b_id = int(input("ID вашего бронирования: "))
                booking_service.return_booking(b_id)
                print("Инвентарь возвращён!")
            except ValueError:
                print("Ошибка: введите число")
            except Exception as e:
                print(f"Ошибка: {e}")

        elif choice == "0":
            break


def trainer_menu(user):
    while True:
        print(f"\n===== Тренер: {user.full_name} =====")
        print("1. Просмотр всего инвентаря")
        print("2. Просмотр всех бронирований")
        print("0. Выход")
        choice = input("Выберите действие: ")

        if choice == "1":
            for eq in equipment_repository.get_all():
                print(f"[{eq.equipment_id}] {eq.equipment_name} | Автор: {eq.author_name}")

        elif choice == "2":
            for b in booking_repository.get_all():
                print(f"[{b.booking_id}] {b.user_name} — {b.equipment_name} — {b.status}")

        elif choice == "0":
            break


def admin_menu(user):
    while True:
        print(f"\n===== Администратор: {user.full_name} =====")
        print("1. Просмотр всего инвентаря")
        print("2. Добавить инвентарь")
        print("3. Просмотр всех бронирований")
        print("4. Отменить бронирование")
        print("5. Просмотр пользователей")
        print("6. Добавить пользователя")
        print("0. Выход")
        choice = input("Выберите действие: ")

        if choice == "1":
            for eq in equipment_repository.get_all():
                print(f"[{eq.equipment_id}] {eq.equipment_name} | Автор: {eq.author_name}")

        elif choice == "2":
            try:
                view = input("Вид инвентаря (например, Свободные веса): ")
                name = input("Название: ")
                author_id = int(input("ID автора (1-3): "))
                equipment_service.add_equipment(view, name, author_id)
                print("Добавлено!")
            except ValueError:
                print("Ошибка: ID автора должен быть числом")
            except Exception as e:
                print(f"Ошибка: {e}")

        elif choice == "3":
            for b in booking_repository.get_all():
                print(f"[{b.booking_id}] {b.user_name} — {b.equipment_name} — {b.booking_date} — {b.status}")

        elif choice == "4":
            try:
                b_id = int(input("ID бронирования для отмены: "))
                booking_service.cancel_booking(b_id)
                print("Бронирование отменено!")
            except ValueError:
                print("Ошибка: введите число")
            except Exception as e:
                print(f"Ошибка: {e}")

        elif choice == "5":
            for u in user_repository.get_all():
                print(f"[{u.user_id}] {u.full_name} — логин: {u.login} — {u.role_name}")

        elif choice == "6":
            try:
                first_name = input("Имя: ")
                second_name = input("Фамилия: ")
                login = input("Логин: ")
                password = input("Пароль: ")
                role_id = int(input("ID роли (1-Админ, 2-Тренер, 3-Клиент): "))
                user_service.register_user(first_name, second_name, login, password, role_id)
                print("Пользователь добавлен!")
            except ValueError:
                print("Ошибка: ID роли должен быть числом")
            except Exception as e:
                print(f"Ошибка: {e}")

        elif choice == "0":
            break