from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup, Message, PhotoSize)

yes_button = InlineKeyboardButton(
    text='Да',
    callback_data='yes'
)
no_button = InlineKeyboardButton(
    text='Нет',
    callback_data='no')
# Добавляем кнопки в клавиатуру в один ряд
keyboard: list[list[InlineKeyboardButton]] = [
    [yes_button, no_button]
]
# Создаем объект инлайн-клавиатуры
markup = InlineKeyboardMarkup(inline_keyboard=keyboard)

appr_button = InlineKeyboardButton(
    text='Далее',
    callback_data='yes'
)
disappr_button = InlineKeyboardButton(
    text='Выйти из подбора',
    callback_data='no')
# Добавляем кнопки в клавиатуру в один ряд
keyboard: list[list[InlineKeyboardButton]] = [
    [appr_button], [disappr_button]
]
# Создаем объект инлайн-клавиатуры
final_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)


PE1_button = InlineKeyboardButton(
    text='ПЭ1',
    callback_data='ПЭ1'
)
PE2_button = InlineKeyboardButton(
    text='ПЭ2',
    callback_data='ПЭ2')
PRE1_button = InlineKeyboardButton(
    text='ПРЕ1',
    callback_data='ПРЕ1')
# Добавляем кнопки в клавиатуру в один ряд
plata_keyboard: list[list[InlineKeyboardButton]] = [
    [PE1_button, PE2_button],
    [PRE1_button]
]
# Создаем объект инлайн-клавиатуры
plata_markup = InlineKeyboardMarkup(inline_keyboard=plata_keyboard)
# 1х220В или 3х220В
engine1_button = InlineKeyboardButton(
    text='1х220В',
    callback_data='1х220В'
)
engine2_button = InlineKeyboardButton(
    text='3х220В',
    callback_data='3х220В')
# Добавляем кнопки в клавиатуру в один ряд
engine_keyboard: list[list[InlineKeyboardButton]] = [
    [engine1_button, engine2_button]
]
# Создаем объект инлайн-клавиатуры
engine_markup = InlineKeyboardMarkup(inline_keyboard=engine_keyboard)


vfc1_button = InlineKeyboardButton(
    text='ПЧВ1',
    callback_data='vfc1'
)
vfc3_button = InlineKeyboardButton(
    text='ПЧВ3',
    callback_data='vfc3')
# Добавляем кнопки в клавиатуру в один ряд
vfc_keyboard: list[list[InlineKeyboardButton]] = [
    [vfc1_button, vfc3_button]
]
# Создаем объект инлайн-клавиатуры
vfc_markup = InlineKeyboardMarkup(inline_keyboard=vfc_keyboard)

rb1_button = InlineKeyboardButton(
    text='РБ1',
    callback_data='RB1'
)
rb3_button = InlineKeyboardButton(
    text='РБ3',
    callback_data='RB3')
# Добавляем кнопки в клавиатуру в один ряд
rb_keyboard: list[list[InlineKeyboardButton]] = [
    [rb1_button, rb3_button]
]
# Создаем объект инлайн-клавиатуры
rb_markup = InlineKeyboardMarkup(inline_keyboard=rb_keyboard)


# 1х220В или 3х220В
volt1_button = InlineKeyboardButton(
    text='220В',
    callback_data='yes'
)
volt2_button = InlineKeyboardButton(
    text='380В',
    callback_data='no'
)
volt3_button = InlineKeyboardButton(
    text='Другое',
    callback_data='pass'
)
# Добавляем кнопки в клавиатуру в один ряд
volt_keyboard: list[list[InlineKeyboardButton]] = [
    [volt1_button, volt2_button],
    [volt3_button]
]
# Создаем объект инлайн-клавиатуры
volt_markup = InlineKeyboardMarkup(inline_keyboard=volt_keyboard)

lpo1_button = InlineKeyboardButton(
    text='ЛПО1',
    callback_data='ЛПО1'
)
lpo2_button = InlineKeyboardButton(
    text='ЛПО2',
    callback_data='ЛПО2'
)
lpo3_button = InlineKeyboardButton(
    text='ЛПО3',
    callback_data='ЛПО3'
)
no_button = InlineKeyboardButton(
    text='Панель не нужна',
    callback_data='no'
)
# Добавляем кнопки в клавиатуру в один ряд
lpo_keyboard: list[list[InlineKeyboardButton]] = [
    [lpo1_button, lpo2_button, lpo3_button],
    [no_button]
]
# Создаем объект инлайн-клавиатуры
lpo_markup = InlineKeyboardMarkup(inline_keyboard=lpo_keyboard)


Profibus = InlineKeyboardButton(
    text='Profibus',
    callback_data='ПИП1'
)
Profinet = InlineKeyboardButton(
    text='Profinet',
    callback_data='ПИП2'
)
CANopen = InlineKeyboardButton(
    text='CANopen',
    callback_data='ПИК1'
)
EtherCat = InlineKeyboardButton(
    text='EtherCat',
    callback_data='ПИЭ1'
)
Modbus = InlineKeyboardButton(
    text='Modbus TCP/IP',
    callback_data='ПИЭ2'
)
# Добавляем кнопки в клавиатуру в один ряд
encoders_keyboard: list[list[InlineKeyboardButton]] = [
    [Profibus],
    [Profinet],
    [CANopen],
    [EtherCat],
    [Modbus]
]
# Создаем объект инлайн-клавиатуры
encoders_markup = InlineKeyboardMarkup(inline_keyboard=encoders_keyboard)


koef1 = InlineKeyboardButton(
    text='1',
    callback_data='1.0'
)
koef2 = InlineKeyboardButton(
    text='2',
    callback_data='1.1'
)
koef3 = InlineKeyboardButton(
    text='3',
    callback_data='1.2'
)
koef4 = InlineKeyboardButton(
    text='4',
    callback_data='1.35'
)
koef5 = InlineKeyboardButton(
    text='5',
    callback_data='1.7'
)
# Добавляем кнопки в клавиатуру в один ряд
moment_keyboard: list[list[InlineKeyboardButton]] = [
    [koef1,koef2,koef3,koef4,koef5] 
]
# Создаем объект инлайн-клавиатуры
moment_markup = InlineKeyboardMarkup(inline_keyboard=moment_keyboard)