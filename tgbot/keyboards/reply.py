from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from data.l10n.translator import LocalizedTranslator


def main_menu_kb(l10n: LocalizedTranslator):
    builder = ReplyKeyboardBuilder()

    buttons = [
        KeyboardButton(text=l10n.get_text(key="reserve-topchan-btn")),
        KeyboardButton(text=l10n.get_text(key="feedback-btn")),
        KeyboardButton(text=l10n.get_text(key="settings-btn")),
    ]

    builder.add(*buttons)
    builder.adjust(1, 2)
    return builder.as_markup(resize_keyboard=True)


def phone_request_kb(l10n: LocalizedTranslator):
    builder = ReplyKeyboardBuilder()

    buttons = [
        KeyboardButton(text=l10n.get_text(key="phone-request-btn"), request_contact=True),
    ]
    builder.add(*buttons)
    return builder.as_markup(resize_keyboard=True)


def feedback_kb(l10n: LocalizedTranslator):
    builder = ReplyKeyboardBuilder()
    builder.button(text=l10n.get_text(key="cancel-btn"))
    return builder.as_markup(resize_keyboard=True)
