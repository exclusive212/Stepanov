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
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS animals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        type TEXT NOT NULL,
        owner TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

# Регистрация нового пользователя
def register_user(username, password, first_name, last_name, email, phone):
    try:
        cursor.execute('INSERT INTO users (username, password, first_name, last_name, email, phone) VALUES (?, ?, ?, ?, ?, ?)',
                       (username, password, first_name, last_name, email, phone))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def load_image(page):
    try:
        image = ft.Image(src="d1.jpg", width=page.window.width, height=page.window.height, fit=ft.ImageFit.COVER)
        return image
    except Exception as e:
        print(f"Ошибка загрузки изображения: {e}")
        return None

def open_register(e):
    page.go('/register')

def open_login(e):
    page.go('/login')

def login_register_window(page):
    page.title = "Вход и регистрация"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    image = load_image(page)
    
    register_button = ft.ElevatedButton(text="Регистрация", on_click=open_register)
    login_button = ft.ElevatedButton(text="Войти", on_click=open_login)

    button_container = ft.Column(
        [register_button, login_button],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=10,
    )

    content = [
        image if image else ft.Text("Изображение не найдено"),
        ft.Container(
            content=button_container,
            alignment=ft.Alignment(0, 0),
            padding=20,
        ),
    ]
    
    page.add(ft.Stack(content))



    def open_register(e):
        registration_window(page)

    def open_login(e):
        login_window(page)

    register_button = ft.ElevatedButton(text="Регистрация", on_click=open_register)
    login_button = ft.ElevatedButton(text="Войти", on_click=open_login)

    # Создаем контейнер для кнопок, выравненных по центру
    button_container = ft.Column(
        [
            register_button,
            login_button,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=10,
    )

    # Добавляем картинку и кнопки в страницу
    page.add(
        ft.Stack(
            [
                image,
                ft.Container(
                    content=button_container,
                    alignment=ft.Alignment(0, 0),  # Центрируем кнопки
                    padding=20,  # Установка отступов
                ),
            ]
        )
    )

# Окно регистрации
def registration_window(page):
    page.clean()  # Очищаем текущее содержимое страницы
    page.title = "Регистрация"
    
    username_input = ft.TextField(label="Имя пользователя", width=300)
    password_input = ft.TextField(label="Пароль", password=True, width=300)
    first_name_input = ft.TextField(label="Имя", width=300)
    last_name_input = ft.TextField(label="Фамилия", width=300)
    email_input = ft.TextField(label="Электронная почта", width=300)
    phone_input = ft.TextField(label="Телефон", width=300)
    message = ft.Text("", color=ft.colors.RED)

    def register(e):
        if register_user(username_input.value, password_input.value, first_name_input.value, last_name_input.value, email_input.value, phone_input.value):
            message.value = "Регистрация прошла успешно!"
            page.update()
            open_animals_window(page)  # Переход в окно "Гостиница для животных"
        else:
            message.value = "Имя пользователя или электронная почта уже заняты."
        page.update()

    register_button = ft.ElevatedButton(text="Зарегистрироваться", on_click=register)

    page.add(
        ft.Column(
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
        )
    )

# Окно входа
def login_window(page):
    page.clean()  # Очищаем текущее содержимое страницы
    page.title = "Вход"
    
    username_input = ft.TextField(label="Имя пользователя", width=300)
    password_input = ft.TextField(label="Пароль", password=True, width=300)
    message = ft.Text("", color=ft.colors.RED)

    def login(e):
        if check_user(username_input.value, password_input.value):
            message.value = "Вход успешен!"
            page.clean()
            open_animals_window(page)
        else:
            message.value = "Неверное имя пользователя или пароль."
        page.update()

    login_button = ft.ElevatedButton(text="Войти", on_click=login)

    page.add(
        ft.Column(
            [
                username_input,
                password_input,
                login_button,
                message,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
        )
    )

# Окно "Гостиница для животных"
def open_animals_window(page):
    page.clean()  # Очищаем текущее содержимое страницы
    page.title = "Гостиница для животных"
    page.vertical_alignment = ft.MainAxisAlignment.START

    animal_name_input = ft.TextField(label="Имя животного", width=300)
    animal_type_input = ft.TextField(label="Тип животного", width=300)
    owner_name_input = ft.TextField(label="Имя владельца", width=300)

    def add_animal(e):
        if not animal_name_input.value or not animal_type_input.value or not owner_name_input.value:
            return  # Можно добавить сообщение об ошибке
        add_animal_to_db(animal_name_input.value, animal_type_input.value, owner_name_input.value)
        animal_name_input.value = ""
        animal_type_input.value = ""
        owner_name_input.value = ""
        update_animal_list()

    def update_animal_list():
        animal_list.controls.clear()
        animals = get_animals_from_db()
        for animal in animals:
            animal_list.controls.append(ft.Text(f"{animal[0]} ({animal[1]}) - Владелец: {animal[2]}"))
        page.update()

    add_animal_button = ft.ElevatedButton(text="Добавить животное", on_click=add_animal)

    animal_list = ft.Column()

    page.add(
        ft.Column(
            [
                animal_name_input,
                animal_type_input,
                owner_name_input,
                add_animal_button,
                ft.Text("Список животных:"),
                animal_list,
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=10,
        )
    )

    update_animal_list()

# Функция добавления животных в базу данных
def add_animal_to_db(name, animal_type, owner):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO animals (name, type, owner) VALUES (?, ?, ?)', (name, animal_type, owner))
    conn.commit()
    conn.close()

# Функция получения списка животных из базы данных
def get_animals_from_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name, type, owner FROM animals')
    animals = cursor.fetchall()
    conn.close()
    return animals

# Инициализация базы данных
init_db()

# Запуск окна регистрации и входа
ft.app(target=login_register_window)




