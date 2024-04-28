from typing import List, Dict

from aiogram.types import User as AIOGRAMuser
from aiogram_dialog import DialogManager

from data.l10n.translator import LocalizedTranslator
from domain.repositories.db_repo.requests import RequestsRepo


async def overall_settings_getter(
        dialog_manager: DialogManager,
        **kwargs
):
    user: AIOGRAMuser = dialog_manager.event.from_user
    l10n: LocalizedTranslator = dialog_manager.middleware_data.get("l10n")
    repo: RequestsRepo = dialog_manager.middleware_data.get("repo")

    db_user = await repo.users.get_user(telegram_id=user.id)

    data = {
        "choose_option_text": l10n.get_text(key='choose-option'),

        "change_language_btn_text": l10n.get_text(key='change-language-btn'),
        "close_btn_text": l10n.get_text(key='close-btn')
    }

    return data


async def change_language_getter(
        dialog_manager: DialogManager,
        **kwargs
):
    l10n: LocalizedTranslator = dialog_manager.middleware_data.get("l10n")

    data = {
        "back_btn_text": l10n.get_text(key='back-btn')
    }

    return data
