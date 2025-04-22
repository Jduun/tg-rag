from aiogram import Router
from aiogram.types import Message

from llm import get_llm_answer

router: Router = Router()


@router.message()
async def process_text_message(message: Message):
    answer = await get_llm_answer(message.from_user.id, message.text)
    await message.reply(text=answer)
