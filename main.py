import telebot  # импортируем библиотеку для создания ТГ-ботов
from telebot import types  # импортируем модуль для создания кнопок чата
import random

bot = telebot.TeleBot('5552249208:AAH_mcOSV1gvhDtwt9BbpkQNZPLUbtuVZFo')  # присваиваем токен бота из ТГ

#  считываем части текста из файлов в переменные для их будущей рандомной компоновки
#  в текст гороскопа
with open("first.txt", "r") as f1:
    first = f1.readlines()
with open("second.txt", "r") as f2:
    second = f2.readlines()
with open("second_add.txt", "r") as f2_add:
    second_add = f2_add.readlines()
with open("third.txt", "r") as f3:
    third = f3.readlines()


# обработчик для считывания команд пользователя
@bot.message_handler(commands=['help'])
def helper(message):
    help_message = '<b>/mem_cats</b> - показывает рандомный мемчик с котиками\n' \
                           '<b>/who_are_you_today</b> - показывает какой ты сегодня пингвинчик\n' \
                           '<b>/horoscope</b> - максимально точно предсказывает будущее, но только на один денёк'
    bot.send_message(message.chat.id, help_message, parse_mode='html')


@bot.message_handler(commands=['start'])
def start(message):
    send_mess = f'Привет <b>{message.from_user.first_name}</b>! Ну что? Глянем рандомный мемчик с котиками, посмотрим' \
                        ' какой ты сегодня пингвинчик или вообще, заглянем в будущее почитав сегодняшний гороскоп?'
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    # параметры: 1 - размер кнопок одинаковый на компе и телефоне, 2 - количество кнопок в строке - 3 шт
    help_button = types.KeyboardButton('/help')
    start_button = types.KeyboardButton('/start')
    mem_cats_button = types.KeyboardButton('/mem_cats')
    horoscope_button = types.KeyboardButton('/horoscope')
    who_are_you_today_button = types.KeyboardButton('/who_are_you_today')
    markup.add(help_button, start_button, mem_cats_button, who_are_you_today_button, horoscope_button)
    # через message.chat.id обращаемся к нашему с ботом чату, отправляем сообщение, формат отправки parse_mode
    # используем html чтобы иметь возможность управлять видом текста с помощью тагов
    bot.send_message(message.chat.id, send_mess, parse_mode='html', reply_markup=markup)


#  отправляет пользователю рандомно выбранный мем
@bot.message_handler(commands=['mem_cats'])
def mem_cats(message):
    mem = open('cat_mems/' + str(random.randint(1, 42)) + '.jpeg', 'rb')
    bot.send_photo(message.chat.id, mem)


#  отправляет пользователю рандомно выбранный статус-картинку
@bot.message_handler(commands=['who_are_you_today'])
def who_are_you_today(message):
    status_png = open('who_you/' + str(random.randint(1, 23)) + '.png', 'rb')
    bot.send_photo(message.chat.id, status_png)


#  отправляем пользователю гороскоп
@bot.message_handler(commands=['horoscope'])
def horoscope(message):
    # Пишем приветствие
    send_mess = f"<b>{message.from_user.first_name}</b>! \nCейчас я расскажу тебе гороскоп на сегодня. Не унывай," \
                        ' давай посмотрим, может там что-то хорошее!'
    bot.send_message(message.chat.id, send_mess, parse_mode='html')
    # Готовим кнопки
    keyboard = types.InlineKeyboardMarkup()
    # По очереди готовим текст и обработчик для каждого знака зодиака
    key_oven = types.InlineKeyboardButton(text='♈️ Овен ♈️', callback_data='zodiac')
    # И добавляем кнопку на экран
    keyboard.add(key_oven)
    key_telec = types.InlineKeyboardButton(text='♉️ Телец ♉️', callback_data='zodiac')
    keyboard.add(key_telec)
    key_bliznecy = types.InlineKeyboardButton(text='♊️ Близнецы ♊️', callback_data='zodiac')
    keyboard.add(key_bliznecy)
    key_rak = types.InlineKeyboardButton(text='♋️ Рак ♋️', callback_data='zodiac')
    keyboard.add(key_rak)
    key_lev = types.InlineKeyboardButton(text='♌️ Лев ♌️', callback_data='zodiac')
    keyboard.add(key_lev)
    key_deva = types.InlineKeyboardButton(text='♍️ Дева ♍️', callback_data='zodiac')
    keyboard.add(key_deva)
    key_vesy = types.InlineKeyboardButton(text='♎️ Весы ♎️', callback_data='zodiac')
    keyboard.add(key_vesy)
    key_scorpion = types.InlineKeyboardButton(text='♏️ Скорпион ♏️', callback_data='zodiac')
    keyboard.add(key_scorpion)
    key_strelec = types.InlineKeyboardButton(text='♐️ Стрелец ♐️', callback_data='zodiac')
    keyboard.add(key_strelec)
    key_kozerog = types.InlineKeyboardButton(text='♑️ Козерог ♑️', callback_data='zodiac')
    keyboard.add(key_kozerog)
    key_vodoley = types.InlineKeyboardButton(text='♒️ Водолей ♒️', callback_data='zodiac')
    keyboard.add(key_vodoley)
    key_ryby = types.InlineKeyboardButton(text='♓️ Рыбы ♓️', callback_data='zodiac')
    keyboard.add(key_ryby)
    # Показываем все кнопки сразу и пишем сообщение о выборе
    bot.send_message(message.from_user.id, text='Напомни мне свой знак зодиака!', reply_markup=keyboard)


# Обработчик нажатий на кнопки
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    # Если нажали на одну из 12 кнопок — выводим гороскоп
    if call.data == "zodiac":
        # Формируем гороскоп
        msg = random.choice(first) + ' ' + random.choice(second) + ' ' + random.choice(
            second_add) + ' ' + random.choice(third)
        msg = msg.replace("\n", "")
        # Отправляем текст в Телеграм
        bot.send_message(call.message.chat.id, msg)


#  устанавливаем запуск проекта на постоянную работу
bot.polling(none_stop=True)
