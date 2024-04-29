from aiogram import Router, flags
from aiogram.filters import Command
from aiogram.types import Message

from data.l10n.translator import LocalizedTranslator
from tgbot.misc.constants import SUPPORT_USERNAME

commands_router = Router()


@commands_router.message(Command("help"))
@flags.rate_limit(key="default")
async def get_help(
        message: Message,
        l10n: LocalizedTranslator
):
    await message.answer(l10n.get_text(key="help", args={"support_username": SUPPORT_USERNAME}))
