import telebot  # импортируем библиотеку для создания ТГ-ботов
from telebot import types  # импортируем модуль для создания кнопок чата
import random
import requests
from bs4 import BeautifulSoup

bot = telebot.TeleBot('')  # присваиваем токен бота из ТГ

# обработчик для считывания команд пользователя
@bot.message_handler(commands=['help'])
def helper(message):
    help_message = '<b>/mem_cats</b> - показывает рандомный мемчик с котиками\n' \
                           '<b>/who_are_you_today</b> - показывает какой ты сегодня пингвинчик\n' \
                           '<b>/horoscope</b> - максимально точно предсказывает будущее пользуясь \n' \
                           'гороскопом с horo.mail.ru'
    bot.send_message(message.chat.id, help_message, parse_mode='html')


@bot.message_handler(commands=['start'])
def start(message):
    send_mess = f'Привет <b>{message.from_user.first_name}</b>! Ну что? Глянем рандомный мемчик с котиками, посмотрим' \
                        ' какой ты сегодня пингвинчик или вообще, заглянем в будущее почитав сегодняшний гороскоп?'
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    # параметры: 1 - размер кнопок одинаковый на компе и телефоне, 2 - количество кнопок в строке - 3 шт
    help_button = types.KeyboardButton('/help')
    start_button = types.KeyboardButton('/start')
    mem_cats_button = types.KeyboardButton('/mem_cats')
    horoscope_button = types.KeyboardButton('/horoscope')
    who_are_you_today_button = types.KeyboardButton('/who_are_you_today')
    markup.add(help_button, mem_cats_button, who_are_you_today_button, horoscope_button)
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


#  отправляем пользователю гороскоп с сайта https://horo.mail.ru/
@bot.message_handler(commands=['horoscope'])
def horoscope(message):
    # Пишем приветствие
    send_mess = f"<b>{message.from_user.first_name}</b>! \nCейчас я расскажу тебе гороскоп на сегодня. Не унывай," \
                        ' давай посмотрим, может там что-то хорошее!'
    bot.send_message(message.chat.id, send_mess, parse_mode='html')
    # Готовим кнопки
    keyboard = types.InlineKeyboardMarkup()
    # По очереди готовим текст, обработчик для каждого знака зодиака и добавляем кнопки на экран
    key_oven = types.InlineKeyboardButton(text='♈️ Овен ♈️', callback_data='oven')
    keyboard.add(key_oven)
    key_telec = types.InlineKeyboardButton(text='♉️ Телец ♉️', callback_data='telec')
    keyboard.add(key_telec)
    key_bliznecy = types.InlineKeyboardButton(text='♊️ Близнецы ♊️', callback_data='bliznecy')
    keyboard.add(key_bliznecy)
    key_rak = types.InlineKeyboardButton(text='♋️ Рак ♋️', callback_data='rak')
    keyboard.add(key_rak)
    key_lev = types.InlineKeyboardButton(text='♌️ Лев ♌️', callback_data='lev')
    keyboard.add(key_lev)
    key_deva = types.InlineKeyboardButton(text='♍️ Дева ♍️', callback_data='deva')
    keyboard.add(key_deva)
    key_vesy = types.InlineKeyboardButton(text='♎️ Весы ♎️', callback_data='vesy')
    keyboard.add(key_vesy)
    key_scorpion = types.InlineKeyboardButton(text='♏️ Скорпион ♏️', callback_data='scorpion')
    keyboard.add(key_scorpion)
    key_strelec = types.InlineKeyboardButton(text='♐️ Стрелец ♐️', callback_data='strelec')
    keyboard.add(key_strelec)
    key_kozerog = types.InlineKeyboardButton(text='♑️ Козерог ♑️', callback_data='kozerog')
    keyboard.add(key_kozerog)
    key_vodoley = types.InlineKeyboardButton(text='♒️ Водолей ♒️', callback_data='vodoley')
    keyboard.add(key_vodoley)
    key_ryby = types.InlineKeyboardButton(text='♓️ Рыбы ♓️', callback_data='ryby')
    keyboard.add(key_ryby)
    # Показываем все кнопки сразу и пишем сообщение о выборе
    bot.send_message(message.from_user.id, text='Напомни мне свой знак зодиака!', reply_markup=keyboard)


# Обработчик нажатий на кнопки
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    # Если нажали на одну из 12 кнопок — выводим гороскоп
    if call.data == "oven":
        # Парсим гороскоп
        url = 'https://horo.mail.ru/prediction/aries/today/'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        quotes = soup.find_all('div''', class_='article__text')
        for quote in quotes:
            # Отправляем текст в Телеграм
            bot.send_message(call.message.chat.id, quote.text)
    elif call.data == "telec":
        url = 'https://horo.mail.ru/prediction/taurus/today/'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        quotes = soup.find_all('div''', class_='article__text')
        for quote in quotes:
            bot.send_message(call.message.chat.id, quote.text)
    elif call.data == "bliznecy":
        url = 'https://horo.mail.ru/prediction/gemini/today/'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        quotes = soup.find_all('div''', class_='article__text')
        for quote in quotes:
            bot.send_message(call.message.chat.id, quote.text)
    elif call.data == "rak":
        url = 'https://horo.mail.ru/prediction/cancer/today/'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        quotes = soup.find_all('div''', class_='article__text')
        for quote in quotes:
            bot.send_message(call.message.chat.id, quote.text)
    elif call.data == "lev":
        url = 'https://horo.mail.ru/prediction/leo/today/'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        quotes = soup.find_all('div''', class_='article__text')
        for quote in quotes:
            bot.send_message(call.message.chat.id, quote.text)
    elif call.data == "deva":
        url = 'https://horo.mail.ru/prediction/virgo/today/'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        quotes = soup.find_all('div''', class_='article__text')
        for quote in quotes:
            bot.send_message(call.message.chat.id, quote.text)
    elif call.data == "vesy":
        url = 'https://horo.mail.ru/prediction/libra/today/'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        quotes = soup.find_all('div''', class_='article__text')
        for quote in quotes:
            bot.send_message(call.message.chat.id, quote.text)
    elif call.data == "scorpion":
        url = 'https://horo.mail.ru/prediction/scorpio/today/'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        quotes = soup.find_all('div''', class_='article__text')
        for quote in quotes:
            bot.send_message(call.message.chat.id, quote.text)
    elif call.data == "strelec":
        url = 'https://horo.mail.ru/prediction/sagittarius/today/'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        quotes = soup.find_all('div''', class_='article__text')
        for quote in quotes:
            bot.send_message(call.message.chat.id, quote.text)
    elif call.data == "kozerog":
        url = 'https://horo.mail.ru/prediction/capricorn/today/'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        quotes = soup.find_all('div''', class_='article__text')
        for quote in quotes:
            bot.send_message(call.message.chat.id, quote.text)
    elif call.data == "vodoley":
        url = 'https://horo.mail.ru/prediction/aquarius/today/'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        quotes = soup.find_all('div''', class_='article__text')
        for quote in quotes:
            bot.send_message(call.message.chat.id, quote.text)
    elif call.data == "ryby":
        url = 'https://horo.mail.ru/prediction/pisces/today/'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        quotes = soup.find_all('div''', class_='article__text')
        for quote in quotes:
            bot.send_message(call.message.chat.id, quote.text)

#  устанавливаем запуск проекта на постоянную работу
bot.polling(none_stop=True)
