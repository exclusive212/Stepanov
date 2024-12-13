from flet import Container, Image
import flet as ft
import sqlite3
import os

# Проверка наличия файла
if not os.path.isfile('d1.jpg'):
    print("Файл d1.jpg не найден!")

# Создание базы данных и таблиц, если они не существуют
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    # Удаляем старую таблицу, если она существует
    cursor.execute('DROP TABLE IF EXISTS animals')

    # Создаем таблицу пользователей
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE, 
        phone TEXT NOT NULL
    )
    ''')

    # Создаем таблицу животных с необходимыми столбцами
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS animals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        type TEXT NOT NULL,
        owner TEXT NOT NULL,
        price REAL NOT NULL DEFAULT 1500,
        days INTEGER NOT NULL DEFAULT 1,
        total_price REAL NOT NULL DEFAULT 1500
    )
    ''')

    conn.commit()
    conn.close()

# Регистрация нового пользователя
def register_user(username, password, first_name, last_name, email, phone):
    # Подключаемся к базе данных
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Проверяем, существует ли уже пользователь с таким же именем пользователя или электронной почтой
    cursor.execute('SELECT * FROM users WHERE username=? OR email=?', (username, email))
    user = cursor.fetchone()
    if user:
        conn.close()
        return False  # Возвращаем False, если пользователь уже существует

    # Вставляем нового пользователя в таблицу users
    cursor.execute('''
    INSERT INTO users (username, password, first_name, last_name, email, phone)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (username, password, first_name, last_name, email, phone))
    
    conn.commit()
    conn.close()
    
    return True  # Возвращаем True, если регистрация прошла успешно

# Загрузка изображения для страницы
def load_image(page):
    try:
        return ft.Image(src="d1.jpg", width=page.window.width, height=page.window.height, fit=ft.ImageFit.COVER)
    except Exception as e:
        print(f"Ошибка загрузки изображения: {e}")
        return ft.Text("Ошибка загрузки изображения", color=ft.colors.RED)

# Открытие окна регистрации
def open_register(page):
    print("Открываю окно регистрации")
    registration_window(page)

# Открытие окна входа
def open_login(page):
    print("Открываю окно входа")
    login_window(page)

# Окно входа и регистрации
def login_register_window(page):
    page.title = "Вход и регистрация"
    image = load_image(page)

    # Создаем полупрозрачный контейнер для затемнения
    overlay = ft.Container(
        bgcolor=ft.colors.BLACK54,
        width=page.window.width,
        height=page.window.height,
    )

    # Кнопки регистрации и входа
    register_button = ft.ElevatedButton(text="Регистрация", on_click=lambda e: open_register(page))
    login_button = ft.ElevatedButton(text="Войти", on_click=lambda e: open_login(page))

    # Контейнер для кнопок
    button_container = ft.Column(
        [register_button, login_button],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=10,
    )

    button_panel = ft.Container(
        content=button_container,
        bgcolor="#808080B3",  # Цвет фона кнопок
        border_radius=10,     # Скругление углов
        padding=20,           # Отступы внутри контейнера
        width=300,            # Ширина панели
        height=150,           # Высота панели
        border=ft.border.all(2, ft.colors.BLACK),
        alignment=ft.Alignment(0, 0)  # Центрирование внутри контейнера
    )

    # Добавляем все элементы в стек
    page.add(ft.Stack([image, overlay, ft.Container(content=button_panel, alignment=ft.Alignment(0, 0), width=page.window.width, height=page.window.height)]))

# Окно регистрации
def registration_window(page):
    page.clean()
    page.title = "Регистрация"

    # Поля для ввода данных
    username_input = ft.TextField(label="Имя пользователя", width=300)
    password_input = ft.TextField(label="Пароль", password=True, width=300)
    first_name_input = ft.TextField(label="Имя", width=300)
    last_name_input = ft.TextField(label="Фамилия", width=300)
    email_input = ft.TextField(label="Электронная почта", width=300)
    phone_input = ft.TextField(label="Телефон", width=300)
    message = ft.Text("", color=ft.colors.RED)

    # Функция регистрации
    def register(e):
        if not username_input.value or not password_input.value or not first_name_input.value or \
           not last_name_input.value or not email_input.value or not phone_input.value:
            message.value = "Пожалуйста, заполните все поля."
            page.update()
            return

        if register_user(username_input.value, password_input.value, first_name_input.value,
                         last_name_input.value, email_input.value, phone_input.value):
            message.value = "Регистрация прошла успешно!"
            page.update()
            open_animals_window(page)
            
            # Очистка полей
            username_input.value = ""
            password_input.value = ""
            first_name_input.value = ""
            last_name_input.value = ""
            email_input.value = ""
            phone_input.value = ""
        else:
            message.value = "Имя пользователя или электронная почта уже заняты."
        
        page.update()

    # Кнопка регистрации
    register_button = ft.ElevatedButton(text="Зарегистрироваться", on_click=register)

    # Вывод формы
    page.add(
        ft.Container(
            content=ft.Column(
                [
                    username_input,
                    password_input,
                    first_name_input,
                    last_name_input,
                    email_input,
                    phone_input,
                    register_button,
                    message,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10,
            ),
            alignment=ft.Alignment(0, 0),
            width=page.window_width,
            height=page.window_height,
        )
    )

# Окно входа
def login_window(page):
    page.clean()
    page.title = "Вход"

    # Поля для ввода данных
    username_input = ft.TextField(label="Имя пользователя", width=300)
    password_input = ft.TextField(label="Пароль", password=True, width=300)
    message = ft.Text("", color=ft.colors.RED)

    # Функция входа
    def login(e):
        if check_user(username_input.value, password_input.value):
            message.value = "Вход успешен!"
            page.clean()
            open_animals_window(page)
        else:
            message.value = "Неверное имя пользователя или пароль."
        page.update()

    # Кнопка для входа
    login_button = ft.ElevatedButton(text="Войти", on_click=login)

    # Вывод формы
    page.add(
        ft.Container(
            content=ft.Column(
                [
                    username_input,
                    password_input,
                    login_button,
                    message,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10,
            ),
            alignment=ft.Alignment(0, 0),
            width=page.window_width,
            height=page.window_height,
        )
    )

# Проверка пользователя
def check_user(username, password):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
    user = cursor.fetchone()
    conn.close()
    return user is not None


# Окно для добавления животных
def open_animals_window(page):
    page.clean()
    page.title = "Гостиница для животных"

    # Загрузка изображения
    animal_image = ft.Image(src="d2.jpg", width=400, height=300,  fit=ft.ImageFit.FILL) 
    # Ввод для добавления животного
    animal_name_input = ft.TextField(label="Имя животного", width=300)
    animal_type_input = ft.TextField(label="Тип животного", width=300)
    owner_name_input = ft.TextField(label="Имя и Фамилия владельца", width=300)
    days_input = ft.TextField(label="Количество дней", width=300, keyboard_type=ft.KeyboardType.NUMBER)

    message = ft.Text("", color=ft.colors.RED)

    # Фиксированная цена за ден
    fixed_price_per_day = 1200
    # Функция добавления животного
    def add_animal(e):
        if not animal_name_input.value or not animal_type_input.value or not owner_name_input.value or not days_input.value:
            message.value = "Все поля должны быть заполнены."
            page.update()
            return

        # Вычисление общей стоимости с фиксированной ценой за день
        try:
            days = int(days_input.value)
            total_price = fixed_price_per_day * days
        except ValueError:
            message.value = "Количество дней должно быть числом."
            page.update()
            return

        # Добавление животного в базу данных
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO animals (name, type, owner, price, days, total_price)
                          VALUES (?, ?, ?, ?, ?, ?)''', 
                       (animal_name_input.value, animal_type_input.value, owner_name_input.value, fixed_price_per_day, days, total_price))
        conn.commit()
        conn.close()

        # Вывод сообщения об успехе
        message.value = f"Животное добавлено! Общая стоимость: {total_price} руб."
        page.update()

        # Очистка полей
        animal_name_input.value = ""
        animal_type_input.value = ""
        owner_name_input.value = ""
        days_input.value = ""

        # Обновление списка животных
        update_animal_list(page)

    # Кнопка для добавления животного
    add_button = ft.ElevatedButton(text="Добавить животное", on_click=add_animal)

    # Вывод формы для добавления животного
    page.add(
        ft.Stack(
            [
                # Контейнер с изображением, выравнивание в верхний левый угол
                ft.Container(content=animal_image, alignment=ft.Alignment(0, 0), width=550, height=250),
                ft.Container(
                    content=ft.Column(
                        [
                            animal_name_input,
                            animal_type_input,
                            owner_name_input,
                            days_input,
                            add_button,
                            message,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=10,
                    ),
                    alignment=ft.Alignment(0, 0),
                    width=page.window_width,
                    height=page.window_height,
                ),
            ]
        )
    )

    # Обновление списка животных
    update_animal_list(page)

# Обновление списка животных
def update_animal_list(page):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name, type, owner, total_price FROM animals')
    animals = cursor.fetchall()
    conn.close()

    # Формируем список животных в виде списка объектов Text
    animal_list = []
    for animal in animals:
        # Оборачиваем каждую строку в компонент Text
        animal_text = ft.Text(f"{animal[0]} ({animal[1]}) - {animal[2]} - Цена: {animal[3]} руб.")
        animal_list.append(animal_text)

    # Отображаем список на странице
    page.add(ft.Column(animal_list, spacing=5))
    page.update()


# Инициализация базы данных
init_db()

# Запуск приложения
ft.app(target=login_register_window)