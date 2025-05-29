from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from lexicon.lexicon_ru import LEXICON_RU, FRUIT_LIST
#from main.py import FRUIT_LIST


#----------------------------------------------------------#
#-----------Создание reply-клавиатуры c командами----------#

# Создаем сами кнопки
fillstart_button = KeyboardButton(text=LEXICON_RU['fillstart_btn'])
showdata_button =  KeyboardButton(text=LEXICON_RU['showdata_btn'])
cancel_button =    KeyboardButton(text=LEXICON_RU['cancel_btn'])
help_button =      KeyboardButton(text=LEXICON_RU['help_btn'])
contacts_button =  KeyboardButton(text=LEXICON_RU['contacts_btn'])

# Создаем клавиатуру
bottom_kb = ReplyKeyboardMarkup(
	keyboard=[
		[fillstart_button, showdata_button],
		[cancel_button, help_button, contacts_button]],
	resize_keyboard=True)


#----------------------------------------------------------#
#----Создание-клавиатуры c кнопками продолжить/отмена------#
continue_button = InlineKeyboardButton(
	text='Прожолжить заполнение',
	callback_data="continue_fillform")
	
markup_cont_fillform = InlineKeyboardMarkup(
	inline_keyboard=[[continue_button]])



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






def check_fruit_modkb(check_data):
  aple_button = InlineKeyboardButton(
    text=FRUIT_LIST['check_aple'],
    callback_data='check_aple')

  orange_button = InlineKeyboardButton(
    text=FRUIT_LIST['check_orange'],
    callback_data='check_orange')
  
  banan_button = InlineKeyboardButton(
    text=FRUIT_LIST['check_banan'],
    callback_data='check_banan')

  kiwi_button = InlineKeyboardButton(
    text=FRUIT_LIST['check_kiwi'],
    callback_data='check_kiwi')
    
#  fruit_next_button = InlineKeyboardButton(
#    text='Продолжить',
#    callback_data='fruit_next_button')
  
  keyboard_fruit: list[list[InlineKeyboardButton]] = [
  [aple_button, orange_button],
  [banan_button, kiwi_button]]
#  [fruit_next_button]]
  
  markup_fruit = InlineKeyboardMarkup(inline_keyboard=keyboard_fruit)
  return markup_fruit


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


#----------------------------------------------------------#
#---------Создание клавиатуры согласия на новости----------#

yes_news_button = InlineKeyboardButton(
  text='Да, согласен!',
  callback_data='yes_news')

no_news_button = InlineKeyboardButton(
  text='Нет, спасибо!',
  callback_data='no_news')
  
keyboard_wish_news: list[list[InlineKeyboardButton]] = [
  [yes_news_button, no_news_button]]
  
markup_wish_news = InlineKeyboardMarkup(inline_keyboard=keyboard_wish_news)