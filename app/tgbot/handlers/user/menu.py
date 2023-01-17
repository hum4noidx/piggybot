from aiogram.types import Message

from tgbot.handlers.message_templates import challenge_rules


async def menu_hello(event: Message):
    await event.answer(f'Привет, {event.from_user.full_name}!')
    await event.answer(challenge_rules())
