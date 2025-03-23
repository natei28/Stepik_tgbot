from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
import random



BOT_TOKEN = '7437970301:AAGHr82WI47z6YLk-B_17f6T2RStS9BZThw'
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Задаем колличество попыток
ATTEMPS = 5

# Словарь в котором будут хранится данные пользователя
user = {
  'in_game': False,
  'secret_number': None,
  'attemps': None,
  'total_games': 0,
  'wins': 0
}

# Создаем функцию, возвращающая рандомрандомное число от 1 до 100
def get_random_number() -> int:
  return random.randint(1, 100)

# Этот хэндлер будет обрабатывать команду '/start'
@dp.message(CommandStart())
async def process_start_command(message:Message):
  await message.answer(
    'Привет!\nДавайте сыграем в игру "Угадай число"?\n\n'
    'Чтобы получить правила игры и список доступных '
    'команд - отправьте команду /help'
    )

# Этот хэндлер будет обрабатывать команду '/hhelp
@dp.message(Command(commands = 'help'))
async def process_help_command(message:Message):
  await message.answer(
    'Правила игры:\n\n'
    'Я загадываю число от 1 до 100, а вам нужно его угадать\n'
    f'У вас есть {ATTEMPS} попыток\n\n'
    'Доступные команды: \n'
    '/help - правила игры и список команд\n'
    '/cancel - выйти из игры\n'
    '/stat - посмотреть статистику\n\n'
    'Давай сыграем?')
    
# Этот хэндлер будет обрабатывать комманду '/stat'
@dp.message(Command(commands = 'stat'))
async def process_stat_command(message:Message):
  await message.answer(
    f'Всего сыграно: {user["total_games"]} \n'
    f'Игр выиграно: {user["wins"]}'
    )

# Этот хэндлер будет обрабатывать комманду '/cancel'
@dp.message(Command(commands = 'cancel'))
async def process_cancel_command(message: Message):
  if user['in_game']:
    user['in_game'] = False
    await message.answer(
      'Вы вышли из игры. Если захотите сыграть снова - напишите об этом'
      )
  else:
    await message.answer(
      'А мы и так с Вами не играем! \n'
      'Может сыграем разок?')
      
# Этот хэндлер будет срабатывать на согласие прльзователя сыграть
@dp.message(F.text.lower().in_(['да', 'давай', 'сыграем', 'игра', 'играть', 'хочу играть']))
async def process_positive_answer(message: Message):
  if not user['in_game']:
    user['in_game'] = True
    user['secret_number'] = get_random_number()
    user['attemps'] = ATTEMPS
    await message.answer(
      'Ура!\n\n'
      'Я загадал число от 1 до 100, попробуй угадать!'
      )
  else:
    'Вы в игре, введите число от 1 до 100 \n'
    'Пока мы играем в игру я могу реагировать только на числа от 1 до 100 и команды /cancel и /stat'
  
# Этот хэндлер будет срабатывать на отказ пользователя играть в игру
@dp.message(F.text.lower().in_(['нет', 'не', 'не хочу', 'не буду']))
async def process_negative_answer(message: Message):
  if not user['in_game']:
    await message.answer(
      'Очень жаль! \n'
      'Если захотите сыграть напишите об этом')
  else:
    await message.answer(
      'Вы в игре! \n'
      'Ведите число от 1 до 100')
      
# этот хэндлер будет отрабатывать при отправке чисел от 1 до 100 пользователем
@dp.message(lambda x: x.text and x.text.isdigit() and 1 <= int(x.text) <= 100)
async def process_number_answer(message: Message):
  if user['in_game']:
    if int(message.text) == user['secret_number']:
      user['in_game'] = False
      user['total_games'] += 1
      user['wins'] +=1
      await message.answer(
        f'Ура, поздравляем, вы угадали число {user["secret_number"]}'
        )
    elif int(message.text) < user['secret_number']:
      user['attemps'] -= 1
      await message.answer(
        'Не угадали, загаданное число больше!\n'
        f'Осталось {user["attemps"]} попыток'
        )
    elif int(message.text) > user['secret_number']:
      user['attemps'] -= 1
      await message.answer(
        'Не угадали, загаданное число меньше! \n'
        f'Осталось {user["attemps"]} попыток'
        )
    if user['attemps'] == 0:
      user['in_game'] = False
      user['total_games'] += 1
      await message.answer(
        'У вас больше не осталось попыток. \n'
        'К сожалению вы ПРОИГРАЛИ \n'
        f'У вас было {ATTEMPS} попыток \n'
        f'Загаданное число было {user["secret_number"]} \n'
        'Хотите сыграть еще?'
        )
  else:
    await message.answer(
      'Мы еще не играем, хотите сыграть?'
      )

# Этот бот будет отрабатывать на все остальные сообщения
@dp.message()
async def process_other_command(message: Message):
  if user['in_game']:
    await message.answer(
      'Мы с вами играем, пришлите число от 1 до 100')
  else:
    await message.answer(
      'Я довольно ограниченный бот. \n'
      'Давайте сыграем в игру "Угадай число!"'
      )


if __name__ == '__main__':
  dp.run_polling(bot)