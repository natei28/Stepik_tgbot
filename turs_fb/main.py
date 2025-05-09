import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup, Message, PhotoSize, BotCommand)

from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from config_data.config import Config, load_config
from handlers import other_handlers, user_handlers

# Инициализируем логгер
logger = logging.getLogger(__name__)

# Инициализируем хранилище (создаем экземпляр класса MemotyStоrage)
storage = MemoryStorage()

# Функция конфигурирования и запуска бота
async def main():
  # Конфигурируем логирование
  logging.basicConfig(
    level=logging.INFO,
    format='%(filename)s:%(lineno)d #%(levelname)-8s '
           '[%(asctime)s] - %(name)s - %(message)s')
  # Выводим в консоль информацию о начале запуска бота
  logger.info('Starting bot')

  # Загружаем конфиг в переменную config
  config: Config = load_config()

  # Инициализируем бот и диспетчер
  bot = Bot(
    token=config.tg_bot.token,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML))
  dp = Dispatcher(storage=storage)
  

# Создаем асинхронную функции
  async def set_main_menu(bot: Bot):
    # Создаем список с командами и их описанием для кнопки menu
    main_menu_commands = [
        BotCommand(command='/cancel',
                   description='Отменить заполнение формы'),
        BotCommand(command='/fillform',
                   description='Заполнить форму-анкету'),
        BotCommand(command='/help',
                   description='Информация о работе Бота')
    ]

    await bot.set_my_commands(main_menu_commands)

    

  # Регистриуем роутеры в диспетчере
  dp.startup.register(set_main_menu)
  dp.include_router(user_handlers.router)
  dp.include_router(other_handlers.router)

  # Пропускаем накопившиеся апдейты и запускаем polling
  await bot.delete_webhook(drop_pending_updates=True)
  await dp.start_polling(bot)


asyncio.run(main())