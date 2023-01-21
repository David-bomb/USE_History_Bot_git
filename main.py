from aiogram import Bot, types
from aiogram.utils import executor
import sqlite3
import datetime
import json
from aiogram.dispatcher import Dispatcher
# from aiogram.utils.callback_data import CallbackData

from helper import unpacker
import logging
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from tgbotpag import InlineKeyboardPaginator
from aiogram.utils.callback_data import CallbackData

# Создание бота
TOKEN = '5165988091:AAGZ1qrF6r7f8cB_crlOzX0dpHltfViCyA8'
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
# Создание соединений с файлами, вероятно перемещение их в отдельный файл
conn = sqlite3.connect('users.db')
cur = conn.cursor()
connection = sqlite3.connect('dates.db')
cursor = connection.cursor()
# Инициализация логирования
logging.basicConfig(
    filename='errors.log',
    format='%(asctime)s %(levelname)s %(name)s %(message)s',
    level=logging.ERROR
)
# turn_page_cb = CallbackData('turn_page', 'movement',
#                           'page')  # Создание машины колбеков, которая используется в выводе сообщений в browse
# Открытие нужных файлов
with open('dates.txt', 'r', encoding='utf-8') as file:
    txtDates = file.readlines()
with open("dates.json", "r") as read_file:
    JsDates = json.load(read_file)

urlkb = InlineKeyboardMarkup(row_width=2)
urlButton = InlineKeyboardButton(text='Назад', callback_data='list_back')
urlButton2 = InlineKeyboardButton(text='Вперед', callback_data='list_forward')
urlkb.add(urlButton, urlButton2)


@dp.message_handler(commands=['start'])  # Функция приветствия и регистрации
async def start(msg: types.Message):
    await msg.reply(
        "Привет, меня зовут HistoryBot, но для вас просто Хисти. Готов вас проконсультировать по некоторым историческим вопросам!\nНапишите /help , чтобы увидеть мои возможности!")
    if not cur.execute(  # Регистрация юзера, если он еще не зарегистрирован
            f'''SELECT * FROM users WHERE id = {msg.from_user.id}''').fetchall():
        sql = '''INSERT INTO users(id, username, name, regs) VALUES(?, ?, ?, ?)'''
        data_tuple = (
            msg.from_user.id, msg.from_user.username, msg.from_user.first_name,
            datetime.datetime.now().strftime("%Y-%m-%d"))
        cur.execute(sql, data_tuple)
        conn.commit()


@dp.message_handler(commands=['help'])  # Команда помощь ¯\_(ツ)_/¯
async def help(msg: types.Message):
    message = 'Нужна помощь? Я всегда любил помогать!\nЯ могу:\n-Отправить вам все даты, которые я знаю по команде /view_dates \n-Найти нужные вам события по датам по команде /browse_dates [запрос], например: /browse_dates 1945  , также можно и так:  /browse_dates 9 мая 1945 , либо  /browse_dates январь 1945. Лишних знаков препинания не треуется.\n-Найти нужные вам разделы по событиям по команде /browse_event . Например: "/browse_event Курск" выдаст вам Курскую битву июля - августа 1943 \nЯ буду самосовершенствоваться. Я обещаю!!!\nP.s. Я знаю только даты по истории России, но я обязательно выучу новые, чтобы потом рассказывать их вам!'
    await msg.reply(message)


