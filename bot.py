import telebot
from telebot import types
import os

# Токен вашего бота (рекомендуется использовать переменные окружения)
TOKEN = 'NONE'
bot = telebot.TeleBot(TOKEN)


SUPPORT_ID = 'NONE'  # Получаем из переменной окружения
# Путь к лог-файлам
USERS_LOG_FILE = 'users_log.txt'
QUESTIONS_LOG_FILE = 'questions_log.txt'
IDEAS_LOG_FILE = 'ideas_log.txt'
user_ids = []

# Функция для загрузки ID пользователей из файла
def load_user_ids():
    global user_ids
    if os.path.exists(USERS_LOG_FILE):
        with open(USERS_LOG_FILE, 'r') as f:
            for line in f:
                user_id = line.split(",")[0].split(":")[1].strip()
                user_ids.append(user_id)

# Функция для добавления пользователя в лог
def log_user(user_id, username):
    with open(USERS_LOG_FILE, 'a') as f:
        f.write(f"ID: {user_id}, Username: {username}\n")


# Функция для записи вопросов в лог
def log_question(content):
    with open(QUESTIONS_LOG_FILE, 'a') as f:
        f.write(content + "\n")

# Функция для записи предложений в лог
def log_idea(content):
    with open(IDEAS_LOG_FILE, 'a') as f:
        f.write(content + "\n")

# Команда для отправки сообщения всем пользователям
@bot.message_handler(commands=['all'])
def broadcast_message(message):
    if str(message.chat.id) != SUPPORT_ID:  # Проверяем, что команду вызывает техподдержка
        bot.send_message(message.chat.id, "У вас нет прав для использования этой команды.")
        return

    msg = bot.send_message(message.chat.id, "Введите сообщение для рассылки:")
    bot.register_next_step_handler(msg, send_broadcast)

def send_broadcast(message):
    text = message.text
    for user_id in user_ids:
        try:
            bot.send_message(user_id, text)  # Отправляем сообщение каждому пользователю
            bot.send_message(message.chat.id, f"Сообщение отправлено пользователю с ID: {user_id}.")
        except Exception as e:
            bot.send_message(message.chat.id, f"Не удалось отправить сообщение пользователю {user_id}: {e}")

    bot.send_message(message.chat.id, "Рассылка завершена.")

# Загружаем ID пользователей при старте бота
load_user_ids()

# Команда /start - приветствие и панель кнопок
@bot.message_handler(commands=['start'])
def send_welcome(message):
    log_user(message.chat.id, message.from_user.username)  # Логирование пользователя
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
@bot.message_handler(commands=['NONE'])
def send_questions_log(message):
    if os.path.exists(QUESTIONS_LOG_FILE):
        with open(QUESTIONS_LOG_FILE, 'r') as f:
            bot.send_message(message.chat.id, f.read())
    else:
        bot.send_message(message.chat.id, "Лог вопросов пуст.")

# Команда для вывода логов предложений
@bot.message_handler(commands=['NONE'])
def send_ideas_log(message):
    if os.path.exists(IDEAS_LOG_FILE):
        with open(IDEAS_LOG_FILE, 'r') as f:
            bot.send_message(message.chat.id, f.read())
    else:
        bot.send_message(message.chat.id, "Лог предложений пуст.")

# Запуск бота
bot.polling(none_stop=True)
