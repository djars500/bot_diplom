import os
from datetime import datetime

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove, ReplyKeyboardMarkup, \
    KeyboardButton
from aiogram.utils import executor
from aiogram.utils.callback_data import CallbackData

from keyboard import greet_start, share_key

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

import django

django.setup()
from main.models import MedicalCenter, Special, City, Employee, RegisterRequest

bot = Bot(token='5947757536:AAFVyZ0qSwIEdlSNrVDwf9vLKFFTBkXVNRI')
dp = Dispatcher(bot)

date_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
date_keyboard.add(KeyboardButton("Отправить дату"))

cb = CallbackData('med_center', 'item', 'id', 'message_id')

DESC = """Бот был создан для оптимизации регистрации в медицинских центрах

Для связи:
Почта: djars500@gmail.com 
Номер телефона: +7 708 953 1792
Адрес: Байтурсынова 18а, Шымкент"""

HELP_COMMAND = """
<b>/help</b> - <em>Список команд</em>
<b>/start</b> - <em>Старт бота</em>
<b>/callcenter</b> - <em>Справочник</em>
<b>/desc</b> - <em>Описание бота</em>
"""

register_request = {}


def get_text(reg):
    text = f'Заявка успешно создана \n ФИО: {reg.fio} \n Мед-центр: {reg.medical_center.name} \n' \
           f'Номер телефона: {reg.phone} \n' \
           f'Город: {reg.city.name} \n' \
           f'Специалист: {reg.special.name} \n' \
           f'Время записи: {reg.register_at} \n' \
           f'Имя специалиста: {reg.special.employees.get(medical_center_id=reg.medical_center.id).fio}'

    return text


@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text=HELP_COMMAND,
                           parse_mode="HTML",
                           reply_markup=ReplyKeyboardRemove())


@dp.message_handler(commands=['start'])
async def help_command(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text="Привет, выбери что ты хочешь сделать!",
                           reply_markup=greet_start
                           )


@dp.message_handler(commands=['desc'])
async def help_command(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text=DESC,
                           )


## ВЫБОРКА ГОРОДА
@dp.message_handler(lambda message: message.text.startswith("Зарег"))
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    register_request = None
    city_ikb = InlineKeyboardMarkup()
    cities = City.objects.all()
    for data in cities:
        city_ikb.add(InlineKeyboardButton(f'{data.name}', callback_data=cb.new(item='med', id=data.id,
                                                                               message_id=callback_query.message_id)))
    await bot.send_message(callback_query.from_user.id, reply_markup=city_ikb,
                           text="Заполните данные для создания заявки")


@dp.message_handler(lambda message: message.text.startswith("Посмо"))
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    reg_list_ikb = InlineKeyboardMarkup()

    reg_list = RegisterRequest.objects.all()
    for data in reg_list:
        reg_list_ikb.add(InlineKeyboardButton(f'{data.city.name} {data.medical_center.name} - {data.special.name}',
                                              callback_data=cb.new(item='list', id=data.id,
                                                                   message_id=callback_query.message_id)))
    await bot.send_message(callback_query.from_user.id, reply_markup=reg_list_ikb,
                           text="Выберите чтобы посмотреть детали")


@dp.callback_query_handler(cb.filter(item="list"))
async def register_callback(callback_query: types.CallbackQuery, callback_data: dict):
    reg = RegisterRequest.objects.get(id=callback_data['id'])
    reg_action_ikb = InlineKeyboardMarkup().add(
        InlineKeyboardButton("Удалить", id=reg.id, callback_data=cb.new(item='del', id=reg.id,
                                                                        message_id=callback_query.message.message_id))
    )
    await bot.send_message(callback_query.from_user.id, reply_markup=reg_action_ikb, text=get_text(reg))
    print(callback_query.message.message_id)

@dp.callback_query_handler(cb.filter(item="del"))
async def register_callback(callback_query: types.CallbackQuery, callback_data: dict):
    mes = callback_data['message_id']
    reg = RegisterRequest.objects.filter(id=callback_data['id']).delete()
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=mes)
    await bot.send_message(callback_query.from_user.id, reply_markup=None, text="Запись успешно удалена")


@dp.callback_query_handler(cb.filter(item="med"))
async def register_callback(callback_query: types.CallbackQuery, callback_data: dict):
    med_ikb = InlineKeyboardMarkup()
    city_id = callback_data.get('id')
    register_request['city_id'] = city_id
    med_centers = MedicalCenter.objects.filter(city__in=[city_id])
    for data in med_centers:
        med_ikb.add(InlineKeyboardButton(f'{data.name}', callback_data=cb.new(item='spec', id=data.id,
                                                                              message_id=callback_query.message.message_id)))
    await bot.edit_message_reply_markup(chat_id=callback_query.from_user.id,
                                        message_id=callback_query.message.message_id,
                                        reply_markup=med_ikb,
                                        )