@dp.message_handler(commands=['view_dates'])  # Комманда для просмотра данных
async def view(msg: types.Message, page=1, sent=None):
    sent: types.Message = sent
    '''for x in range(0, len('\n'.join(txtDates)), 4096):
        await bot.send_message(msg.chat.id, '\n'.join(txtDates)[x:x + 4096], parse_mode='markdown')'''
    lens = 0
    ans = []
    dates_filtered = []
    for i in txtDates:
        if lens + len(i) <= 1024:
            ans.append(i)
            lens += len(i)
            # print(lens)
        else:
            # print(lens)
            dates_filtered.append('\n'.join(ans))
            # print('----------------')
            lens = len(i)
            ans = [i]
    dates_filtered.append('\n'.join(ans))
    '''dates_filtered = ['\n'.join(txtDates)[x:x + 1024] for x in  # Нарезка данных по 1024 символа
                      range(0, len('\n'.join(txtDates)), 1024)]'''
    paginator = InlineKeyboardPaginator(  # Создание пагинатора
        len(dates_filtered),
        current_page=page,
        data_pattern='date_list#{page}')
    if sent is None:
        await bot.send_message(msg.chat.id, dates_filtered[page - 1], reply_markup=paginator.markup,
                               parse_mode='markdown')
    else:
        await sent.edit_text(dates_filtered[page - 1], reply_markup=paginator.markup,
                             parse_mode='markdown')


@dp.callback_query_handler(lambda call: call.data.split('#')[0] == 'date_list')
async def characters_page_callback(call):
    page = int(call.data.split('#')[1])
    '''await bot.delete_message(
        call.message.chat.id,
        call.message.message_id
    )'''
    # print(call)
    await view(msg=call.message, page=page, sent=call.message)


'''@dp.message_handler(commands=['info'])
async def info(msg: types.Message):
    message = ''
    await msg.reply(message)'''


@dp.message_handler(commands=['browse_dates'])  # Первый прототип поиска по датам
async def search_date(msg: types.Message):
    '''with open("dates.json", "r") as read_file:
        JsDates = json.load(read_file)'''
    argument = msg.get_args()  # Получение даты
    # print(f'Я получил дату! {argument}')
    # print(JsDates.keys())
    try:
        if len(argument) >= 3:
            if len(argument) == 3:
                argument = '0' + argument
            # print('Код 4. Запрос')
            date = cursor.execute(f''' SELECT date, event FROM dates WHERE date like '%{argument}%' ''').fetchall()
            # print(date)
            # print(date)
            # print(f'Код 4. Получил: {date}')
            if date:
                # print('Код 4. Отправляю...')
                if len(date) > 4096:
                    '''dates_filtered = ['\n'.join(unpacker(date))[x:x + 4096] for x in
                                      range(0, len('\n'.join(unpacker(date))), 4096)]
                    print(dates_filtered)
                    paginator = InlineKeyboardPaginator(
                        len(dates_filtered),
                        current_page=page,
                        data_pattern='character#{page}')
                    # await sender(dates_filtered, msg, page)
                    await bot.send_message(msg.chat.id, dates_filtered[page - 1], reply_markup=paginator.markup,
                                           parse_mode='markdown')'''
                    for x in range(0, len('\n'.join(unpacker(date))), 4096):
                        await bot.send_message(msg.chat.id, '\n'.join(unpacker(date))[x:x + 4096],
                                               parse_mode='markdown')
                else:
                    await bot.send_message(msg.chat.id, '\n'.join(unpacker(date)))
                '''for x in range(0, len('\n'.join(unpacker(date))), 4096):
                    await bot.send_message(msg.chat.id, '\n'.join(unpacker(date))[x:x + 4096], parse_mode='markdown')'''
                # print(dates_filtered)
                # print('Код 4. Отправил')
            else:
                await msg.reply('Ничего не найдено!')
        else:
            await msg.reply('Извините, я не могу обработать запрос короче 3-х символов.')
    except Exception as e:
        logging.error(str(e))
        await msg.reply('Ошибка запроса! Попробуйте вписать запрос по шаблону!')


@dp.message_handler(commands=['browse_event'])
async def search_event(msg: types.Message):
    argument = msg.get_args().lower()  # Получение события
    try:
        if len(argument) >= 4:
            data = cursor.execute(f''' SELECT date, event FROM dates WHERE event_lower like '%{argument}%' ''').fetchall()
            if data:
                if len(data) > 4096:
                    for x in range(0, len('\n'.join(unpacker(data))), 4096):
                        await bot.send_message(msg.chat.id, '\n'.join(unpacker(data))[x:x + 4096],
                                               parse_mode='markdown')
                else:
                    await bot.send_message(msg.chat.id, '\n'.join(unpacker(data)))
            else:
                await msg.reply('Ничего не найдено!')
        else:
            await msg.reply('Не могу обработать запрос короче 4 символов')
    except Exception as e:
        logging.error(str(e))
        await msg.reply('Ошибка запроса!')


