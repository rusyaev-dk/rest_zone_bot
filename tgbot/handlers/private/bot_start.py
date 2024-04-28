import html

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from data.infrastructure.database.models import UserDBModel
from data.l10n.translator import TranslatorHub
from domain.repositories.db_repo.requests import RequestsRepo

from tgbot.keyboards.inline import SetUserLanguageFactory
from tgbot.keyboards.reply import main_menu_kb, phone_request_kb
from tgbot.misc.states import UserRegistrationSG
from tgbot.services.setup_bot_commands import update_user_commands

start_router = Router()


@start_router.message(CommandStart())
async def bot_start(message: Message):
    await message.reply("Hello!")


@start_router.callback_query(SetUserLanguageFactory.filter())
async def set_user_language(
        call: CallbackQuery,
        repo: RequestsRepo,
        callback_data: SetUserLanguageFactory,
        translator_hub: TranslatorHub,
        state: FSMContext,
):
    language_code = callback_data.language_code
    l10n = translator_hub.l10ns.get(language_code)

    user = await repo.users.get_user(telegram_id=call.from_user.id)

    await call.answer()
    await call.message.delete()
    await update_user_commands(bot=call.bot, l10n=l10n)

    if user:
        await repo.users.update_user(UserDBModel.telegram_id == call.from_user.id, language=language_code)
        text = l10n.get_text(key="main-menu-msg")
        await call.message.answer_sticker(
            text,
            reply_markup=main_menu_kb(l10n=l10n)
        )
        return
    args = {
        "name": html.escape(call.from_user.full_name),
    }
    text = l10n.get_text(key="hello-msg", args=args)
    await call.message.answer(
        text=text,
        reply_markup=phone_request_kb(l10n=l10n),
    )
    await state.set_state(UserRegistrationSG.get_phone)
    data = {"language_code": language_code}
    await state.update_data(data=data)


@start_router.message(UserRegistrationSG.get_phone)
async def get_user_phone(
        message: Message,
        repo: RequestsRepo,
        translator_hub: TranslatorHub,
        state: FSMContext,
):
    data = await state.get_data()
    language_code = data.get("language_code")
    l10n = translator_hub.l10ns.get(language_code)
    if not message.contact:
        text = l10n.get_text(key="incorrect-phone-msg")
        await message.answer(
            text=text,
            reply_markup=phone_request_kb(l10n=l10n),
        )
        return

    await repo.users.add_user(
        telegram_id=message.from_user.id,
        full_name=message.from_user.full_name,
        language=language_code,
        username=message.from_user.username,
        phone=message.contact.phone_number,
    )

    text = l10n.get_text(key="registration-complete-msg")
    await message.answer(
        text=text,
        reply_markup=main_menu_kb(l10n=l10n)
    )
    await state.clear()
