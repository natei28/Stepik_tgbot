from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand

# Вместо BOT TOKEN HERE нужно вставить токен вашего бота,
# полученный у @BotFather
BOT_TOKEN = '7486773575:AAEEIZ5N_v4UBKGm3enXkA3gpqE3Wil1J5E'

# Создаем объекты бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# Создаем асинхронную функцию
async def set_main_menu(bot: Bot):
  # Создаем список с командами и их описанием для кнопки menu
  main_menu_commands = [
    BotCommand(
      command='/help',
      description='Справка по работе бота'),
    BotCommand(
      command='/support',
      description='Поддержка'),
    BotCommand(
      command='/contacts',
      description='Другие способы связи'),
    BotCommand(
      command='/payments',
      description='Платежи')
  ]
  await bot.set_my_commands(main_menu_commands)


# Регистрируем асинхронную функцию в диспетчере,
# которая будет выполняться на старте бота,
dp.startup.register(set_main_menu)
# Запускаем поллинг
dp.run_polling(bot)