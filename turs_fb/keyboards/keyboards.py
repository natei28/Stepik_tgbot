from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from lexicon.lexicon_ru import LEXICON_RU



male_button = InlineKeyboardButton(
  text='Мужской ♂',
  callback_data='male')

female_button = InlineKeyboardButton(
  text='Женский ♀',
  callback_data='female')

undefined_button = InlineKeyboardButton(
  text='🤷 Пока не ясно',
  callback_data='undefined_gender')
  
keyboard_male: list[list[InlineKeyboardButton]] = [
  [male_button, female_button],
  [undefined_button]]
  
markup_gender = InlineKeyboardMarkup(inline_keyboard=keyboard_male)

