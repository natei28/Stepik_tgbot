from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.filters.callback_data import CallbackData
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

BOT_TOKEN = '7437970301:AAE1tgR7533Q-qpwB7xy0cD5AfU3U8S5flM'

# Создаем объекты бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

FRUITS: dict[str, str] = {
  'check_aple': 'Яблоко',
  'check_kiwi': 'Киви',
  'check_banana': 'Банан',
  'check_orange': 'Апельсин',
  'check_chery': 'Вишня',
  'check_mango': 'Манго',
}
user_check_fruit = []
#user_check_fruit: list[str] = []

def create_kb(DICT_BTN: dict, width: int):
  kb_builder = InlineKeyboardBuilder()
  buttons: list[InlineKeyboardButton] = []
  for button in list(DICT_BTN.keys()):
    buttons.append(InlineKeyboardButton(
      text=DICT_BTN[button],
      callback_data=button))
  kb_builder.row(*buttons, width=width)
  return kb_builder.as_markup()

def create_kb_mod(callback: CallbackQuery,
                  user_check_items: dict, 
                  DICT_BTN: dict, 
                  width: int, 
                  button_type: int = 1): #button_type: 1-button, 2-checkbox
  if button_type == 1:
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []
    for button in list(DICT_BTN.keys()):
      buttons.append(InlineKeyboardButton(
        text=DICT_BTN[button],
        callback_data=button))
    kb_builder.row(*buttons, width=width)
    return kb_builder.as_markup()
    
  elif button_type == 2:
    if DICT_BTN[callback.data][2:] in (user_check_items):
      print(f"1.1 {DICT_BTN}")
      DICT_BTN[callback.data] = DICT_BTN[callback.data][2:]
      print(f"1.2 {DICT_BTN}")
      user_check_items.remove(DICT_BTN[callback.data])
      print(f'Пользователь выбрал:{user_check_items}')
    else:
      print(f"2.1 {DICT_BTN}")
      DICT_BTN[callback.data] = f"+ {DICT_BTN[callback.data]}"
      user_check_items.append(DICT_BTN[callback.data][2:])
      print(f'Пользователь выбрал:{user_check_items}')
    
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []
    for button in list(DICT_BTN.keys()):
      buttons.append(InlineKeyboardButton(
        text=DICT_BTN[button],
        callback_data=button))
    kb_builder.row(*buttons, width=width)
    return kb_builder.as_markup()
    
    
    
    
    
    
    

@dp.message(CommandStart())
async def process_command_start(message: Message):
  await message.answer(text='Добрый день!\n'
                            'Это тестовый бот\n\n'
                            'Напишите слово "Фрукты"')

@dp.message(F.text.lower() == 'фрукты')
async def process_command_fruits(message: Message):
  check_fruits_markup = create_kb_mod(None, None, FRUITS, 2)
  await message.answer(text="Выбирете фрукты:",
                       reply_markup=check_fruits_markup)

@dp.callback_query(F.data.in_(list(FRUITS.keys())))
async def process_check_fruits(callback: CallbackQuery):
  
#  if FRUITS[callback.data][2:] in (user_check_fruit):
#    FRUITS[callback.data] = FRUITS[callback.data][2:]
#    user_check_fruit.remove(FRUITS[callback.data])
#    print(f'Пользователь выбрал:{user_check_fruit}')
#  else:
#    FRUITS[callback.data] = f"+ {FRUITS[callback.data]}"
#    user_check_fruit.append(FRUITS[callback.data][2:])
#    print(f'Пользователь выбрал:{user_check_fruit}')
  check_fruits_markup = create_kb_mod(callback, user_check_fruit, FRUITS, 2, 2)
  print(user_check_fruit)
  await callback.message.edit_text(text='Выберете один или несколько:',
                                   reply_markup=check_fruits_markup)
  
  
  
  
  
  
  

# Запускаем поллинг
if __name__ == '__main__':
  dp.run_polling(bot)