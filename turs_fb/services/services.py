from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from lexicon.lexicon_ru import LEXICON_RU, FRUIT_LIST
from keyboards.keyboards import keyboard_fruit, markup_fruit

#----------------------------------------------------------#
#--------------Создание клавиатуры выбора фруктов-------------#
def check_fruit_modkb(check_data):
  aple_button = InlineKeyboardButton(
    text=FRUIT_LIST['check_aple'],
    callback_data='check_aple')

  orange_button = InlineKeyboardButton(
    text=FRUIT_LIST['check_orange'],
    callback_data='check_orange')
  
  keyboard_fruit: list[list[InlineKeyboardButton]] = [
  [aple_button, orange_button]]
  
  markup_fruit = InlineKeyboardMarkup(inline_keyboard=keyboard_fruit)
  return markup_fruit