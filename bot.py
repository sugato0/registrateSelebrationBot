
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Command
from aiogram import *
from random import randrange,shuffle
import DBQueries

bot_token = '5362306060:AAEXhy-7D5k6553J0DduwDyqAK-i0sNjep4'
CHATID = "-1001852260806"


bot = Bot(token=bot_token)
storage = MemoryStorage()

dp = Dispatcher(bot, storage=storage)

dbqr = DBQueries.DB()

class Order:
    def __init__(self,idclient,idevent,idplace,num_ber_people,date,idorganizer):
        
        self.idclient = idclient
        self.idevent = idevent
        
        self.number_people = num_ber_people
        self.idplace = idplace
        self.date = date

        self.idorganizer = idorganizer


        
class Client:
    def __init__(self,client_id,client_fio, client_phone, client_email):
        self.client_id = client_id
        self.client_fio =  client_fio
        self.client_phone = client_phone
        self.client_email = client_email

# class OrderForm(StatesGroup):
#     idevent = State()
#     idplace = State()
#     num_ber_people = State()
#     date = State()
#     idorganizer = State()


class OrderForm(StatesGroup):

    
    idevent = State()
    number_people = State()
    idPlace = State()
    date = State()
    
class Serv_order(StatesGroup):
    serv_id = State()
    
    



class ClientForm(StatesGroup):
    
    client_fio= State()
    client_phone = State()
    client_email = State()

class COMMIT(StatesGroup):
    choose = State()





somenome = "1"




@dp.message_handler(Command('start'))
async def start_handler(message: types.Message):
    keyBoard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyBoard.add(*["Зарегистрироваться"])
    await message.answer('Я бот для организации праздников. Выберите что вас интересует',
                         reply_markup=keyBoard)
    
    

@dp.message_handler(text = ["Зарегистрироваться"])
async def start_handler(message: types.Message):
    
    await message.answer('Введите ваши фамилию имя и отчество')
    await ClientForm.client_fio.set()

