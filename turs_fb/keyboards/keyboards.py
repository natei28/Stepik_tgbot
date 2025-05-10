from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from lexicon.lexicon_ru import LEXICON_RU


#----------------------------------------------------------#
#--------------Создание клавиатуры выбора пола-------------#

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

#----------------------------------------------------------#
#----------Создание клавиатуры выбора образования----------#

hi_educ_button = InlineKeyboardButton(
  text='Высшее',
  callback_data='higher')

sec_educ_button = InlineKeyboardButton(
  text='Среднее',
  callback_data='secondary')

no_educ_button = InlineKeyboardButton(
  text='Нет образования',
  callback_data='no_edu')
  
keyboard_edu: list[list[InlineKeyboardButton]] = [
  [hi_educ_button, sec_educ_button],
  [no_educ_button]]
  
markup_edu = InlineKeyboardMarkup(inline_keyboard=keyboard_edu)