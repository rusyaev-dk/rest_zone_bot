from aiogram import Bot
from aiogram.types import User as AIOGRAMuser
from aiogram_dialog import DialogManager

from data.l10n.translator import LocalizedTranslator
from domain.repositories.db_repo.requests import RequestsRepo
from tgbot.keyboards.reply import phone_request_kb


async def overall_settings_getter(
        dialog_manager: DialogManager,
        **kwargs
):
    user: AIOGRAMuser = dialog_manager.event.from_user
    l10n: LocalizedTranslator = dialog_manager.middleware_data.get("l10n")
    repo: RequestsRepo = dialog_manager.middleware_data.get("repo")
    bot: Bot = dialog_manager.middleware_data.get("bot")

    phone_request_message_id = dialog_manager.dialog_data.get("phone_request_message_id")
    if phone_request_message_id:
        await bot.delete_message(chat_id=user.id, message_id=phone_request_message_id)

    db_user = await repo.users.get_user(telegram_id=user.id)
    overall_text_args = {"phone": db_user.phone}
    data = {
        "overall_settings_text": l10n.get_text(key='overall-settings-msg', args=overall_text_args),
        "change_phone_btn_text": l10n.get_text(key='change-phone-btn'),
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


async def change_phone_getter(
        dialog_manager: DialogManager,
        **kwargs
):
    user: AIOGRAMuser = dialog_manager.event.from_user
    l10n: LocalizedTranslator = dialog_manager.middleware_data.get("l10n")
    bot: Bot = dialog_manager.middleware_data.get("bot")

    data = {
        "send_phone_msg_text": l10n.get_text(key='phone-setting-msg'),
        "back_btn_text": l10n.get_text(key='back-btn')
    }

    text = l10n.get_text('send-phone-msg')
    phone_request_message = await bot.send_message(
        text=text,
        chat_id=user.id,
        reply_markup=phone_request_kb(l10n=l10n),
    )

    dialog_manager.dialog_data.update(phone_request_message_id=phone_request_message.message_id)
    return data