@dp.message_handler(state=ClientForm.client_fio)
async def process_customer(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['client_fio'] = message.text
    await message.answer('Введи ваш номер телефона')
    await ClientForm.client_phone.set()

@dp.message_handler(state=ClientForm.client_phone)
async def process_customer(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['client_phone'] = message.text
    await message.answer('Введите адрес электронной почты')
    await ClientForm.client_email.set()

@dp.message_handler(state=ClientForm.client_email)
async def process_customer(message: types.Message, state: FSMContext):
    keyboard = types.InlineKeyboardMarkup()
    async with state.proxy() as data:
        data['client_email'] = message.text
    for i in dbqr.getEvents():
        keyboard.add(types.InlineKeyboardButton(text = i[1],callback_data=str(i[0])+str("_event")))
    if not(dbqr.IsUserExist(message.from_user.id)):
        client = Client(
                str(message.from_user.id),
                data['client_fio'],
                data['client_phone'],
                data['client_email']
            )
    

        dbqr.setUser(client.client_id,
                    client.client_fio,
                    client.client_phone,
                    client.client_email)

    


    await state.finish()
    await OrderForm.idevent.set()
    await message.answer("Выберите тип мероприятия",reply_markup=keyboard)

@dp.callback_query_handler(text_contains = "event",state=OrderForm.idevent)
async def process_customer(call: types.CallbackQuery, state: FSMContext):
    event_id = call.data.split("_")[0]
    
    async with state.proxy() as data:
        
        
        data['idevent'] = event_id
    
    # for i in dbqr.getProv_Serv():
    #     keyboard.add(types.InlineKeyboardButton(text = i[2],callback_data=i[0]))
    # keyboard.add(types.InlineKeyboardButton(text = "Продолжить",callback_data="0"))
    
    await OrderForm.number_people.set()
    await call.message.answer("Введите количество людей на мероприятии")
    

@dp.message_handler(state=OrderForm.number_people)
async def process_customer(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['number_people'] = message.text
    
    keyboard = types.InlineKeyboardMarkup()
    
    
    for i in dbqr.getPlace(message.text):

        keyboard.add(types.InlineKeyboardButton(text = i[1],callback_data=i[0]))
    await message.answer("Выберите место для мероприятия", reply_markup=keyboard)
    await OrderForm.idPlace.set()

@dp.callback_query_handler(state=OrderForm.idPlace)
async def process_customer(call: types.CallbackQuery, state: FSMContext):
    
    
    async with state.proxy() as data:
        
        
        data['idPlace'] = call.data
    
    await call.message.answer("Введите дату формат: дд-мм-гггг")

    await OrderForm.date.set()
    

@dp.message_handler(state=OrderForm.date)
async def process_customer(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['date'] = message.text
    keyboard = types.InlineKeyboardMarkup()
    for i in dbqr.getProv_Serv():
        keyboard.add(types.InlineKeyboardButton(text = i[2],callback_data=i[0]))
    keyboard.add(types.InlineKeyboardButton(text = "Закончить регистрацию",callback_data="0"))
    try:
        date = data["date"].split("-")
        date = f"{date[2]}-{date[1]}-{date[0]}"


        order = Order(
            str(message.from_user.id),

            data["idevent"],
            data["idPlace"],
            data["number_people"],
            
            date,
            str(randrange(1,5))
        )
        # print(order.idclient,
        #             order.idevent,
        #             order.idplace,
        #             order.number_people,
        #             order.date,
        #             order.idorganizer)

        dbqr.setOrder(order.idclient,
                    order.idevent,
                    order.idplace,
                    order.number_people,
                    order.date,
                    order.idorganizer)


        await state.finish()
        await Serv_order.serv_id.set()
        await message.answer("Выберите дополнительную услугу, \
                            после выбора одной или нескольких \
                            дополнительных услуг нажите завершить регистрацию",reply_markup=keyboard)

    except Exception as e:
        print(e)
        await message.answer("Не верный формат введеных данных попробуйте вновь")
        

    
@dp.callback_query_handler(state=Serv_order.serv_id)
async def process_customer(call: types.CallbackQuery, state: FSMContext):
    
    
    async with state.proxy() as data:
        
        
        data['serv_id'] = call.data
    

    
    
    if call.data == "0":
        keyboard = types.InlineKeyboardMarkup()

        data = dbqr.getALL(call.from_user.id)
        texter = f"ФИО : {data[0][0]}\nНомер телефона : {data[0][1]}\nemail : {data[0][2]}\nномер заказа : {data[0][3]}\nсобытие : {data[0][4]}\nМесто : {data[0][5]}\nАдрес : {data[0][6]}\nКоличество человек : {data[0][7]}\nДата : {data[0][8]}\nДоп услуги : {'|'.join([i[-1] for i in data])}\n"
 
        keyboard.add(types.InlineKeyboardButton(text = "Подтвердить",callback_data="1"))

        await COMMIT.choose.set()
        await call.message.answer(texter,reply_markup=keyboard)
        
    else:
        dbqr.setServ_Order(call.data,call.from_user.id)


@dp.callback_query_handler(state=COMMIT.choose)
async def process_customer(call: types.CallbackQuery, state: FSMContext):
    data = dbqr.getALL(call.from_user.id)
    texter = f"ФИО : {data[0][0]}\nНомер телефона : {data[0][1]}\nemail : {data[0][2]}\nномер заказа : {data[0][3]}\nсобытие : {data[0][4]}\nМесто : {data[0][5]}\nАдрес : {data[0][6]}\nКоличество человек : {data[0][7]}\nДата : {data[0][8]}\nДоп услуги : {'|'.join([i[-1] for i in data])}\n"
 
    
    await bot.send_message(CHATID,texter)
    await state.finish()
    await call.message.answer("Спасибо за заказ")
    

    










executor.start_polling(dp, skip_updates=True)