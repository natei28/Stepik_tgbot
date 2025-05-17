import asyncio
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup, Message, PhotoSize)
from aiogram.filters import Command, CommandStart, StateFilter

from keyboards.keyboards import bottom_kb, markup_cont_fillform, markup_gender, markup_edu, markup_wish_news
from lexicon.lexicon_ru import LEXICON_RU
from config_data.config import user_dict, FSMFillForm, FSMFillForm_list

router = Router()

# Этот зэндлер будет срабатывать на команду /start вне состояний
# и предлагать перейти к заполнению анкеты, отправив команлу /fillform
@router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message):
  await message.answer(text=LEXICON_RU['/start'],
                       reply_markup=bottom_kb)


# Этот хэндлер будет срабатывать на кнопку "Справка"
# в любом состоянии бота, будет определять в каком
# сейчас срстоянии бот и предлагать прлтзователю 
# продожить заполнение анкеты, подсказывая на каком он шаге
@router.message(F.text==LEXICON_RU['help_btn'])
async def procesd_help_command(message: Message, state: FSMContext):
	if await state.get_state() in FSMFillForm_list:
		await message.answer(text=LEXICON_RU['/help'],
		                     reply_markup=markup_cont_fillform)
	else:
		await message.answer(text=LEXICON_RU['/help'])
	#await message.answer(text=LEXICON_RU[await state.get_state()])


# Этот хэндлер будет срабатывать на кнопку "Контакты"
# в любом состоянии бота, будет определять в каком
# сейчас состоянии бот и предлагать пользователю 
# продожить заполнение анкеты, если кнопку нажали при заполнении анкеты
@router.message(F.text==LEXICON_RU['contacts_btn'])
async def process_contacts_command(message: Message, state: FSMContext):
	if await state.get_state() in FSMFillForm_list:
		await message.answer(text=LEXICON_RU['/contacts'],
		                     reply_markup=markup_cont_fillform)
	else:
		await message.answer(text=LEXICON_RU['/contacts'])
		



# Этот хэндлер будет срабатывать на комманду /cancel
# в состоянии по умолчанию и сообщать, что это команда
# работает внутри машины состояний
@router.message(Command(commands='cancel'), StateFilter(default_state))
async def process_cancel_command(message: Message):
  await message.answer(text=LEXICON_RU['/cancel_outFSM'])

# Этот хэндлер будет срабатывать на команду /cancel
# в любом состоянию кроме состояния по умолчанию и 
# отключать машину состояний
@router.message(Command(commands='cancel'), ~StateFilter(default_state))
async def process_cancel_inState_command(message: Message, state: FSMContext):
  await message.answer(text=LEXICON_RU['/cancel_inFSM'])
  await state.clear()
  

# Этот хэндлер будет срабатывать на команду /fillform
# и переврдить бота в состояние одидания ввода Имени
#@router.message(Command(commands='fillform'), StateFilter(default_state))
@router.message(Command(commands='fillform'), StateFilter(default_state))
@router.message(F.text==LEXICON_RU['fillstart_btn'],StateFilter(default_state))
async def process_fillform_command(message: Message, state: FSMContext):
  await message.answer(text=LEXICON_RU['/fillform'])
  await asyncio.sleep(1) 
  await message.answer(text=LEXICON_RU['name_sent'])
  await state.set_state(FSMFillForm.fill_name)
#  print(LEXICON_RU[await state.get_state()])
  
  
# Этот хэндлер будет срабатывать если введено корректное Имя
# и переводить бота в состочние ожидания ввода возраста
@router.message(StateFilter(FSMFillForm.fill_name), F.text.isalpha())
async def process_name_sent(message: Message, state: FSMContext):
  # Сохраняем введенное имя в хранилище по ключу name
  await state.update_data(name=message.text)
  await message.answer(text=LEXICON_RU['thanks'])
  await asyncio.sleep(1) 
  await message.answer(text=LEXICON_RU['age_sent'])
  await state.set_state(FSMFillForm.fill_age)
  
# Этот хэндлер будет срабатывать,если во время ввода
# имени введено чтото некоректное
@router.message(StateFilter(FSMFillForm.fill_name))
async def warning_not_name(message: Message):
  await message.answer(text=LEXICON_RU['wrong'])
  await asyncio.sleep(1) 
  await message.answer(text=LEXICON_RU['note_name'])


# Этот хэндлер будет срабатывать, если введен коректный возраст
# и переводить бота в состояние выбора пола
@router.message(StateFilter(FSMFillForm.fill_age),
                lambda x: x.text.isdigit() and 4 <= int(x.text) <= 120)
async def process_age_sent(message: Message, state: FSMContext):
  await state.update_data(age=message.text)
  await message.answer(text=LEXICON_RU['thanks'])
  await asyncio.sleep(1)
  await message.answer(text=LEXICON_RU['gender_sent'],
                       reply_markup=markup_gender)
  await state.set_state(FSMFillForm.fill_gender)
  
# Этот хэндлер будет сратавать, если во время ввода
# возраста ввести что нибудь некорректное
@router.message(StateFilter(FSMFillForm.fill_age))
async def warning_not_age(message: Message):
  await message.answer(text=LEXICON_RU['wrong'])
  await asyncio.sleep(1)
  await message.answer(text=LEXICON_RU['note_age'])

#-------------------------------------------------------------------------#
# Этот хзндлер будет срабатывать на нажатие
# кнопки при выборе пола и переводить бот в 
# состояние отпраки фото
@router.callback_query(StateFilter(FSMFillForm.fill_gender), 
                       F.data.in_(['male', 'female', 'undefined_gender']))
