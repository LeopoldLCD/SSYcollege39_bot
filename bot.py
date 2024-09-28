import telebot
from telebot import types
import os

# Ваш токен
token = NONE
bot = telebot.TeleBot(token)

# Путь для сохранения логов
LOG_DIR = 'logs'
USERS_FILE = 'users.txt'

# Создаём директорию для логов, если её нет
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)


# Функция для логирования сообщений каждого пользователя в отдельный файл
def log_message(message):
    user_id = message.from_user.id
    log_file = os.path.join(LOG_DIR, f'{user_id}.txt')
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"{message.from_user.first_name} ({message.from_user.id}): {message.text}\n")


# Функция для сохранения уникальных пользователей
def save_user(user):
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'w', encoding='utf-8') as f:
            f.write(f"{user.id}\n")
    else:
        with open(USERS_FILE, 'r+', encoding='utf-8') as f:
            users = f.readlines()
            user_data = f"{user.id}\n"
            if user_data not in users:  # Проверка, чтобы избежать дублирования пользователей
                f.write(user_data)


# Функция для получения списка пользователей из файла
def get_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            users = f.readlines()
            return [int(user.strip()) for user in users]
    return []


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start_message(message):
    log_message(message)
    save_user(message.from_user)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    but1 = types.KeyboardButton("Рассписание🗓")
    but2 = types.KeyboardButton("Задать вопрос ССУ❓")
    but3 = types.KeyboardButton("Предложения/Идеи💡")
    but4 = types.KeyboardButton("Авторы©️")

    markup.row(but1)
    markup.row(but2)
    markup.row(but3)
    markup.row(but4)

    bot.send_message(message.chat.id, f"Привет, {message.from_user.first_name}! \nВыбери нужную опцию:",
                     reply_markup=markup)


# Обработчик текстовых сообщений
@bot.message_handler(content_types='text')
def message_reply(message):
    log_message(message)
    save_user(message.from_user)

    if message.text == "Рассписание🗓":
        markupmes = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton("Расписание", url=NONE)
        markupmes.row(button1)
        bot.send_message(message.chat.id, 'Здесь вы можете посмотреть рассписание', reply_markup=markupmes)

    elif message.text == "Задать вопрос ССУ❓":
        markupmes = types.InlineKeyboardMarkup()
        button2 = types.InlineKeyboardButton("Задать вопрос ССУ", url=NONE)
        markupmes.row(button2)
        bot.send_message(message.chat.id, 'Здесь вы можете задать вопрос', reply_markup=markupmes)

    elif message.text == "Предложения/Идеи💡":
        markupmes = types.InlineKeyboardMarkup()
        button3 = types.InlineKeyboardButton("Предложения/Идеи", url=NONE)
        markupmes.row(button3)
        bot.send_message(message.chat.id, 'Здесь вы можете оставить предложения или идеи', reply_markup=markupmes)

    elif message.text == "Авторы©️":
        bot.send_message(message.chat.id, "Автор этого бота:\nNONE\n\n"
                                          "Авторы бота с расписанием:\n"
                                          "NONE\n"
                                          "NONE")

    # Оповещения всем пользователям: NONE <сообщение>
    elif message.text.startswith(NONE):
        notification_message = message.text[len(NONE):]  # Получаем сообщение для рассылки
        send_notifications(notification_message)
        bot.send_message(message.chat.id, 'Оповещение отправлено всем пользователям.')

    # Личное сообщение пользователю: NONE <id> <сообщение>
    elif message.text.startswith(NONE):
        try:
            parts = message.text.split(maxsplit=2)
            user_id = int(parts[1])
            personal_message = parts[2]
            send_personal_message(user_id, personal_message)
            bot.send_message(message.chat.id, f'Сообщение отправлено пользователю с ID {user_id}.')
        except (IndexError, ValueError):
            bot.send_message(message.chat.id, 'Неправильный формат команды. Используйте NONE <id> <сообщение>.')


# Функция для отправки оповещений всем пользователям
def send_notifications(notification_message):
    users = get_users()
    for user_id in users:
        try:
            bot.send_message(user_id, notification_message)
        except Exception as e:
            print(f"Не удалось отправить сообщение пользователю {user_id}: {e}")


# Функция для отправки личного сообщения
def send_personal_message(user_id, message):
    try:
        bot.send_message(user_id, message)
    except Exception as e:
        print(f"Не удалось отправить личное сообщение пользователю {user_id}: {e}")


# Запуск бота
bot.infinity_polling()
