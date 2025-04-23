from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup, Message, PhotoSize)
from aiogram.types import BotCommand
import logging
from data_base.dao import add_vfc
from keyboards.inline_keyboards import *
import pandas as pd

# from keyboards.reply_note_kb import main_note_kb
from keyboards.reply_other_kb import main_kb

vfc_selection = Router()

# Создаем "базу данных" пользователей
user_dict: dict[int, dict[str, str | int | bool]] = {}

# Cоздаем класс, наследуемый от StatesGroup, для группы состояний нашей FSM
class FSMEquipmentSelection(StatesGroup):
    state_1 = State()  # Состояние для выбора напряжения сети
    state_4 = State()
    state_5 = State()
    state_21 = State()  # Состояние для выбора типа оборудования
    state_7 = State()  # Состояние для выбора типа оборудования
    state_10 = State()  # Состояние для ввода коэффициента запаса
    state_11 = State()  # Состояние для ввода коэффициента запаса
    state_14 = State()  # Состояние для расчета выходного тока
    state_16 = State()  # Состояние для расчета выходного тока
    state_13 = State()  # Состояние для расчета выходного тока
    state_18 = State()  # Состояние для расчета выходного тока
    state_19 = State()  # Состояние для расчета выходного тока
    state_23 = State()  # Состояние для расчета выходного тока
    state_25 = State()  # Состояние для расчета выходного тока
    state_28 = State()  # Состояние для расчета выходного тока
    state_29 = State()  # Состояние для расчета выходного тока
    state_30 = State()  # Состояние для расчета выходного тока
    state_31 = State()  # Состояние для расчета выходного тока
    state_prot_select = State()  # Состояние для расчета выходного тока
    state_vfc_selection = State()  # Состояние для расчета выходного тока
    model_selection = State()  # Состояние для выбора дополнительных опций
    state_select_res = State()
    check_state = State()
    state_approve = State()


# async def setup_bot_commands():
#     bot_commands = [
#         BotCommand(command="/vfcselection", description="Начать подбор ПЧВ"),
#         BotCommand(command="/showdata", description="Показать данные подбора"),
#         BotCommand(command="/cancel", description="Отменить подбор")
#     ]
#     await bot.set_my_commands(bot_commands)

# Этот хэндлер будет срабатывать на команду /start вне состояний
# и предлагать перейти к заполнению анкеты, отправив команду /vfcselection
@vfc_selection.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message):
    await message.answer(
        text='Добро пожаловать!\n\n'
             'Чтобы перейти к подбору модели ПЧВ - '
             'отправьте команду /vfcselection'
    )


# Этот хэндлер будет срабатывать на команду "/cancel" в состоянии
# по умолчанию и сообщать, что эта команда работает внутри машины состояний
@vfc_selection.message(Command(commands='cancel'), StateFilter(default_state))
async def process_cancel_command(message: Message):
    await message.answer(
        text='Подбор не производится\n\n'
             'Чтобы перейти к подбору - '
             'отправьте команду /vfcselection'
    )


