from dataclasses import dataclass
from environs import Env
from aiogram.fsm.state import State, StatesGroup

@dataclass
class TgBot:
  token: str  # Токен для доступа к телеграм-боту


@dataclass
class Config:
  tg_bot: TgBot


def load_config(path: str | None = None) -> Config:
  env = Env()
  env.read_env(path)
  return Config(tg_bot=TgBot(token=env('BOT_TOKEN')))
  
  
  

#Создаем базу данных пользователей
user_dict: dict[int, dict[str, str | int | bool]] = {}
  
#  Создаем класс (FSMFillForm) наследуемый от класса StateGroup (FSMFill группа для определения состояний, в еашем проекте одна гпуппа, 6пупп может много)
class FSMFillForm(StatesGroup):
#   Создаем экземплярв класса State, последовательно перечисляя возможные состояния, 
#   в которых бот модет находится, взаимодействуя с пользователем
  fill_name = State()          # Состояние ожидания ввода имени
  fill_age = State()           # Состояние ожидания ввода возраста
  fill_gender = State()        # Состояние ожидания выбора пола
  upload_photo = State()       # Состояние ожидания загрузки фото
  fill_education = State()     # Состояние ожидания выбора образования
  fill_wish_news = State()     # Состояние ожидания выбора прлучать ли новости
  check_fruit = State()

# Создаем список из состояний FSMFillForm:
#  - вытаскиваем в список все атрибуты класса FSMFillForm
#  - добавлем к элементам списка FSMFillForm:
FSMFillForm_list = ['FSMFillForm:' + x for x in dir(FSMFillForm)]


# создаем спмисок с выбором фруктов от пользователя
user_chek_fruit = []