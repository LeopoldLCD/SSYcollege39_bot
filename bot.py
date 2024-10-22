import telebot
from telebot import types
import os
import time
import threading

# Токен вашего бота (рекомендуется использовать переменные окружения)
TOKEN = 'NONE'
bot = telebot.TeleBot(TOKEN)

SUPPORT_ID = 'NONE'  # Получаем из переменной окружения
# Путь к лог-файлам
USERS_LOG_FILE = 'users_log.txt'
QUESTIONS_LOG_FILE = 'questions_log.txt'
IDEAS_LOG_FILE = 'ideas_log.txt'
user_ids = set()  # Используем множество для уникальности ID пользователей

# Функция для инициализации ID пользователей из лог-файла
def initialize_user_ids():
    if os.path.exists(USERS_LOG_FILE):
        with open(USERS_LOG_FILE, 'r') as f:
            for line in f:
                user_id = line.strip().split(": ")[1]  # Предполагается, что строка вида "ID: <id>"
                user_ids.add(user_id)

# Функция для добавления пользователя в лог
def log_user(user_id):
    if user_id in user_ids:  # Проверяем, есть ли ID в множестве
        # Если пользователь уже в логах, можно, например, вывести сообщение
        print(f"Пользователь с ID {user_id} уже существует в логах. Удаляем повторный.")
        remove_user_from_log(user_id)  # Удаляем старую запись

    with open(USERS_LOG_FILE, 'a') as f:
        f.write(f"ID: {user_id}\n")
    user_ids.add(user_id)  # Добавляем ID в множество

# Функция для удаления пользователя из лога
def remove_user_from_log(user_id):
    # Создаем временный файл для записи всех пользователей, кроме удаляемого
    temp_file = 'temp_users_log.txt'
    with open(USERS_LOG_FILE, 'r') as original:
        with open(temp_file, 'w') as new_file:
            for line in original:
                if line.strip() != f"ID: {user_id}":
                    new_file.write(line)
    # Заменяем старый файл новым
    os.replace(temp_file, USERS_LOG_FILE)


@bot.message_handler(commands=['all'])
def broadcast_message(message):
    if message.from_user.id != int(SUPPORT_ID):
        bot.send_message(message.chat.id, "У вас нет прав для выполнения этой команды.")
        return

    # Запрашиваем текст и изображение
    bot.send_message(message.chat.id, "Введите текст для рассылки:")
    bot.register_next_step_handler(message, process_broadcast_text)


def process_broadcast_text(message):
    broadcast_text = message.text
    bot.send_message(message.chat.id, "Пожалуйста, отправьте изображение для рассылки.")
    bot.register_next_step_handler(message, process_broadcast_image, broadcast_text)


def process_broadcast_image(message, broadcast_text):
    if message.content_type != 'photo':
        bot.send_message(message.chat.id, "Пожалуйста, отправьте изображение.")
        bot.register_next_step_handler(message, process_broadcast_image, broadcast_text)
        return

    image_file_id = message.photo[-1].file_id
    bot.send_message(message.chat.id, "Начинаем рассылку...")

    threading.Thread(target=send_broadcast, args=(broadcast_text, image_file_id)).start()


def send_broadcast(text, image_file_id):
    for user_id in user_ids:
        try:
            bot.send_photo(user_id, image_file_id, text)
            time.sleep(1)  # Задержка в 1 секунду между отправками
        except Exception as e:
            print(f"Не удалось отправить сообщение пользователю {user_id}: {e}")


# Функция для записи вопросов в лог
def log_question(content):
    with open(QUESTIONS_LOG_FILE, 'a') as f:
        f.write(content + "\n")

# Функция для записи предложений в лог
def log_idea(content):
    with open(IDEAS_LOG_FILE, 'a') as f:
        f.write(content + "\n")

# Команда /start - приветствие и панель кнопок
@bot.message_handler(commands=['start'])
def send_welcome(message):
    log_user(message.chat.id)  # Логирование пользователя
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_question = types.KeyboardButton("❓ Задать вопрос ССУ")
    btn_idea = types.KeyboardButton("💡 Предложение/Замечание")
    btn_authors = types.KeyboardButton("👥 Авторы")
    markup.row(btn_question)
    markup.row(btn_idea)
    markup.row(btn_authors)

    bot.send_message(
        message.chat.id,
        f"Привет, {message.from_user.username}! Выберите одну из опций:",
        reply_markup=markup
    )

