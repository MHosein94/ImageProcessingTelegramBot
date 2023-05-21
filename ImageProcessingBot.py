import telebot
from telebot import types
from datetime import datetime as dt
import FaceMakeup
import requests

Token = '*********************'

bot = telebot.TeleBot(Token)

@bot.message_handler(commands=['start'])
def getPic(message):
    bot.reply_to(message, 'Send Your Photo!')


@bot.message_handler(content_types=['photo'])
def getPicture(message):
    photo_info = bot.get_file(file_id=message.photo[-1].file_id)
    message_id = bot.send_message(chat_id=message.from_user.id, text='Receiving the Photo...').message_id
    photo_path = f'https://api.telegram.org/file/bot{Token}/{photo_info.file_path}'
    photo = requests.get(photo_path)

    bot.delete_message(message.from_user.id, message_id)
    message_id = bot.send_message(chat_id=message.from_user.id, text='Processing the Photo...').message_id

    now = str(dt.now().day) + str(dt.now().hour) + str(dt.now().minute) + str(dt.now().second) + str(dt.now().microsecond)
    file_name = f'New Image - {now}.jpg'
    with open(file_name, 'wb') as f:
        f.write(photo.content)
    makeupFileName = FaceMakeup.makeup(file_name)

    makeup_image = open(makeupFileName, 'rb')
    bot.delete_message(message.from_user.id, message_id)
    message_id = bot.send_message(chat_id=message.from_user.id, text='Sending the Photo').message_id
    bot.send_chat_action(chat_id=message.from_user.id, action='upload_photo')
    bot.send_photo(chat_id=message.from_user.id, photo=makeup_image)
    bot.delete_message(message.from_user.id, message_id)

bot.polling()