# Этот хэндлер будет срабатывать на команду "/cancel" в любых состояниях,
# кроме состояния по умолчанию, и отключать машину состояний
@vfc_selection.message(Command(commands='cancel'), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(
        text='Вы вышли из подбора\n\n'
             'Чтобы снова перейти к подбору - '
             'отправьте команду /vfcselection'
    )
    # Сбрасываем состояние и очищаем данные, полученные внутри состояний
    await state.clear()
    # await callback.message.answer(text='Теперь введите номинальный ток двигателя (указан на шильдике двигателя)')
    # await state.set_state(FSMEquipmentSelection.state_23)


# Этот хэндлер будет срабатывать на команду /vfcselection
# и переводить бота в состояние ожидания ввода напряжения
@vfc_selection.message(Command(commands='vfcselection'), StateFilter(default_state))
@vfc_selection.message(F.text == 'Подбор ПЧВ')
async def state_1s(message: Message, state: FSMContext):
    # await message.answer(text='Напряжение питающей сети: 220В?')
    # await print(state.get_state())
    # await setup_bot_commands()
    await message.answer(
        text='Напряжение питающей сети 220В или 380В?',
        reply_markup=volt_markup
    )
    
    await state.set_state(FSMEquipmentSelection.state_1)


# Этот хэндлер будет срабатывать, если во время выбора напряжения
# будет введено/отправлено что-то некорректное
@vfc_selection.message(StateFilter(FSMEquipmentSelection.state_1))
async def warning_not_gender(message: Message):
    print('state_1')

    await message.answer(
        text='Пожалуйста, пользуйтесь кнопками '
             'при выборе напряжения сети\n\nЕсли вы хотите прервать '
             'подбор - отправьте команду /cancel'
    )

@vfc_selection.callback_query(StateFilter(FSMEquipmentSelection.state_1),
                   F.data.in_(['yes', 'no', 'pass']))
async def start(callback: CallbackQuery, state: FSMContext):
    # Cохраняем пол (callback.data нажатой кнопки) в хранилище,
    # по ключу "gender"
    print('state_1')

    await state.update_data(vfc1=None)
    await state.update_data(vfc3=None)
    await state.update_data(engine_power = None)
    await state.update_data(encoder_to_resolver_replacement = None)
    await state.update_data(prom_protocol = None)
    await state.update_data(extra_IO_or_temperature_sensor = None)
    await state.update_data(plata = None)
    await state.update_data(industrial_protocols_support = None)
    await state.update_data(nominal_out_vfc_power = None)
    await state.update_data(res_type = None)
    await state.update_data(encoder_support=None)
    await state.update_data(resolver_connection=None)
    await state.update_data(vfc_power=None)
    await state.update_data(vfc_model_selected=None)
    await state.update_data(distance_to_engine=None)
    await state.update_data(is_shielded=None)
    await state.update_data(rmt_model=None)
    await state.update_data(lpo='')
    await state.update_data(rb1400=0)
    await state.update_data(rb1080=0)
    await state.update_data(rb3=None)
    await state.update_data(voltage=callback.data)
    print(callback.data)
    await state.update_data(vfc1=True)
    await state.update_data(vfc3=False)
    await state.update_data(pvv1=False)

    if callback.data == 'yes':
        # await callback.message.answer("Какой номинальный ток двигателя?", reply_markup=keyboard)
        # Отправляем в чат сообщение о выходе из машины состояний
        await callback.message.answer(
            text='''Невозможно использование доп. плат расширения для:
подключения устройства с протоколом Profibus, Profinet, CANopen, EtherCat, Modbus TCP/IP; 
подключения резольвера; для подключения энкодера;
входов и выходов.'''
        )
        await callback.message.answer(
            text='Питание двигателя 1х220В или 3х220В?',
            reply_markup = engine_markup
        )
        
        await state.set_state(FSMEquipmentSelection.state_4)
        
        
        # await state.set_state(FSMEquipmentSelection.model_selection)
    elif callback.data == 'no':
        await callback.message.answer(
            text='''Потребуется ли поддержка пром. 
протоколов или энкодера/резольвера или 
наличие доп. входов/выходов?''',
            reply_markup=markup
        )
        # await callback.message.answer('Необходима ли вам поддержка энкодеров?', reply_markup=keyboard)
        await state.set_state(FSMEquipmentSelection.state_5)
    else:
        await callback.message.answer(
            text='''К сожалению, в нашем ассортименте нет моделей, поддерживающих такой вольтаж. Чтобы начать подбор заново, отправьте /vfcselection'''
        )
        await state.clear()
    await callback.answer()


@vfc_selection.callback_query(StateFilter(FSMEquipmentSelection.state_4),
                   F.data.in_(['1х220В', '3х220В']))
async def engine_power(callback: CallbackQuery, state: FSMContext):
    print('state_4')
    await state.update_data(engine_power=callback.data)
    print(callback.data)
    user_dict[callback.from_user.id] = await state.get_data()

    await callback.message.answer(text='Теперь введите номинальный ток двигателя. Он указан на шильдике двигателя (необходимо указать только целое число)')
    await state.set_state(FSMEquipmentSelection.state_23)

@vfc_selection.callback_query(StateFilter(FSMEquipmentSelection.state_5),
                   F.data.in_(['yes', 'no']))
async def encoder_support(callback: CallbackQuery, state: FSMContext):
    print('state_5')
    
    await state.update_data(encoder_support=callback.data)
    print(callback.data)
    await state.update_data(vfc3=True)
    await state.update_data(vfc1=False)

    if callback.data == 'yes':
        await callback.message.answer(
            text='''Требуется ли поддержка промышленных 
протоколов Profibus, Profinet, CANopen, 
EtherCat, Modbus TCP/IP?''',
            reply_markup=markup
        )
        await state.set_state(FSMEquipmentSelection.state_7)
    elif callback.data == 'no':
        await callback.message.answer(
            text='''Требуется ли контроль обрыва 
ремня привода без датчика?''',
            reply_markup=markup
        )
        await state.set_state(FSMEquipmentSelection.state_21)

    await callback.answer()

@vfc_selection.message(StateFilter(FSMEquipmentSelection.state_5))
async def warning_not_gender(message: Message):
    print('state_5')

    await message.answer(
        text='Пожалуйста, пользуйтесь кнопками '
             '\n\nЕсли вы хотите прервать '
             'подбор - отправьте команду /cancel'
    )

@vfc_selection.message(StateFilter(FSMEquipmentSelection.state_5))
async def warning_not_gender(message: Message):
    print('state_5')

    await message.answer(
        text='Пожалуйста, пользуйтесь кнопками '
             '\n\nЕсли вы хотите прервать '
             'подбор - отправьте команду /cancel'
    )

@vfc_selection.callback_query(StateFilter(FSMEquipmentSelection.state_7),
                   F.data.in_(['yes', 'no']))
async def enc2res_replacement(callback: CallbackQuery, state: FSMContext):

    print('state_7')

    await state.update_data(encoder_to_resolver_replacement=callback.data)
    print(callback.data)

    if callback.data == 'yes':
        # Информирование о необходимости 
        # использов-я доп. платы расширения 
        # для подключения резольвера.
        await callback.message.answer(
            '''Внимание! Возможна поддержка
только одного протокола.'''
        )

        await callback.message.answer(
            '''Необходимо 
использовать доп. платы расширения 
для подключения устройства с выбранным протоколом.
Выберите необходимый протокол: ''',
            reply_markup=encoders_markup
        )
        await state.set_state(FSMEquipmentSelection.state_prot_select)
    elif callback.data == 'no':
        await callback.message.answer(
            text='Требуется ли подключение энкодера/резольвера?',
            reply_markup=markup
        )
        await state.set_state(FSMEquipmentSelection.state_16)

    await callback.answer()

@vfc_selection.message(StateFilter(FSMEquipmentSelection.state_7))
async def warning_not_gender(message: Message):
    print('state_7')
    await message.answer(
        text='Пожалуйста, пользуйтесь кнопками '
             '\n\nЕсли вы хотите прервать '
             'подбор - отправьте команду /cancel'
    )

# @vfc_selection.message(F.text == '1' or F.text == '2' or F.text == '3' or F.text == '4' or F.text == '5')
@vfc_selection.callback_query(StateFilter(FSMEquipmentSelection.state_prot_select),
                   F.data.in_(['ПИП1', 'ПИП2', 'ПИЭ1', 'ПИЭ2', 'ПИК1']))
async def encoder_resolver_connection(callback: CallbackQuery, state: FSMContext):
    print('state_prot_select')

    await state.update_data(prom_protocol=callback.data)
    print(callback.data)
    await callback.message.answer(
            text=f'Для подключения необходимо использовать плату {callback.data}. Она добавлена в список подобранного оборудования'
        )
    await callback.message.answer(
            text='Требуется ли подключение энкодера/резольвера?',
            reply_markup=markup
        )
    await state.set_state(FSMEquipmentSelection.state_10)

@vfc_selection.message(StateFilter(FSMEquipmentSelection.state_prot_select))
async def warning_not_gender(message: Message):
    print('state_prot_select')

    await message.answer(
        text='Пожалуйста, пользуйтесь кнопками '
             '\n\nЕсли вы хотите прервать '
             'подбор - отправьте команду /cancel'
    )

@vfc_selection.callback_query(StateFilter(FSMEquipmentSelection.state_16),
                   F.data.in_(['yes', 'no']))
async def resolver_connection(callback: CallbackQuery, state: FSMContext):
    print('state_16')

    await state.update_data(resolver_connection=callback.data)
    print(callback.data)
    # resolver_connection = 'yes'

    if callback.data == 'yes':
        await callback.message.answer(
            text='''Необходимо использовать доп. платы расширения 
для подключения энкодера или резольвера. Для энкодеров есть 2 варианта плат: 
ПЭ1 и ПЭ2.  Различия в том, что напряжение питания ПЭ1 равно 5 В, ПЭ2 - 12 В, 
ПЭ1 работает с TTL-энкодерами, ПЭ2 работает с HTL-энкодерами. Для резольвера
плата ПРЕ1. Невозможно одновременное использование доп платы для входов и выходов. Какая плата вам нужна?''',
            reply_markup=plata_markup
        )
        await state.set_state(FSMEquipmentSelection.state_18)
    elif callback.data == 'no':
        await callback.message.answer(
            text='''Требуется ли наличие доп. входов/выходов или
подключение датчика температуры двигателя? ''',
            reply_markup=markup
        )
        await state.set_state(FSMEquipmentSelection.state_19)

@vfc_selection.message(StateFilter(FSMEquipmentSelection.state_16))
async def warning_not_gender(message: Message):
    print('state_16')

    await message.answer(
        text='Пожалуйста, пользуйтесь кнопками '
             '\n\nЕсли вы хотите прервать '
             'подбор - отправьте команду /cancel'
    )

@vfc_selection.callback_query(StateFilter(FSMEquipmentSelection.state_19),
                   F.data.in_(['yes', 'no']))
async def plates_selection(callback: CallbackQuery, state: FSMContext):

    print('state_19')

    await state.update_data(resolver_connection=callback.data)
    print(callback.data)
    # resolver_connection = 'yes'

    if callback.data == 'yes':
        await callback.message.answer(
            text='''Необходимо 
использование доп. платы расширения 
для входов и выходов, плата добавлена в набор. (ПВВ1)''',
            # reply_markup=markup
        )
        await state.update_data(pvv1=True)

        # await callback.message.answer(
        #     text='Чтобы посмотреть данные '
        #         'подбора - отправьте команду /showdata'
        # )
        # await callback.answer()

        user_dict[callback.from_user.id] = await state.get_data()
        # Завершаем машину состояний
        # await state.clear()
        await callback.message.answer(text='Теперь введите номинальный ток двигателя (указан на шильдике двигателя)')
        await state.set_state(FSMEquipmentSelection.state_23)
    elif callback.data == 'no':
        await callback.message.answer(
            text='''Требуется ли контроль обрыва 
ремня привода без датчика?''',
            reply_markup=markup
        )
        
        await state.set_state(FSMEquipmentSelection.state_21)

@vfc_selection.message(StateFilter(FSMEquipmentSelection.state_19))
async def warning_not_gender(message: Message):
    print('state_19')

    await message.answer(
        text='Пожалуйста, пользуйтесь кнопками '
             '\n\nЕсли вы хотите прервать '
             'подбор - отправьте команду /cancel'
    )

@vfc_selection.callback_query(StateFilter(FSMEquipmentSelection.state_21),
                   F.data.in_(['yes', 'no']))
async def vfc_decision(callback: CallbackQuery, state: FSMContext):
    print('state_21')
    await state.update_data(resolver_connection=callback.data)
    print(callback.data)
    # resolver_connection = 'yes'

    user_dict[callback.from_user.id] = await state.get_data()

    if callback.data == 'yes':
        await state.update_data(vfc3=True)
        await state.update_data(vfc1=False)
        await callback.message.answer(text='Теперь введите номинальный ток двигателя (указан на шильдике двигателя)')
        await state.set_state(FSMEquipmentSelection.state_23)
    else:
        await state.update_data(vfc3=True)
        await state.update_data(vfc1=True)
        await callback.message.answer(text='Теперь введите номинальный ток двигателя (указан на шильдике двигателя)')
        await state.set_state(FSMEquipmentSelection.state_23)

@vfc_selection.callback_query(StateFilter(FSMEquipmentSelection.state_vfc_selection),
                   F.data.in_(['vfc1', 'vfc3']))
async def state_vfc_selection(callback: CallbackQuery, state: FSMContext):
    print('state_vfc_selection')

    user_dict[callback.from_user.id] = await state.get_data()

    if callback.data == 'vfc1':
        await state.update_data(vfc3=False)
        await state.update_data(vfc1=True)
        vfc_model = user_dict[callback.from_user.id]['vfc1_model']

    else:
        await state.update_data(vfc3=True)
        await state.update_data(vfc1=False)
        vfc_model = user_dict[callback.from_user.id]['vfc3_model']

        
    # await callback.message.answer(text='Теперь введите номинальный ток двигателя (указан на шильдике двигателя)')
    if not vfc_model['Мощность используемого электродвигателя, кВт'].values[0] >= 90:
        await state.update_data(vfc_model_selected=vfc_model)
        await callback.message.answer(
                text='''На каком расстоянии находится ПЧВ от двигателя? (укажите только целое число метров)'''
            )
        await state.set_state(FSMEquipmentSelection.state_28)
    else:
        await callback.message.answer(
                text='''Так как выбран ПЧВ с мощностью более 90 кВт, нет возможности использовать моторный
и сетевой дроссели '''
            )
        print(vfc_model)
        
        if vfc_model['Мощность используемого электродвигателя, кВт'].values[0] < 30:
            await callback.message.answer(
                    text=f'Есть необходимость в тормозном резисторе? (продолжительность включения составляет 10%)',
                    reply_markup = markup
                )
            
            await state.set_state(FSMEquipmentSelection.state_30)
        else:
            await callback.message.answer(
                text='''Можно также приобрести выносные панели (ЛПО). Они предназначены для 
программирования и оперативного управления ПЧВ. Виды: 
однострочная и двухстрочная (с одинаковым функционалом) - ЛПО1 и ЛПО2, а также графическая 
(с пояснениями на русском языке) - ЛПО3. Подключаются к ПЧВ через прямой патч-корд 
длиной до 30 метров. Патч-корд в комплекте не идет, мы, к сожалению, его не продаем.''',
                reply_markup=lpo_markup
            )
            await state.set_state(FSMEquipmentSelection.state_31)
            
        # await state.clear()


@vfc_selection.callback_query(StateFilter(FSMEquipmentSelection.state_10),
                   F.data.in_(['yes', 'no']))
async def extra_IO_or_temperature_sensor(callback: CallbackQuery, state: FSMContext):
    print('state_10')
    await state.update_data(extra_IO_or_temperature_sensor=callback.data)
    print(callback.data)
    # 
    #  and resolver_connection == 'yes'!!!!!!!!!!!!!!!!!!!!!!!!!!!
    if callback.data == 'yes':
        await callback.message.answer(
            text='''Невозможно  
использование доп. платы расширения 
для входов и выходов (ПВВ1), так как для нее не 
остается слота.'''
        )
        
        await callback.message.answer(
            text='''Необходимо использовать доп. платы расширения 
для подключения энкодера или резольвера. Для энкодеров есть 2 варианта плат: 
ПЭ1 и ПЭ2.  Различия в том, что напряжение питания ПЭ1 равно 5 В, ПЭ2 - 12 В, 
ПЭ1 работает с TTL-энкодерами, ПЭ2 работает с HTL-энкодерами. Для резольвера
плата ПРЕ1. Невозможно одновременное использование доп платы для входов и выходов. Какая плата вам нужна?''',
            reply_markup=plata_markup
        )
        await state.set_state(FSMEquipmentSelection.state_11)
    elif callback.data == 'no':
        await callback.message.answer(
            text='''Требуется ли наличие доп. входов/выходов или
подключение датчика температуры двигателя? ''',
            reply_markup=markup
        )
        await state.set_state(FSMEquipmentSelection.state_14)

    await callback.answer()

@vfc_selection.message(StateFilter(FSMEquipmentSelection.state_10))
async def warning_not_gender(message: Message):
    print('state_10')

    await message.answer(
        text='Пожалуйста, пользуйтесь кнопками '
             '\n\nЕсли вы хотите прервать '
             'подбор - отправьте команду /cancel'
    )

@vfc_selection.callback_query(StateFilter(FSMEquipmentSelection.state_11),
                   F.data.in_(['ПЭ1', 'ПЭ2', 'ПРЕ1']))
async def plata(callback: CallbackQuery, state: FSMContext):
    print('state_11')
    
    await state.update_data(plata=callback.data)
    print(callback.data)

    # await callback.message.answer(
    #     text='Чтобы посмотреть данные '
    #         'подбора - отправьте команду /showdata'
    # )
    # await callback.answer()
    user_dict[callback.from_user.id] = await state.get_data()
    # Завершаем машину состояний
    # await state.clear()
    await callback.message.answer(text='Теперь введите номинальный ток двигателя (указан на шильдике двигателя)')
    await state.set_state(FSMEquipmentSelection.state_23)


@vfc_selection.callback_query(StateFilter(FSMEquipmentSelection.state_13),
                   F.data.in_(['yes', 'no']))
async def extra_plates(callback: CallbackQuery, state: FSMContext):
    print('state_13')

    await state.update_data(plata=callback.data)
    print(callback.data)
    
    await callback.message.answer(
        text='''Внимание! Необходимо 
использование доп. платы расширения 
для входов и выходов, плата добавлена в набор. (ПВВ1)'''
    )
    await state.update_data(pvv1=True)

    user_dict[callback.from_user.id] = await state.get_data()

    await callback.message.answer(text='Теперь введите номинальный ток двигателя (указан на шильдике двигателя)')
    await state.set_state(FSMEquipmentSelection.state_23)

    await callback.answer()

@vfc_selection.callback_query(StateFilter(FSMEquipmentSelection.state_18),
                   F.data.in_(['ПЭ1', 'ПЭ2', 'ПРЕ1']))
async def extra_IO(callback: CallbackQuery, state: FSMContext):
    print('state_18')

    await state.update_data(plata=callback.data)
    print(callback.data)
    await callback.message.answer(
            text='''Требуется ли наличие доп. входов/выходов или
подключение датчика температуры двигателя?  ''',
            reply_markup=markup
        )
        # Отправляем в чат сообщение о выходе из машины состояний
    
    await state.set_state(FSMEquipmentSelection.state_19)
    
    await callback.answer()

@vfc_selection.message(StateFilter(FSMEquipmentSelection.state_18))
async def warning_not_gender(message: Message):
    print('state_18')

    await message.answer(
        text='Пожалуйста, пользуйтесь кнопками '
             '\n\nЕсли вы хотите прервать '
             'подбор - отправьте команду /cancel'
    )

@vfc_selection.callback_query(StateFilter(FSMEquipmentSelection.state_14),
                   F.data.in_(['yes', 'no']))
async def industrial_protocols_support(callback: CallbackQuery, state: FSMContext):
    print('state_14')

    await state.update_data(industrial_protocols_support=callback.data)
    print(callback.data)

    if callback.data == 'yes':
        # Отправляем в чат сообщение о выходе из машины состояний
        await callback.message.answer(
            text='''Внимание! Необходимо 
использов-я доп. платы расширения 
для входов и выходов, плата добавлена в набор. (ПВВ1)'''
        )
        await state.update_data(pvv1=True)

        user_dict[callback.from_user.id] = await state.get_data()
        # Завершаем машину состояний
        # await state.clear()
        await callback.message.answer(text='Теперь введите номинальный ток двигателя (указан на шильдике двигателя)')
        await state.set_state(FSMEquipmentSelection.state_23)
        # await state.set_state(FSMEquipmentSelection.model_selection)
        
        
        # await state.set_state(FSMEquipmentSelection.model_selection)
    elif callback.data == 'no':
    
        user_dict[callback.from_user.id] = await state.get_data()
        # Завершаем машину состояний
        # await state.clear()
        await callback.message.answer(text='Теперь введите номинальный ток двигателя (указан на шильдике двигателя)')
        await state.set_state(FSMEquipmentSelection.state_23)
        
        
        # await state.set_state(FSMEquipmentSelection.model_selection)

    await callback.answer()


@vfc_selection.message(StateFilter(FSMEquipmentSelection.state_23),
            lambda x: (x.text.isdigit() or '.' in x.text) and 0 <= float(x.text) <= 1000)
async def process_age_sent(message: Message, state: FSMContext):
    print('state_23')

    await state.update_data(vfc_power=message.text)

    user_dict[message.from_user.id] = await state.get_data()

    await message.answer(
        text='''Выберите ваш тип механизма и нажмите на соответствующую кнопку:\n
1) Механизм с легким и нормальным плавным пуском, низким динамическим моментом сопротивления нагрузки

2) Механизм с нагруженным плавным пуском, умеренным динамическим моментом сопротивления нагрузки           

3) Механизм с нагруженным пуском, с повышенным динамическим моментом сопротивления нагрузки

4) Механизм с тяжелым пуском, с большим динамическим моментом сопротивления нагрузки

5) Механизм со сверхтяжелым пуском, с большим динамическим моментом сопротивления нагрузки''',
        reply_markup= moment_markup
    )
    await state.set_state(FSMEquipmentSelection.state_25)

@vfc_selection.message(StateFilter(FSMEquipmentSelection.state_23))
async def warning_not_gender(message: Message):
    print('state_23')

    await message.answer(
        text='Введено некорректное число '
             '\n\nЕсли вы хотите прервать '
             'подбор - отправьте команду /cancel'
    )

@vfc_selection.callback_query(StateFilter(FSMEquipmentSelection.state_25),
                   F.data.in_(['1.0', '1.1', '1.2', '1.35', '1.7', 'ПЧВ1', 'ПЧВ3']))   
# @vfc_selection.callback_query(StateFilter(FSMEquipmentSelection.state_25),
#                    F.data.in_(['ПЧВ1', 'ПЧВ3']))   
async def process_age_sentt(callback: CallbackQuery, state: FSMContext):
    print('state_25')

    # await state.update_data(nominal_out_vfc_power=message.text)
    # data = await state.get_data()
    print(state)
    # if message.from_user.id in user_dict:
    total_nominal_power = float(user_dict[callback.from_user.id]['vfc_power']) * float(callback.data)

    vfc_engine_df = pd.read_excel('exel_files\модели ПЧВ по выходному току двигателя.xlsx')
    # if user_dict[callback.from_user.id]['voltage'] == 'yes':
    #     vfc_engine_df = vfc_engine_df[vfc_engine_df['Источник питания'] == '1 фазы ~220 В']
    #     print('1 phase: ', vfc_engine_df)
    # elif user_dict[callback.from_user.id]['voltage'] == 'no':
    #     vfc_engine_df = vfc_engine_df[vfc_engine_df['Источник питания'] == '3 фазы ~380 В']
    #     print('3 phase: ', vfc_engine_df)


    vfc1_engine_df = vfc_engine_df[vfc_engine_df["Модификация"].str.startswith('ПЧВ1')]
    vfc1_model = vfc1_engine_df[vfc1_engine_df['Номинальный выходной ток, А'] >= total_nominal_power].head(1)
    vfc3_engine_df = vfc_engine_df[vfc_engine_df["Модификация"].str.startswith('ПЧВ3')]

    print(user_dict[callback.from_user.id]) 
    print('decision: ', user_dict[callback.from_user.id]['vfc1'], user_dict[callback.from_user.id]['vfc3'])
    if user_dict[callback.from_user.id]['vfc1'] and user_dict[callback.from_user.id]['vfc3']:
        # vfc1_engine_df = vfc_engine_df[vfc_engine_df["Модификация"].str.startswith('ПЧВ1')]
        # vfc1_model = vfc1_engine_df[vfc1_engine_df['Номинальный выходной ток, А'] >= total_nominal_power].head(1)
        # vfc3_engine_df = vfc_engine_df[vfc_engine_df["Модификация"].str.startswith('ПЧВ3')]
        # print(vfc_engine_df)
        vfc3_model = vfc3_engine_df[vfc3_engine_df['Номинальный выходной ток, А'] >= total_nominal_power].head(1)
        
        print(vfc1_model)
        print(vfc3_model)

        await state.update_data(vfc1_model=vfc1_model)
        await state.update_data(vfc3_model=vfc3_model)

        print('vfc1: ', vfc1_model.empty, ' vfc3: ', vfc3_model.empty)
        if not vfc1_model.empty and not vfc3_model.empty:
            await callback.message.answer(text=f'Подобранные модели ПЧВ: {vfc1_model["Модификация"].values[0]}, {vfc3_model["Модификация"].values[0]}')
            await callback.message.answer(
                text='''\nМощность ПЧВ1 от 0.75 до 22 кВт, ПЧВ3 - от 0.75 до 450 кВт, 
ПЧВ1 имеет модификации 0.75-2.2кВт с питанием от сети 1х220В,
перегрузочная способность ПЧВ1: 150% в теч. 60с, ПЧВ3 – 120% в теч. 35с.
ПЧВ1 используются в общепромышленном режиме, а ПЧВ3 - для 
вентиляторно-насосной нагрузки. \nПожалуйста, выберите более подходящую для вас модель ''',
                reply_markup=vfc_markup
            ) 
            await state.set_state(FSMEquipmentSelection.state_vfc_selection)
        elif vfc3_model.empty:
            vfc_model = vfc1_model
            await state.update_data(vfc_model_selected=vfc_model)
            if not vfc_model.empty:
                await callback.message.answer(text=f'Подобранная модель ПЧВ: {vfc_model["Модификация"].values[0]}')
            else:
                await callback.message.answer(text=f'Не удалось подобрать модель с указанными параметрами. Возможно были неправильно указаны параметры или у нас не нашлось оборудования, удовлетворяющего указанным характеристикам. Начать подбор заново - /vfcselection')
                await state.clear()
        elif vfc1_model.empty:
            vfc_model = vfc3_model
            await state.update_data(vfc_model_selected=vfc_model)
            if not vfc_model.empty:
                await callback.message.answer(text=f'Подобранная модель ПЧВ: {vfc_model["Модификация"].values[0]}')
            else:
                await callback.message.answer(text=f'Не удалось подобрать модель с указанными параметрами. Возможно были неправильно указаны параметры или у нас не нашлось оборудования, удовлетворяющего указанным характеристикам. Начать подбор заново - /vfcselection')
                await state.clear()
        else:
            await callback.message.answer(text=f'К сожалению, не нашлось ни одной модели по указанным параметрам')
            await state.clear()

    elif user_dict[callback.from_user.id]['vfc1']:
        vfc_engine_df = vfc_engine_df[vfc_engine_df["Модификация"].str.startswith('ПЧВ1')]
        vfc_model = vfc_engine_df[vfc_engine_df['Номинальный выходной ток, А'] >= total_nominal_power].head(1)
        await state.update_data(vfc_model_selected=vfc_model)
        if not vfc_model.empty:
            await callback.message.answer(text=f'Подобранная модель ПЧВ: {vfc_model["Модификация"].values[0]}')
        else:
            await callback.message.answer(text=f'Не удалось подобрать модель с указанными параметрами. Возможно были неправильно указаны параметры или у нас не нашлось оборудования, удовлетворяющего указанным характеристикам. Начать подбор заново - /vfcselection')
            await state.clear()

    else:
        vfc_engine_df = vfc_engine_df[vfc_engine_df["Модификация"].str.startswith('ПЧВ3')]
        vfc_model = vfc_engine_df[vfc_engine_df['Номинальный выходной ток, А'] >= total_nominal_power].head(1)
        await state.update_data(vfc_model_selected=vfc_model)
        
        if not vfc_model.empty:
            await callback.message.answer(text=f'Подобранная модель ПЧВ: {vfc_model["Модификация"].values[0]}')
        else:
            await callback.message.answer(text=f'Не удалось подобрать модель с указанными параметрами. Возможно были неправильно указаны параметры или у нас не нашлось оборудования, удовлетворяющего указанным характеристикам. Начать подбор заново - /vfcselection')
            await state.clear()

    # print(vfc_engine_df)
    print(user_dict[callback.from_user.id])
    user_dict[callback.from_user.id] = await state.get_data()
    # vfc_model = user_dict[message.from_user.id]['vfc_model_selected']
    # try:
    vfc_rmt_df = pd.read_excel('exel_files\модели ПЧВ и моторные дроссели.xlsx')
    distance_df = pd.read_excel('exel_files\Длины кабелей.xlsx')

    # print()

    

    print('vfc_rmt_df: ', vfc_rmt_df)

    rmt_model = vfc_rmt_df[vfc_rmt_df['Модификация'] == vfc_model['Модификация'].values[0]]
    print(rmt_model)
    distance = user_dict[callback.from_user.id]['distance_to_engine']
    is_shielded = user_dict[callback.from_user.id]['is_shielded']

    vfc_max_distance = distance_df[distance_df['Мощность ПЧВ'] <= vfc_model['Мощность используемого электродвигателя, кВт'].values[0]].tail(1)
        
    if user_dict[callback.from_user.id]['engine_power'] == '3х220В':
        vfc_rmt_df = vfc_rmt_df[vfc_rmt_df['Реакторы моторные'].str.startswith('РМТ')]
    elif user_dict[callback.from_user.id]['engine_power'] == '1х220В':
        vfc_rmt_df = vfc_rmt_df[vfc_rmt_df['Реакторы моторные'].str.startswith('РМО')]
        print(rmt_model)
        await state.update_data(rmt_model=rmt_model)

        await callback.message.answer(
                text=f'Необходимо применение моторного дросселя следующей модели: {rmt_model["Реакторы моторные"].values[0]}, он добавлен в список необходимых устройств. Максимальная длина в метрах с применением дросселя: {vfc_max_distance["Экранированный с применением моторного дросселя, м"].values[0]}')
        await callback.message.answer(
                    text=f'Есть необходимость в тормозном резисторе? (продолжительность включения составляет 10%)',
                    reply_markup = markup
                )
        await state.set_state(FSMEquipmentSelection.state_30)

    if not vfc_model['Мощность используемого электродвигателя, кВт'].values[0] >= 90:
        await state.update_data(vfc_model_selected=vfc_model)
        if user_dict[callback.from_user.id]['engine_power'] != '1х220В':
            await callback.message.answer(
                    text='''На каком расстоянии находится ПЧВ от двигателя? (укажите только число метров)'''
                )
            await state.set_state(FSMEquipmentSelection.state_28)
    else:
        await callback.message.answer(
                text='''Так как выбран ПЧВ с мощностью более 90 кВт, нет возможности использовать моторный
и сетевой дроссели '''
            )
        print(vfc_model)
        
        if vfc_model['Мощность используемого электродвигателя, кВт'].values[0] < 30 and user_dict[callback.from_user.id]['engine_power'] != '1х220В':
            await callback.message.answer(
                    text=f'Есть необходимость в тормозном резисторе? (продолжительность включения составляет 10%)',
                    reply_markup = markup
                )
            
        
            await state.set_state(FSMEquipmentSelection.state_30)
        else:
            await callback.message.answer(
                text='''Можно также приобрести выносные панели (ЛПО). Они предназначены для 
        программирования и оперативного управления ПЧВ. Виды: 
        однострочная и двухстрочная (с одинаковым функционалом) - ЛПО1 и ЛПО2, а также графическая 
        (с пояснениями на русском языке) - ЛПО3. Подключаются к ПЧВ через прямой патч-корд 
        длиной до 30 метров. Патч-корд в комплекте не идет, мы, к сожалению, его не продаем.''',
                reply_markup=lpo_markup
            )
            await state.set_state(FSMEquipmentSelection.state_31)
        # await state.clear()
    # except:
    #     print('Уже подобрали.')

@vfc_selection.message(StateFilter(FSMEquipmentSelection.state_25))
async def warning_not_gender(message: Message):
    print('state_25')

    await message.answer(
        text='Пожалуйста, пользуйтесь кнопками '
             '\n\nЕсли вы хотите прервать '
             'подбор - отправьте команду /cancel'
    )

@vfc_selection.message(StateFilter(FSMEquipmentSelection.state_28),
        lambda x: (x.text.isdigit() or '.' in x.text) and 0 <= float(x.text) <= 1200)
async def process_age_sentt(message: Message, state: FSMContext):
    print('state_28')

    # if message.from_user.id in user_dict:
    await state.update_data(distance_to_engine=message.text)

    await message.answer(
            text='''Вы используете экранированный кабель? ''',
            reply_markup = markup
        )
    
    await state.set_state(FSMEquipmentSelection.state_29)

@vfc_selection.message(StateFilter(FSMEquipmentSelection.state_28))
async def warning_not_gender(message: Message):
    print('state_28')

    await message.answer(
        text='Введено некорректное число '
             '\n\nЕсли вы хотите прервать '
             'подбор - отправьте команду /cancel'
    )

@vfc_selection.callback_query(StateFilter(FSMEquipmentSelection.state_29),
                   F.data.in_(['yes', 'no']))
async def is_shielded(callback: CallbackQuery, state: FSMContext):
    print('state_29')

    await state.update_data(is_shielded=callback.data)
    print(callback.data)

    user_dict[callback.from_user.id] = await state.get_data()
    
    vfc_model = user_dict[callback.from_user.id]['vfc_model_selected']
    
    vfc_rmt_df = pd.read_excel('exel_files\модели ПЧВ и моторные дроссели.xlsx')
    distance_df = pd.read_excel('exel_files\Длины кабелей.xlsx')

    # print()

    if user_dict[callback.from_user.id]['engine_power'] == '3х220В':
        vfc_rmt_df = vfc_rmt_df[vfc_rmt_df['Реакторы моторные'].str.startswith('РМТ')]
    elif user_dict[callback.from_user.id]['engine_power'] == '1х220В':
        vfc_rmt_df = vfc_rmt_df[vfc_rmt_df['Реакторы моторные'].str.startswith('РМО')]

    print('vfc_rmt_df: ', vfc_rmt_df)

    rmt_model = vfc_rmt_df[vfc_rmt_df['Модификация'] == vfc_model['Модификация'].values[0]]
    print(rmt_model)
    distance = user_dict[callback.from_user.id]['distance_to_engine']
    is_shielded = user_dict[callback.from_user.id]['is_shielded']

    vfc_max_distance = distance_df[distance_df['Мощность ПЧВ'] <= vfc_model['Мощность используемого электродвигателя, кВт'].values[0]].tail(1)
        
    print(vfc_max_distance)
    if not rmt_model.empty:
        print(distance)
        print(vfc_max_distance)
        print(vfc_max_distance['Экранированный кабель, м'].values[0])
        print(distance, vfc_max_distance['Неэкранированный кабель, м'].values[0])
        print(type(distance), type(vfc_max_distance['Неэкранированный кабель, м'].values[0]))
        if is_shielded == 'да':
            if 'ПЧВ1' in vfc_model['Модификация'].values[0] or float(distance) >= vfc_max_distance['Экранированный кабель, м'].values[0] or user_dict[callback.from_user.id]['engine_power'] == '1х220В':
                await callback.message.answer(
                text=f'Необходимо применение моторного дросселя следующей модели: {rmt_model["Реакторы моторные"].values[0]}, он добавлен в список необходимых устройств. Максимальная длина в метрах с применением дросселя: {vfc_max_distance["Экранированный с применением моторного дросселя, м"].values[0]}')
            else:
                await callback.message.answer(
                text=f'Для улучшения качества работы и долговечности можно также приобрести моторный дроссель следующей модели: {rmt_model["Реакторы моторные"].values[0]}, он добавлен в список необходимых устройств. Максимальная длина в метрах с применением дросселя: {vfc_max_distance["Экранированный с применением моторного дросселя, м"].values[0]}')
        else:
            if 'ПЧВ1' in vfc_model['Модификация'].values[0] or float(distance) >= vfc_max_distance['Неэкранированный кабель, м'].values[0] or user_dict[callback.from_user.id]['engine_power'] == '1х220В':
                await callback.message.answer(
                text=f'Необходимо применение моторного дросселя следующей модели: {rmt_model["Реакторы моторные"].values[0]}, он добавлен в список необходимых устройств. Максимальная длина в метрах с применением дросселя: {vfc_max_distance["Неэкранированный с применением моторного дросселя, м"].values[0]}')
            else:
                await callback.message.answer(
                text=f'Для улучшения качества работы и долговечности можно также приобрести моторный дроссель следующей модели: {rmt_model["Реакторы моторные"].values[0]}, он добавлен в список необходимых устройств. Максимальная длина в метрах с применением дросселя: {vfc_max_distance["Неэкранированный с применением моторного дросселя, м"].values[0]}')
    else:
        await callback.message.answer(
                text=f'Не нашлось подходящей модели моторного дросселя')
    await state.update_data(rmt_model=rmt_model)
    print(rmt_model)
    print(vfc_model)
    if vfc_model['Мощность используемого электродвигателя, кВт'].values[0] < 30:
        await callback.message.answer(
                text=f'Есть необходимость в тормозном резисторе? (продолжительность включения составляет 10%)',
                reply_markup = markup
            )
        await state.set_state(FSMEquipmentSelection.state_30)
    else:
        await callback.message.answer(
                text='''Можно также приобрести выносные панели (ЛПО). Они предназначены для 
        программирования и оперативного управления ПЧВ. Виды: 
        однострочная и двухстрочная (с одинаковым функционалом) - ЛПО1 и ЛПО2, а также графическая 
        (с пояснениями на русском языке) - ЛПО3. Подключаются к ПЧВ через прямой патч-корд 
        длиной до 30 метров. Патч-корд в комплекте не идет, мы, к сожалению, его не продаем.''',
                reply_markup=lpo_markup
            )
        await state.set_state(FSMEquipmentSelection.state_31)

@vfc_selection.message(StateFilter(FSMEquipmentSelection.state_29))
async def warning_not_gender(message: Message):
    print('state_29')

    await message.answer(
        text='Пожалуйста, пользуйтесь кнопками '
             '\n\nЕсли вы хотите прервать '
             'подбор - отправьте команду /cancel'
    )

@vfc_selection.callback_query(StateFilter(FSMEquipmentSelection.state_30),
                   F.data.in_(['yes', 'no']))
async def need_resistor(callback: CallbackQuery, state: FSMContext):
    print('state_30')

    await state.update_data(need_resistor=callback.data)
    print(callback.data)

    user_dict[callback.from_user.id] = await state.get_data()
    
    vfc_model = user_dict[callback.from_user.id]['vfc_model_selected']


    vfc1_res_df = pd.read_excel('exel_files\модели ПЧВ1 и тормозные резисторы.xlsx')
    vfc3_res_df = pd.read_excel('exel_files\модели ПЧВ3 и тормозные резисторы.xlsx')

    # if vfc_model['Мощность используемого электродвигателя, кВт'].values[0] > 30 and callback.data == 'yes':
    #     await callback.message.answer('Для установки тормозного резистора будет необходимо дополнительно установить тормозной модуль. (нет в ассортименте)')
    
    if callback.data == 'yes':
        print()
        if 'ПЧВ1' in vfc_model['Модификация'].values[0]:
            rb1400 = vfc1_res_df[vfc1_res_df['Модификация ПЧВ'] == vfc_model['Модификация'].values[0]]['РБ1-400-К20']
            rb1080 = vfc1_res_df[vfc1_res_df['Модификация ПЧВ'] == vfc_model['Модификация'].values[0]]['РБ1-080-1К0']
            rb3 = vfc1_res_df[vfc1_res_df['Модификация ПЧВ'] == vfc_model['Модификация'].values[0]]['Модель РБ3']

            if (not rb1400.empty or not rb1400.empty or not rb3.empty) and vfc_model['Мощность используемого электродвигателя, кВт'].values[0] < 30:

                rb1400 = rb1400.values
                rb1080 = rb1080.values
                await state.update_data(rb3=rb3)
                rb3 = rb3.values[0]

                await callback.message.answer('Подобранные тормозные резисторы:')    

                print(rb1400)
                if len(rb1400) != 0 and rb1400[0] != 0:
                    await state.update_data(rb1400=rb1400[0])
                    await callback.message.answer('РБ1-400-К20: ' + str(rb1400[0]) + ' шт. (для ПЧВ1 должны подключаться последовательно)')
                print(rb1080)
                if len(rb1080) != 0 and rb1080[0] != 0:
                    await state.update_data(rb1080=rb1080[0])
                    await callback.message.answer('РБ1-080-1К0: ' + str(rb1080[0]) + ' шт. (для ПЧВ1 должны подключаться последовательно)')

                # if (len(rb1400) != 0 and rb1400[0] != 0) or (len(rb1080) != 0 and rb1080[0] != 0):
                #     await callback.message.answer('Резисторы серии РБ1 для ПЧВ1 должны подключаться последовательно')
                if len(rb3) != 0:
                    await callback.message.answer(rb3)
                    
                    await callback.message.answer(
                        text='''Выберите пожалуйста тип тормозных резисторов''',
                        reply_markup=rb_markup
                    )
                    await state.set_state(FSMEquipmentSelection.state_select_res)
            else:
                await callback.message.answer('Для установки тормозного резистора будет необходимо дополнительно установить тормозной модуль. (нет в ассортименте)')
                await callback.message.answer(
                    text='''Можно также приобрести выносные панели (ЛПО). Они предназначены для 
            программирования и оперативного управления ПЧВ. Виды: 
            однострочная и двухстрочная (с одинаковым функционалом) - ЛПО1 и ЛПО2, а также графическая 
            (с пояснениями на русском языке) - ЛПО3. Подключаются к ПЧВ через прямой патч-корд 
            длиной до 30 метров. Патч-корд в комплекте не идет, мы, к сожалению, его не продаем.''',
                    reply_markup=lpo_markup
                )
                await state.set_state(FSMEquipmentSelection.state_31)

            await state.set_state(FSMEquipmentSelection.state_select_res)

        else:   
            # сделать рб1
            rb1400 = vfc3_res_df[vfc3_res_df['Модификация ПЧВ'] == vfc_model['Модификация'].values[0]]['РБ1-400-К20']
            rb1080 = vfc3_res_df[vfc3_res_df['Модификация ПЧВ'] == vfc_model['Модификация'].values[0]]['РБ1-080-1К0']


            if (not rb1400.empty or not rb1400.empty) and vfc_model['Мощность используемого электродвигателя, кВт'].values[0] < 30:

                rb1400 = rb1400.values
                rb1080 = rb1080.values
                # await state.update_data(rb1400='')
                # await state.update_data(rb1080='')
                await callback.message.answer('Подобранные тормозные резисторы:')    
                
                print(rb1400)
                if len(rb1400) != 0 and rb1400[0] != 0:
                    await state.update_data(rb1400=rb1400[0])
                    await callback.message.answer('РБ1-400-К20: ' + str(rb1400[0]) + ' шт.')
                print(rb1080)
                if len(rb1080) != 0 and rb1080[0] != 0:
                    await state.update_data(rb1080=rb1080[0])
                    await callback.message.answer('РБ1-080-1К0: ' + str(rb1080[0]) + ' шт.')
                if (len(rb1080) != 0 and rb1080[0] != 0) or (len(rb1400) != 0 and rb1400[0] != 0):
                    await callback.message.answer('Для ПЧВ1 резисторы серии РБ1 должны подключаться последовательно!')
                    
            else:
                await callback.message.answer('Для установки тормозного резистора будет необходимо дополнительно установить тормозной модуль. (нет в ассортименте)')
                await callback.message.answer(
                    text='''Можно также приобрести выносные панели (ЛПО). Они предназначены для 
программирования и оперативного управления ПЧВ. Виды: 
однострочная и двухстрочная (с одинаковым функционалом) - ЛПО1 и ЛПО2, а также графическая 
(с пояснениями на русском языке) - ЛПО3. Подключаются к ПЧВ через прямой патч-корд 
длиной до 30 метров. Патч-корд в комплекте не идет, мы, к сожалению, его не продаем.''',
                    reply_markup=lpo_markup
                )
            await state.set_state(FSMEquipmentSelection.state_31)
                # await callback.message.answer('К сожалению, для заданных параметров не нашлось подходящих резисторов')    

            # if (len(rb1400) != 0 and rb1400[0] != 0) or (len(rb1080) != 0 and rb1080[0] != 0):
            #     await callback.message.answer('Резисторы серии РБ1 для ПЧВ1 должны подключаться последовательно') # await callback.message.answer('РБ1-080-1К0: ' + str(vfc3_res_df[vfc3_res_df['Модификация ПЧВ'] == vfc_model['Модификация'].values[0]]['РБ1-080-1К0'].values[0]) + ' шт.')        
    
            await callback.message.answer(
                text='''Можно также приобрести выносные панели (ЛПО). Они предназначены для 
        программирования и оперативного управления ПЧВ. Виды: 
        однострочная и двухстрочная (с одинаковым функционалом) - ЛПО1 и ЛПО2, а также графическая 
        (с пояснениями на русском языке) - ЛПО3. Подключаются к ПЧВ через прямой патч-корд 
        длиной до 30 метров. Патч-корд в комплекте не идет, мы, к сожалению, его не продаем.''',
                reply_markup=lpo_markup
            )
            await state.set_state(FSMEquipmentSelection.state_31)

    else:
        await callback.message.answer(
                text='''Можно также приобрести выносные панели (ЛПО). Они предназначены для 
        программирования и оперативного управления ПЧВ. Виды: 
        однострочная и двухстрочная (с одинаковым функционалом) - ЛПО1 и ЛПО2, а также графическая 
        (с пояснениями на русском языке) - ЛПО3. Подключаются к ПЧВ через прямой патч-корд 
        длиной до 30 метров. Патч-корд в комплекте не идет, мы, к сожалению, его не продаем.''',
                reply_markup=lpo_markup
            )
        await state.set_state(FSMEquipmentSelection.state_31)

@vfc_selection.message(StateFilter(FSMEquipmentSelection.state_30))
async def warning_not_gender(message: Message):
    print('state_30')

    await message.answer(
        text='Пожалуйста, пользуйтесь кнопками '
             '\n\nЕсли вы хотите прервать '
             'подбор - отправьте команду /cancel'
    )

@vfc_selection.callback_query(StateFilter(FSMEquipmentSelection.state_select_res),
                   F.data.in_(['RB1', 'RB3']))
async def state_select_res(callback: CallbackQuery, state: FSMContext):
    print('state_select_res')

    await state.update_data(res_type=callback.data)
    print(callback.data)

    user_dict[callback.from_user.id] = await state.get_data()

    await callback.message.answer(
        text='''Можно также приобрести выносные панели (ЛПО). Они предназначены для 
программирования и оперативного управления ПЧВ. Виды: 
однострочная и двухстрочная (с одинаковым функционалом) - ЛПО1 и ЛПО2, а также графическая 
(с пояснениями на русском языке) - ЛПО3. Подключаются к ПЧВ через прямой патч-корд 
длиной до 30 метров. Патч-корд в комплекте не идет, мы, к сожалению, его не продаем.''',
        reply_markup=lpo_markup
    )
    await state.set_state(FSMEquipmentSelection.state_31)


@vfc_selection.callback_query(StateFilter(FSMEquipmentSelection.state_31),
                   F.data.in_(['ЛПО1', 'ЛПО2', 'ЛПО3', 'no']))
async def process_gender_press(callback: CallbackQuery, state: FSMContext):
    print('state_31')
    user_dict[callback.from_user.id] = await state.get_data()

    total_order = {
        'vfc': [user_dict[callback.from_user.id]['vfc_model_selected']["Модификация"].values[0], 1], 
        'lpo': [callback.data, 1 if callback.data != 'no' else 0], 
    }
    if user_dict[callback.from_user.id]['prom_protocol']:
        total_order['prom_plata'] = [user_dict[callback.from_user.id]['prom_protocol'],  1]
    
    if user_dict[callback.from_user.id]['res_type'] == 'RB3':
        total_order['rb3'] = [user_dict[callback.from_user.id]['rb3'].values[0],  1 if user_dict[callback.from_user.id]['rb3'].values[0] else 0]
    else:
        total_order['rb1400'] = ['РБ1-400-К20', user_dict[callback.from_user.id]['rb1400'] * 1] 
        total_order['rb1080'] = ['РБ1-080-1К0', user_dict[callback.from_user.id]['rb1080'] * 1] 

    if user_dict[callback.from_user.id]['plata']:
        total_order['plata'] = [str(user_dict[callback.from_user.id]['plata']), 1] 

    if user_dict[callback.from_user.id]['pvv1']:
        total_order['pvv1'] = ['ПВВ1', 1] 

    # if not user_dict[callback.from_user.id]['rmt_model'] is None:
    try:
        total_order['rmt'] = [user_dict[callback.from_user.id]['rmt_model']["Реакторы моторные"].values[0], 1] 
    except:
        print('рмт не подобран')
    await state.update_data(lpo=callback.data)
    await state.update_data(total_order=total_order)

    user_dict[callback.from_user.id] = await state.get_data()
    print('final_dict: ', user_dict[callback.from_user.id])
    print(total_order)
    order_string = ''
    for key, value in total_order.items():
            if value[1] > 0:
                order_string += str(value[0] + ' - ' + str(value[1]) + ' шт.\n')
    await callback.message.answer(
        text=f'''
        Список подобранного оборудования: 
{order_string}'''.strip(),
        reply_markup=final_markup
    )
    await state.set_state(FSMEquipmentSelection.state_approve)

@vfc_selection.callback_query(StateFilter(FSMEquipmentSelection.state_approve),
                   F.data.in_(['yes', 'no']))
async def confirm_add_note(callback: CallbackQuery, state: FSMContext):
    if callback.data == 'yes':
        vfc_order = user_dict[callback.from_user.id]
        total_order = user_dict[callback.from_user.id]['total_order']
        print('total_order: ', total_order)
        art_df = pd.read_excel(r"C:\Users\Admin\Desktop\ovenbot\exel_files\total_prod.xlsx")
        add_link = ''
        for key, value in total_order.items():
            if value[1] > 0:
                print(value, art_df[art_df['Наименование рабочее'] == value[0]])
                add_link += str(art_df[art_df['Наименование рабочее'] == value[0]]['Артикул'].values[0])
                add_link += str('_' + str(value[1]) + ';')
        print(add_link)
        link = f'https://owen.ru/upl_files/tests/cart_interface/cart.php?prods={add_link}'
        print('link:', link)
        # link = 'https://owen.ru/upl_files/tests/cart_interface/cart.php?prods=54214_2;108193_3;131651_5;'
        try:
            vfc_order['rmt_model'] = vfc_order['rmt_model']["Реакторы моторные"].values[0]
        except:
            print('отсутствует рмт')
        await add_vfc(user_id=callback.from_user.id, vfc_order=vfc_order)
        await callback.message.answer(f'''Заказ успешно зарегестрирован!
<a href="{link}">Ссылка на ваш заказ</a>''', 
        disable_web_page_preview=True, parse_mode="HTML",
        reply_markup=main_kb())
        await state.clear()
    else:
        await callback.message.answer(
        text='Вы вышли из подбора\n\n'
             'Чтобы снова перейти к подбору - '
             'отправьте команду /vfcselection',
        reply_markup=main_kb()
        )
        await state.clear()

#########################################
# Этот хэндлер будет срабатывать на отправку команды /showdata
# и отправлять в чат данные анкеты, либо сообщение об отсутствии данных
# @vfc_selection.message(Command(commands='showdata'), StateFilter(default_state))
# async def process_showdata_command(message: Message):
#     # Отправляем пользователю анкету, если она есть в "базе данных"
#     print(user_dict)
#     if message.from_user.id in user_dict:
#         await message.answer(
#             text=f'{user_dict[message.from_user.id]}'
#         )
#     else:
#         # Если анкеты пользователя в базе нет - предлагаем заполнить
#         await message.answer(
#             text='Вы еще не заполняли анкету. Чтобы приступить - '
#             'отправьте команду /vfcselection'
#         )
############################


# Этот хэндлер будет срабатывать на любые сообщения, кроме тех
# для которых есть отдельные хэндлеры, вне состояний
@vfc_selection.message(StateFilter(default_state))
async def send_echo(message: Message):
    await message.reply(text='Извините, сообщение было введено некорректно')


# Запускаем поллинг
# if __name__ == '__main__':
#     dp.run_polling(bot, skip_updates=True, on_startup=setup_bot_commands)