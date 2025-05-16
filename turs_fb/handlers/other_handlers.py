from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.types import Message

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.fsm.storage.memory import MemoryStorage

from config_data.config import FSMFillForm

from lexicon.lexicon_ru import LEXICON_RU

router = Router()


# Хэндлер для сообщений, которые не попали в другие хэндлеры
@router.message(StateFilter(default_state))
async def send_answer(message: Message):
  await message.reply(text=LEXICON_RU['other_answer'])