# Обработчик кнопки "❓ Задать вопрос ССУ"
@bot.message_handler(func=lambda message: message.text == "❓ Задать вопрос ССУ")
def ask_question(message):
    markup = types.InlineKeyboardMarkup()
    fill_btn = types.InlineKeyboardButton(text="Заполнить", callback_data="fill_question")
    cancel_btn = types.InlineKeyboardButton(text="Отменить", callback_data="cancel")
    markup.add(fill_btn, cancel_btn)

    bot.send_message(message.chat.id, "Заполните следующую форму, чтобы задать вопрос:", reply_markup=markup)

# Обработчик кнопки "💡 Предложение/Замечание"
@bot.message_handler(func=lambda message: message.text == "💡 Предложение/Замечание")
def submit_idea(message):
    markup = types.InlineKeyboardMarkup()
    fill_btn = types.InlineKeyboardButton(text="Заполнить", callback_data="fill_idea")
    cancel_btn = types.InlineKeyboardButton(text="Отменить", callback_data="cancel")
    markup.add(fill_btn, cancel_btn)

    bot.send_message(message.chat.id, "Заполните следующую форму, чтобы предложить вашу идею:", reply_markup=markup)

# Обработчик кнопки "👥 Авторы"
@bot.message_handler(func=lambda message: message.text == "👥 Авторы")
def authors(message):
    markupmes = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("ТГК с кодом", url="https://t.me/leohub_hack")
    markupmes.row(button1)
    bot.send_message(message.chat.id, 'Автор бота:\nБахтин Леонид - @SupSSYcollege', reply_markup=markupmes)

# Обработка нажатий кнопок "Заполнить" и "Отменить"
@bot.callback_query_handler(func=lambda call: call.data.startswith("fill") or call.data == "cancel")
def handle_callbacks(call):
    if call.data == "cancel":
        bot.delete_message(call.message.chat.id, call.message.message_id)
    elif call.data == "fill_question":
        bot.send_message(call.message.chat.id, "Ваше ФИО:")
        bot.register_next_step_handler(call.message, process_fio_question)
    elif call.data == "fill_idea":
        bot.send_message(call.message.chat.id, "Ваше ФИО:")
        bot.register_next_step_handler(call.message, process_fio_idea)

# Процесс заполнения формы "Задать вопрос ССУ"
def process_fio_question(message):
    user_data = {'fio': message.text}
    bot.send_message(message.chat.id, "Номер вашей группы:")
    bot.register_next_step_handler(message, process_group_question, user_data)

def process_group_question(message, user_data):
    user_data['group'] = message.text
    bot.send_message(message.chat.id, "Ваш вопрос?")
    bot.register_next_step_handler(message, process_question, user_data)

def process_question(message, user_data):
    user_data['question'] = message.text
    bot.send_message(message.chat.id, "Спасибо! Ваш вопрос отправлен в техподдержку.")

    # Логируем вопрос
    log_question(f"Задать вопрос ССУ\nФИО: {user_data['fio']}\nГруппа: {user_data['group']}\nВопрос: {user_data['question']}\nПользователь: @{message.from_user.username}, ID: {message.chat.id} \n")

    # Отправляем информацию техподдержке
    send_to_support(f"Задать вопрос ССУ\nФИО: {user_data['fio']}\nГруппа: {user_data['group']}\nВопрос: {user_data['question']}", message)

# Процесс заполнения формы "Предложение/замечание"
def process_fio_idea(message):
    user_data = {'fio': message.text}
    bot.send_message(message.chat.id, "Номер вашей группы:")
    bot.register_next_step_handler(message, process_group_idea, user_data)

def process_group_idea(message, user_data):
    user_data['group'] = message.text
    bot.send_message(message.chat.id, "Ваше предложение?")
    bot.register_next_step_handler(message, process_idea, user_data)

