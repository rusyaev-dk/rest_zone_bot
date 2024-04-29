from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder


class SetUserLanguageFactory(CallbackData, prefix="set_language"):
    language_code: str


class FeedbackFactory(CallbackData, prefix="feedback"):
    user_id: int
    msg_to_reply_id: int


class NotifyUsersTargetLanguageFactory(CallbackData, prefix="notify_users"):
    target_language_code: str


class NotifyUsersApproveFactory(CallbackData, prefix="notify_approve"):
    approved: bool


def set_user_language_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text="🇷🇺 Русский", callback_data=SetUserLanguageFactory(language_code="ru"))
    builder.button(text="🇺🇿 O'zbek", callback_data=SetUserLanguageFactory(language_code="uz"))

    builder.adjust(2)

    return builder.as_markup()


def answer_to_user_kb(user_id: int, msg_to_reply_id: int):
    builder = InlineKeyboardBuilder()
    builder.button(text="🖋 Ответить",
                   callback_data=FeedbackFactory(user_id=user_id, msg_to_reply_id=msg_to_reply_id))

    return builder.as_markup()


def set_target_language_code_kb():
    builder = InlineKeyboardBuilder()

    builder.button(text="🇷🇺 ru", callback_data=NotifyUsersTargetLanguageFactory(target_language_code="ru"))
    builder.button(text="🇺🇿 uz", callback_data=NotifyUsersTargetLanguageFactory(target_language_code="uz"))
    builder.button(text="🇬🇧 en", callback_data=NotifyUsersTargetLanguageFactory(target_language_code="en"))
    builder.button(text="🌐 Все", callback_data=NotifyUsersTargetLanguageFactory(target_language_code="all"))
    builder.button(text="❌ Отмена", callback_data=NotifyUsersTargetLanguageFactory(target_language_code="cancel"))

    builder.adjust(3, 1)

    return builder.as_markup()


def notify_approve_kb():
    builder = InlineKeyboardBuilder()

    builder.button(text="✅ Да",
                   callback_data=NotifyUsersApproveFactory(approved=True))
    builder.button(text="❌ Нет",
                   callback_data=NotifyUsersApproveFactory(approved=False))

    builder.adjust(2)

    return builder.as_markup()
