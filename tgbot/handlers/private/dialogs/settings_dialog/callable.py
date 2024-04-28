import html
from typing import List, Dict

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button, Select

from data.infrastructure.database.models import UserDBModel
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
    await call.message.answer(l10n.get_text(key='main-menu'))
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

    await repo.users.update_user(UserDBModel.telegram_id == call.from_user.id, language=language_code)
    l10n = translator_hub.l10ns.get(language_code)

    await dialog_manager.done()
    await dialog_manager.reset_stack()
    await call.message.delete()
    await update_user_commands(bot=call.bot, l10n=l10n)
    args = {
        "name": html.escape(call.from_user.full_name),
        "terms_of_use": f"<a href='{l10n.get_text(key='terms-of-use-link')}'>"
                        f"<b>{l10n.get_text(key='terms-of-use-name')}</b></a>"
    }
    text = l10n.get_text(key="hello", args=args)
    await call.message.answer(text, reply_markup=main_menu_kb(l10n=l10n), disable_web_page_preview=True)
    await call.message.answer(l10n.get_text(key='hello-info'))