def process_idea(message, user_data):
    user_data['idea'] = message.text
    bot.send_message(message.chat.id, "Спасибо! Ваше предложение/замечание отправлено в техподдержку.")

    # Логируем идею
    log_idea(f"Предложение/замечание\nФИО: {user_data['fio']}\nГруппа: {user_data['group']}\nИдея: {user_data['idea']}\nПользователь: @{message.from_user.username}, ID: {message.chat.id} \n")

    # Отправляем информацию техподдержке
    send_to_support(f"Предложение/замечание\nФИО: {user_data['fio']}\nГруппа: {user_data['group']}\nИдея: {user_data['idea']}", message)

# Отправка данных техподдержке
def send_to_support(content, message):
    markup = types.InlineKeyboardMarkup()
    reply_btn = types.InlineKeyboardButton(text="Ответить", callback_data=f"reply_{message.chat.id}")
    cancel_btn = types.InlineKeyboardButton(text="Отменить", callback_data="cancel")
    markup.add(reply_btn, cancel_btn)

    bot.send_message(SUPPORT_ID, f"{content}\n\nПользователь: @{message.from_user.username}\nID: {message.chat.id}", reply_markup=markup)

# Обработка ответа от техподдержки
@bot.callback_query_handler(func=lambda call: call.data.startswith("reply_"))
def handle_support_reply(call):
    user_id = int(call.data.split("_")[1])
    bot.send_message(call.message.chat.id, "Что вы хотите ответить пользователю?")
    bot.register_next_step_handler(call.message, send_reply_to_user, user_id)

def send_reply_to_user(message, user_id):
    bot.send_message(user_id, f"Ответ от техподдержки: {message.text}")
    bot.send_message(SUPPORT_ID, "Ответ отправлен пользователю.")

# Команда для вывода логов вопросов
@bot.message_handler(commands=['question_log'])
def broadcast_message(message):
    if message.from_user.id != int(SUPPORT_ID):
        bot.send_message(message.chat.id, "У вас нет прав для выполнения этой команды.")
        return
def send_questions_log(message):
    if os.path.exists(QUESTIONS_LOG_FILE):
        with open(QUESTIONS_LOG_FILE, 'r') as f:
            bot.send_message(message.chat.id, f.read())
    else:
        bot.send_message(message.chat.id, "Лог вопросов пуст.")

# Команда для вывода логов предложений
@bot.message_handler(commands=['ideas_log'])
def broadcast_message(message):
    if message.from_user.id != int(SUPPORT_ID):
        bot.send_message(message.chat.id, "У вас нет прав для выполнения этой команды.")
        return
def send_ideas_log(message):
    if os.path.exists(IDEAS_LOG_FILE):
        with open(IDEAS_LOG_FILE, 'r') as f:
            bot.send_message(message.chat.id, f.read())
    else:
        bot.send_message(message.chat.id, "Лог предложений пуст.")


# Функция для удаления повторяющихся ID из лога
def clear_duplicate_ids():
    unique_ids = set()
    temp_file = 'temp_users_log.txt'

    # Читаем из оригинального файла и сохраняем уникальные ID в временный файл
    with open(USERS_LOG_FILE, 'r') as original:
        with open(temp_file, 'w') as new_file:
            for line in original:
                user_id = line.strip().split(": ")[1]  # Предполагается, что строка вида "ID: <id>"
                if user_id not in unique_ids:
                    unique_ids.add(user_id)
                    new_file.write(line)

    # Заменяем старый файл новым
    os.replace(temp_file, USERS_LOG_FILE)
    print("Дубликаты удалены из логов.")


# Обработчик команды /clear
@bot.message_handler(commands=['clear'])
def clear_logs(message):
    if message.from_user.id != int(SUPPORT_ID):
        bot.send_message(message.chat.id, "У вас нет прав для выполнения этой команды.")
        return

    clear_duplicate_ids()  # Удаляем дубликаты из логов
    bot.send_message(message.chat.id, "Все дублирующиеся ID удалены из логов.")


# Инициализация ID пользователей при запуске бота
initialize_user_ids()
# Запуск бота
bot.polling(none_stop=True)
