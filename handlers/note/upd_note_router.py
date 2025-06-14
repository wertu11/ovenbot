from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from keyboards.reply_note_kb import main_note_kb

upd_note_router = Router()


class UPDNoteStates(StatesGroup):
    content_text = State()
