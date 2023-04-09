from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

button_register = KeyboardButton('Зарегестрироваться! 📃')
button_check = KeyboardButton('Посмотреть заявку! 📩')
button_call = KeyboardButton('Обратная связь 📲')
button_about = KeyboardButton('О нас  💁🏼‍')

greet_start = ReplyKeyboardMarkup(resize_keyboard=True)
greet_start.add(button_register)
greet_start.add(button_check)
greet_start.add(button_call)
greet_start.add(button_about)


button_med_center = None

share_key = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
share_buttuon = KeyboardButton(text="Поделиться номером 📱", request_contact=True)
share_key.add(share_buttuon)

class CustomInlineMarkup(InlineKeyboardMarkup):
    
    def __init__(self):
        super().__init__()