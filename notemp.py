from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import executor
from aiogram.utils.callback_data import CallbackData

bot = Bot(token='5165988091:AAGZ1qrF6r7f8cB_crlOzX0dpHltfViCyA8')
dp = Dispatcher(bot)
listed = ['Чмоня', 'Шлёпа', 'Тайлер Дердан', 'Патрик Бейтман', 'Райан Гослинг']
num = 0
cd_walk = CallbackData("dun_w", "leaf")
urlkb = InlineKeyboardMarkup(row_width=2)
urlButton = InlineKeyboardButton(text='Назад', callback_data=cd_walk.new(leaf=-1))
urlButton2 = InlineKeyboardButton(text='Вперед', callback_data=cd_walk.new(leaf=+1))
urlkb.add(urlButton, urlButton2)



@dp.message_handler(commands='send')
async def url_command(message: types.Message):
    await message.answer(listed[num%len(listed)], reply_markup=urlkb)


@dp.callback_query_handler(text='list_forward')
async def list_forward_call(callback: types.CallbackQuery, callback_data: dict):
    leaf = callback_data.get('leaf')
    print(leaf)
    await callback.message.edit_text(listed[num%len(listed)], reply_markup=urlkb)
    await callback.answer()


@dp.callback_query_handler(cd_walk.filter())
async def list_forward_call(callback: types.CallbackQuery, callback_data: dict):
    leaf = callback_data.get('leaf')
    print(leaf)
    await callback.message.edit_text(listed[num%len(listed)], reply_markup=urlkb)
    await callback.answer()


if __name__ == '__main__':
    executor.start_polling(dp)
