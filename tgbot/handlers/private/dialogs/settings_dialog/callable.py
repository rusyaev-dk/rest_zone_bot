import html
import re

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button

from data.l10n.translator import LocalizedTranslator, TranslatorHub
from domain.repositories.db_repo.requests import RequestsRepo
from tgbot.keyboards.reply import main_menu_kb
from tgbot.misc.states import SettingsSG
from tgbot.services.setup_bot_commands import update_user_commands


async def close_settings(
        call: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager
):
    l10n: LocalizedTranslator = dialog_manager.middleware_data.get("l10n")
    await call.message.delete()
    await call.message.answer(l10n.get_text(key='main-menu-msg'), reply_markup=main_menu_kb(l10n=l10n))
    await dialog_manager.done()
    await dialog_manager.reset_stack()


async def change_user_language(
        call: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
):
    translator_hub: TranslatorHub = dialog_manager.middleware_data.get("translator_hub")
    repo: RequestsRepo = dialog_manager.middleware_data.get("repo")
    language_code = button.widget_id[:2]

    await repo.users.update_user_language(
        telegram_id=call.from_user.id,
        language_code=language_code
    )
    l10n = translator_hub.l10ns.get(language_code)

    await dialog_manager.done()
    await dialog_manager.reset_stack()
    await call.message.delete()
    await update_user_commands(bot=call.bot, l10n=l10n)
    args = {
        "name": html.escape(call.from_user.full_name),
    }
    text = l10n.get_text(key="hello-msg", args=args)
    await call.message.answer(text, reply_markup=main_menu_kb(l10n=l10n))


# async def phone_validation_filter(
#         message: Message,
#         dialog_manager: DialogManager,
# ):
#     if message.contact:
#         return str(message.contact.phone_number)
#     phone = message.text
#     pattern = r'^\+\d{3}\s?\d{2}\s?\d{3}\s?\d{2}\s?\d{2}$'
#
#     if re.match(pattern, phone):
#         if phone[0] != '+':
#             return "+" + phone
#         return phone
#     else:
#         l10n: LocalizedTranslator = dialog_manager.middleware_data.get("l10n")
#         text = l10n.get_text(key="incorrect-phone-settings-msg")
#         await message.answer(text=text)


async def correct_phone_handler(
        message: Message,
        widget: MessageInput,
        dialog_manager: DialogManager,
) -> None:
    repo: RequestsRepo = dialog_manager.middleware_data.get("repo")
    l10n: LocalizedTranslator = dialog_manager.middleware_data.get("l10n")

    if message.contact:
        phone = message.contact.phone_number
    else:
        phone = message.text
        pattern = r'^\+?998\s?\d{2}\s?\d{3}\s?\d{2}\s?\d{2}$'

        if not re.match(pattern, phone):
            return
        elif phone[0] != '+':
            phone = "+" + phone

    await repo.users.update_user_phone(
        telegram_id=message.from_user.id,
        phone=phone
    )
    text = l10n.get_text(key='settings-applied-msg')
    await message.answer(text=text, reply_markup=main_menu_kb(l10n=l10n))
    await dialog_manager.switch_to(SettingsSG.overall_settings)
