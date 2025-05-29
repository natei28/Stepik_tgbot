from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from lexicon.lexicon_ru import LEXICON_RU, FRUIT_LIST


aple_button = InlineKeyboardButton(
  #text=FRUIT_LIST['aple'],
  text='яблоко',
  callback_data='aple_check')
  
orange_button = InlineKeyboardButton(
  #text=FRUIT_LIST['orange'],
  text='апельсин',
  callback_data='orange_check')

fruit_kb = [aple_button, orange_button]
  
markup_fruit = InlineKeyboardMarkup(
  inline_keyboard=fruit_kb)