# Обработка стронних сообщений -------------------------------------------------------------------------------------
@dp.message_handler(content_types=[types.ContentType.TEXT])  # Обработка обычных текстовых сообщений
async def get_text_messages(msg: types.Message):
    await msg.reply(
        f'Прошу прощения, {msg.from_user.first_name} , я не могу понять, что вы мне написали.\nИспользуйте команды пожалуйста.')


@dp.message_handler(content_types=[types.ContentType.AUDIO])  # Обработка звуковых файлов
async def get_text_messages(msg: types.Message):
    await msg.reply(
        f'Я бы послушал всё, что вы я сейчас от вас получил. Но я не умею.\nИспользуйте команды пожалуйста.')


@dp.message_handler(content_types=[types.ContentType.DOCUMENT])  # Обработка документов
async def get_text_messages(msg: types.Message):
    await msg.reply(
        f'Ничего себе! Целый документ! Умел бы я их читать, я бы с умным видом этим бы и зянялся.\nИспользуйте команды пожалуйста.')


@dp.message_handler(content_types=[types.ContentType.GAME])  # Обработка полученных игр???
async def get_text_messages(msg: types.Message):
    await msg.reply(
        f'Я сам заядлый игрок конечно, но сейчас я при исполнении! Так что вынужден отказаться.\nИспользуйте команды пожалуйста.')


@dp.message_handler(content_types=[types.ContentType.PHOTO])  # Обработка фото
async def get_text_messages(msg: types.Message):
    await msg.reply(
        f'Я бы сказал, что мне нравится фото, если бы они для меня не были набором символов.\nИспользуйте команды пожалуйста.')


@dp.message_handler(content_types=[types.ContentType.STICKER])  # Обработка стикера
async def get_text_messages(msg: types.Message):
    await msg.reply(
        f'Классный стикер! А я вот не знаю, как их добавлять, так ответить не могу...\nИспользуйте команды пожалуйста.')


@dp.message_handler(content_types=[types.ContentType.VIDEO])  # Обработка фото
async def get_text_messages(msg: types.Message):
    await msg.reply(
        f'Видео в большинстве своём много весят, не буду я скачивать твоё видео, а то на полезную информацию места не останется.\nИспользуйте команды пожалуйста.')


@dp.message_handler(content_types=[types.ContentType.VOICE])  # Обработка фото
async def get_text_messages(msg: types.Message):
    await msg.reply(
        f'Потом послушаю, я бот занятой.\nИспользуйте команды пожалуйста.')


@dp.message_handler(content_types=[types.ContentType.CONTACT])  # Обработка фото
async def get_text_messages(msg: types.Message):
    await msg.reply(
        f'Я не расположен к новым знакомствам сегодня...\nИспользуйте команды пожалуйста.')


@dp.message_handler(content_types=[types.ContentType.LOCATION])  # Обработка фото
async def get_text_messages(msg: types.Message):
    await msg.reply(
        f'Я и так в вашем устройстве, зачем мне к вам идти?\nИспользуйте команды пожалуйста.')


@dp.message_handler(content_types=[types.ContentType.UNKNOWN])  # Обработка фото
async def get_text_messages(msg: types.Message):
    await msg.reply(
        f'Используйте команды пожалуйста, а то я не понял, что я вообще получил...')


@dp.message_handler(content_types=[types.ContentType.ANY])  # Обработка фото
async def get_text_messages(msg: types.Message):
    await msg.reply(
        f'Я не понимаю, что я сейчас получил от вас. Извиняюсь.\nИспользуйте команды пожалуйста.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
