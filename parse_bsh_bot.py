import os
import sqlite3
import telebot
from telebot import types
from mod_parse_portal import parse_and_store_data_from_portal
from mod_docx import parse_and_store_docx
from main import find_differences, get_biz_sherif_table
from token_bot import BOT_TOKEN

# токен бота
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Проверить файл .docx")
    item2 = types.KeyboardButton("Текущий список БШ")
    markup.add(item1, item2)
    bot.send_message(message.chat.id, "Привет! Я бот для анализа файлов .docx. Выберите действие:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "Текущий список БШ")
def send_biz_sherif_table(message):
    biz_sherif_table = get_biz_sherif_table()  # Получите текст таблицы (например, в виде строки)

    # Сохраните текст таблицы в файл
    with open('biz_sherif.txt', 'w', encoding='utf-8') as file:
        file.write(biz_sherif_table)

    # Отправьте файл пользователю
    with open('biz_sherif.txt', 'rb') as file:
        bot.send_document(message.chat.id, file)

    # Удалите временный файл
    os.remove('biz_sherif.txt')

@bot.message_handler(func=lambda message: message.text == "Проверить файл .docx")
def ask_for_docx(message):
    bot.send_message(message.chat.id, "Пришлите мне файл .docx для анализа.")

@bot.message_handler(content_types=['document'])
def handle_document(message):
    try:
        # Сохраняем полученный файл
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        file_name = message.document.file_name

        with open(file_name, 'wb') as new_file:
            new_file.write(downloaded_file)

        # Выполняем операции с файлом
        parse_and_store_data_from_portal()
        parse_and_store_docx(file_name)
        find_differences()

        # Отправляем результат обратно в Telegram как файл
        with open('differences.txt', 'r', encoding='cp1251') as result_file:
            # bot.send_document(message.chat.id, result_file)
            bot.send_document(message.chat.id, result_file, caption="Результат анализа файлов", parse_mode="HTML",
                              reply_to_message_id=message.message_id)

        # Удаляем файлы
        os.remove(file_name)
        os.remove('differences.txt')

    except Exception as e:
        bot.reply_to(message, f'Произошла ошибка: {str(e)}')

if __name__ == '__main__':
    bot.polling()