from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder


class SetUserLanguageFactory(CallbackData, prefix="set_language"):
    language_code: str


class FeedbackFactory(CallbackData, prefix="feedback"):
    user_id: int
    msg_to_reply_id: int


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