## ВЫБОРКА МЕД ЦЕНТРА
@dp.callback_query_handler(cb.filter(item="med"))
async def register_callback(callback_query: types.CallbackQuery, callback_data: dict):
    med_ikb = InlineKeyboardMarkup()
    city_id = callback_data.get('id')
    register_request['city_id'] = city_id
    med_centers = MedicalCenter.objects.filter(city__in=[city_id])
    for data in med_centers:
        med_ikb.add(InlineKeyboardButton(f'{data.name}', callback_data=cb.new(item='spec', id=data.id,
                                                                              message_id=callback_query.message.message_id)))
    await bot.edit_message_reply_markup(chat_id=callback_query.from_user.id,
                                        message_id=callback_query.message.message_id,
                                        reply_markup=med_ikb,
                                        )


## ВЫБОРКА СПЕЦИАЛИСТА
@dp.callback_query_handler(cb.filter(item="spec"))
async def register_callback(callback_query: types.CallbackQuery, callback_data: dict):
    spec_ikb = InlineKeyboardMarkup()
    med_id = callback_data.get('id')
    register_request['medical_center_id'] = med_id
    spec = Special.objects.filter(employees__medical_center_id=med_id)

    for data in spec:
        spec_ikb.add(InlineKeyboardButton(f'{data.name}', callback_data=cb.new(item='emp', id=data.id,
                                                                               message_id=callback_query.message.message_id)))
    await bot.edit_message_reply_markup(chat_id=callback_query.from_user.id,
                                        message_id=callback_query.message.message_id,
                                        reply_markup=spec_ikb,
                                        )


## ВЫБОРКА СПЕЦИАЛИСТА
@dp.callback_query_handler(cb.filter(item="emp"))
async def register_callback(callback_query: types.CallbackQuery, callback_data: dict):
    emp_ikb = InlineKeyboardMarkup()
    spec_id = callback_data.get('id')
    register_request['special_id'] = spec_id
    emp = Employee.objects.filter(specail__in=spec_id)
    for data in emp:
        emp_ikb.add(
            InlineKeyboardButton(f'{data.fio} - {data.price} тг', callback_data=cb.new(item='date', id=data.id,
                                                                                       message_id=callback_query.message.message_id)))
    await bot.edit_message_reply_markup(chat_id=callback_query.from_user.id,
                                        message_id=callback_query.message.message_id,
                                        reply_markup=emp_ikb,
                                        )


## ВЫБОРКА СПЕЦИАЛИСТА
@dp.callback_query_handler(cb.filter(item="date"))
async def register_callback(callback_query: types.CallbackQuery, callback_data: dict):
    # Отправляем сообщение с просьбой ввести дату и привязываем к нему клавиатуру
    await bot.send_message(callback_query.from_user.id, "Введите дату в формате ДД.ММ.ГГГГ", reply_markup=date_keyboard)


@dp.message_handler(content_types=types.ContentType.CONTACT)
async def process_contact(message: types.Message):
    contact = message.contact
    register_request['phone'] = contact.phone_number
    register_request['fio'] = f'{contact.first_name} {contact.last_name}'
    reg = RegisterRequest.objects.create(**register_request)
    sent_message = await bot.send_message(chat_id=message.chat.id, text=get_text(reg),
                                          reply_markup=None)
    # Сохраняем message_id отправленного сообщения в объекте Message для дальнейшего использования
    message.sent_message_id = sent_message.message_id
    # Удаляем кнопку "Поделиться номером" из разметки
    await message.answer('Продолжить', reply_markup=greet_start)


async def handle_message(message: types.Message):
    # Проверяем, что пользователь отправил сообщение с текстом
    if message.text:
        # Проверяем, что отправленный текст соответствует формату даты
        try:
            dates = datetime.strptime(message.text, '%d.%m.%Y')
            # Если формат даты верный, можно продолжить обработку
            # Например, отправить пользователю подтверждение
            await message.answer(f"Вы ввели дату: {dates.strftime('%d.%m.%Y')}")
            register_request['register_at'] = dates.date()
            await bot.send_message(chat_id=message.from_user.id,
                                   text="Введите номер",
                                   reply_markup=share_key)
        except ValueError:
            # Если формат даты неверный, отправляем сообщение с просьбой ввести дату еще раз
            await message.answer("Неверный формат даты. Пожалуйста, введите дату в формате ДД.ММ.ГГГГ",
                                 reply_markup=date_keyboard)


# Регистрируем функцию-обработчик
dp.register_message_handler(handle_message)


## ВЫБОРКА СПЕЦИАЛИСТА
@dp.callback_query_handler(cb.filter(item="phone"))
async def register_callback(callback_query: types.CallbackQuery, callback_data: dict):
    await bot.edit_message_reply_markup(chat_id=callback_query.from_user.id,
                                        message_id=callback_query.message.message_id,
                                        reply_markup=None,
                                        )
    await bot.send_message(chat_id=callback_query.from_user.id,
                           text="Введите номер",
                           reply_markup=share_key)


executor.start_polling(dp)