async def process_gender_press(callback: CallbackQuery, state: FSMContext):
  await state.update_data(gender=callback.data)
  await callback.message.delete()
  await asyncio.sleep(1)
  await callback.message.answer(text=LEXICON_RU['thanks'])
  await callback.message.answer(text="проаерка")
  await asyncio.sleep(1)
  await callback.message.answer(text=LEXICON_RU['photo_get'])
  await state.set_state(FSMFillForm.upload_photo)

# Этот хэндлер будет срабатывать, если время выбора пола
# будет отправлено чтото другое
@router.message(StateFilter(FSMFillForm.fill_gender))
async def warning_not_gender(message: Message):
  await message.answer(text=LEXICON_RU['wrong'])
  await asyncio.sleep(1)
  await message.answer(text=LEXICON_RU['note_gender'])
  await asyncio.sleep(1)
  await message.answer(text=LEXICON_RU['gender_sent'],
                       reply_markup=markup_gender)


#-------------------------------------------------------------------------#
# Этот хэндлер будет срабатывать на отправку пользователем
# своей фотографии и переводить бота в состояние ожидания
# выбора образования
@router.message(StateFilter(FSMFillForm.upload_photo), 
                F.photo[-1].as_('largest_photo'))
async def process_photo_sent(message: Message,
                             state: FSMContext,
                             largest_photo: PhotoSize):
  await state.update_data(
    photo_unique_id=largest_photo.file_unique_id,
    photo_id=largest_photo.file_id)
  await message.answer(text=LEXICON_RU['thanks'])
  await asyncio.sleep(1)
  await message.answer(text=LEXICON_RU['edu_sent'],
                       reply_markup=markup_edu)
  await state.set_state(FSMFillForm.fill_education)
  
# Этот хэндлер будет срабатывать, если во время отправки
# фотографии, пользователем будет отправлено чтото другое
@router.message(StateFilter(FSMFillForm.upload_photo))
async def warning_not_photo(message: Message):
	await message.answer(text=LEXICON_RU['wrong'])
	await asyncio.sleep(1)
	await message.answer(text=LEXICON_RU['note_photo'])
	
	
#-------------------------------------------------------------------------#
# Этот хэндлер будет срабатывать, если выбрано образование
# и переводить бота в состояние выбора согласия на новости
@router.callback_query(StateFilter(FSMFillForm.fill_education),
                       F.data.in_(['higher', 'secondary', 'no_edu']))
async def process_edu_press(callback: CallbackQuery, state: FSMContext):
	await state.update_data(education=callback.data)
	await callback.message.delete()
	await callback.message.answer(text=LEXICON_RU['thanks'])
	await asyncio.sleep(1)
	await callback.message.answer(text=LEXICON_RU['wish_news_sent'],
	                              reply_markup=markup_wish_news)
	await state.set_state(FSMFillForm.fill_wish_news)

# Этот хэндлер бедет срабатывать, если вместо выбора образования
# отправлено чтото другое
@router.message(StateFilter(FSMFillForm))
async def warning_not_edu(message: Message):
	await message.answer(text=LEXICON_RU['wrong'])
	await asyncio.sleep(1)
	await message.answer(text=LEXICON_RU['note_edu'])


#-------------------------------------------------------------------------#
# Этот хэндлер будет срабатывать на нажатие кнопки
# согласия или не согласия получать новости и переводить
# бота в состояние "по умолчанию"
@router.callback_query(StateFilter(FSMFillForm.fill_wish_news,
                       F.data.in_(['yes_news', 'no_news'])))
async def process_wish_news_press(callback: CallbackQuery, state:FSMContext):
	await state.update_data(wish_news=callback.data == 'yes_news')
	user_dict[callback.from_user.id] = await state.get_data()
	await callback.message.answer(text=LEXICON_RU['thanks'])
	await state.clear()
	await asyncio.sleep(1)
	await callback.message.answer(text=LEXICON_RU['out_fsm'])
	await asyncio.sleep(1)
	await callback.message.answer(text=LEXICON_RU['show_data'])

# Этот хэндлер будет срабатывать, если во время согласия на получение
# новостей будет введено/отправлено что-то некорректноеR
@router.message(StateFilter(FSMFillForm.fill_wish_news))
async def warning_not_wish_news(message:Message):
	await message.answer(text=LEXICON_RU['note_wish_news'])


#-------------------------------------------------------------------------#
# Этот хэндлер будет срабатывать на команду /showdata
# и отправлять в чат данные анкеты, либо сообщать 
# об отсутствии данных
@router.message(StateFilter(default_state), Command(commands='showdata'))
async def process_showdata_command(message: Message):
	if message.from_user.id in user_dict:
		await message.answer_photo(
			photo=user_dict[message.from_user.id]["photo_id"],
			caption=f'Имя: {user_dict[message.from_user.id]["name"]}\n'
			        f'Возраст: {user_dict[message.from_user.id]["age"]}\n'
			        f'Пол: {user_dict[message.from_user.id]["gender"]}\n'
			        f'Образование: {user_dict[message.from_user.id]["education"]}\n'
			        f'Получать новости: {user_dict[message.from_user.id]["wish_news"]}')
	else:
		await message.answer(text=LEXICON_RU['note_anket_data'])
		
	



#router.message.register(process_start_command, Command(commands="start"), StateFilter(default_state))
#router.message.register(process_start_command, Command(commands="start"), StateFilter(default_state))